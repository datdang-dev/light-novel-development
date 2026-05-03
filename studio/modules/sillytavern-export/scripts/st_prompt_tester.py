#!/usr/bin/env python3
"""
SillyTavern Prompt Pipeline Tester
===================================
Simulates how SillyTavern assembles the messages[] array sent to the AI model.
Use this to inspect and validate what the model actually receives, without
opening the SillyTavern UI.

Pipeline order (mirroring openai.js → populateChatCompletion):
  1. System Prompt (Main Prompt from Chat Preset)
  2. Character Description + Personality
  3. Scenario
  4. Lorebook entries (keyword-triggered, injected at their configured depth/position)
  5. Depth Prompt (from character card extensions)
  6. Chat History (user/assistant turns)
  7. Post-History / Jailbreak Prompt (injected at depth 0 = last user message)

Usage:
  python3 st_prompt_tester.py <character_card.json> [options]

Options:
  --chat <file.json>     Mock chat history (array of {role, content})
  --user-msg <text>      Single user message to test with
  --user-name <name>     User's display name (default: Kurosaki Dat)
  --output <file>        Write assembled payload to file (JSON)
  --send                 Send the assembled payload to OpenRouter API
  --model <model>        Model to use (default: arcee-ai/trinity-large-preview:free)
  --verbose              Show token estimates per message
  --no-color             Disable colored output

Environment:
  OPEN_ROUTER_API_KEY    API key (loaded from .env or env var)
"""

import json
import argparse
import sys
import os
import re
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.markdown import Markdown
    has_rich = True
except ImportError:
    has_rich = False

# ── ANSI Colors ──────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"
    BG_DARK = "\033[40m"

NO_COLOR = False

def c(color, text):
    if NO_COLOR:
        return text
    return f"{color}{text}{C.RESET}"


# ── Helpers ──────────────────────────────────────────────
def estimate_tokens(text):
    """Rough token estimate: ~4 chars per token for English, ~2-3 for CJK/Vietnamese."""
    return max(1, len(text) // 3)

def replace_macros(text, char_name, user_name):
    """Replace SillyTavern macros: {{char}}, {{user}}"""
    text = text.replace("{{char}}", char_name)
    text = text.replace("{{user}}", user_name)
    # Remove unresolved macros like {{getvar::...}}
    text = re.sub(r'\{\{getvar::[^}]*\}\}', '', text)
    return text

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_env(start_dir=None):
    """Walk upward from start_dir looking for .env, parse KEY=VALUE lines."""
    d = Path(start_dir or os.getcwd()).resolve()
    for _ in range(10):  # max 10 levels up
        env_file = d / '.env'
        if env_file.is_file():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, _, value = line.partition('=')
                        os.environ.setdefault(key.strip(), value.strip())
            return str(env_file)
        if d.parent == d:
            break
        d = d.parent
    return None


# ── Lorebook Engine ──────────────────────────────────────
def trigger_lorebook(entries, chat_text, char_name, user_name):
    """
    Scan chat_text for lorebook keyword triggers.
    Returns list of triggered entries with their content and position metadata.
    """
    triggered = []
    for entry in entries:
        if not entry.get('enabled', True):
            continue
        keys = entry.get('keys', [])
        is_constant = entry.get('constant', False)
        
        if is_constant:
            triggered.append(entry)
            continue
            
        for key in keys:
            key_resolved = replace_macros(key, char_name, user_name)
            if key_resolved.lower() in chat_text.lower():
                triggered.append(entry)
                break
    
    return triggered


# ── Chat Completion Preset Loader ────────────────────────
def load_preset(preset_path, char, char_name, user_name):
    """
    Load a SillyTavern Chat Completion Preset and resolve which prompts are enabled.
    Returns (preset_data, ordered_items) where ordered_items is a list of dicts:
      { 'identifier', 'name', 'role', 'content', 'injection_depth', 'injection_position', 'is_marker', 'marker_type' }
    """
    preset = load_json(preset_path)
    prompts_by_id = {}
    for p in preset.get('prompts', []):
        prompts_by_id[p['identifier']] = p

    # Get prompt_order — first entry (char_id 100000) = marker order,
    # second entry (char_id 100001) = custom items with enabled overrides
    prompt_orders = preset.get('prompt_order', [])

    # Build enabled set from prompt_order overrides
    enabled_overrides = {}
    for po in prompt_orders:
        for item in po.get('order', []):
            enabled_overrides[item['identifier']] = item.get('enabled', False)

    # Known marker identifiers that map to character card fields
    MARKER_IDS = {
        'main', 'nsfw', 'jailbreak', 'charDescription', 'charPersonality',
        'scenario', 'personaDescription', 'worldInfoBefore', 'worldInfoAfter',
        'chatHistory', 'dialogueExamples', 'enhanceDefinitions'
    }

    # Get the marker order (character_id 100000)
    marker_order = []
    for po in prompt_orders:
        if po.get('character_id') == 100000:
            marker_order = po.get('order', [])
            break

    # Get custom items order (character_id 100001)
    custom_order = []
    for po in prompt_orders:
        if po.get('character_id') == 100001:
            custom_order = po.get('order', [])
            break

    # Resolve custom items — items enabled in prompt_order override the item-level enabled
    enabled_custom_items = []
    for co in custom_order:
        cid = co['identifier']
        is_enabled = co.get('enabled', False)
        if is_enabled and cid in prompts_by_id:
            item = prompts_by_id[cid]
            content = item.get('content', '')
            if not content or content.strip() == '':
                continue
            # Skip items that are just macro comments like {{// ...}}
            clean = re.sub(r'\{\{//[^}]*\}\}', '', content).strip()
            if not clean:
                continue
            enabled_custom_items.append({
                'identifier': cid,
                'name': item.get('name', ''),
                'role': item.get('role', 'system'),
                'content': content,
                'injection_depth': item.get('injection_depth', 4),
                'injection_position': item.get('injection_position', 0),
                'injection_order': item.get('injection_order', 100),
            })

    # Resolve marker order — which card fields are enabled and in what sequence
    enabled_markers = []
    for mo in marker_order:
        mid = mo['identifier']
        if mo.get('enabled', False) and mid in MARKER_IDS:
            enabled_markers.append(mid)

    return preset, enabled_markers, enabled_custom_items


# ── Pipeline Builder ─────────────────────────────────────
def build_prompt_pipeline(char_path, preset_path=None, chat_history=None,
                          user_msg=None, user_name="Kurosaki Dat"):
    """
    Simulates SillyTavern's prepareOpenAIMessages + populateChatCompletion.
    When preset_path is provided, uses the Chat Completion Preset to determine
    which prompts are active and their assembly order.
    Returns the assembled messages[] array and diagnostic metadata.
    """
    raw = load_json(char_path)
    char = raw.get('data', raw)  # V3 uses 'data' wrapper, fallback for V2

    char_name = char.get('name', 'Character')

    # ── Collect all text for lorebook scanning ──
    all_chat_text = ""
    if chat_history:
        all_chat_text = " ".join([m.get('content', '') for m in chat_history])
    if user_msg:
        all_chat_text += " " + user_msg

    messages = []
    diagnostics = {
        'char_name': char_name,
        'user_name': user_name,
        'total_messages': 0,
        'total_tokens_est': 0,
        'lorebook_triggered': [],
        'preset_items': [],
        'sections': []
    }

    # ── Load Preset if provided ──
    preset = None
    enabled_markers = None
    custom_items = []
    preset_settings = {}
    if preset_path:
        preset, enabled_markers, custom_items = load_preset(
            preset_path, char, char_name, user_name
        )
        preset_settings = {
            'temperature': preset.get('temperature', 1),
            'top_p': preset.get('top_p', 0.92),
            'top_k': preset.get('top_k', 0),
            'max_tokens': preset.get('openai_max_tokens', 8192),
            'model': preset.get('openrouter_model', ''),
            'personality_format': preset.get('personality_format', '{{personality}}'),
            'scenario_format': preset.get('scenario_format', '{{scenario}}'),
        }
        diagnostics['preset_name'] = os.path.basename(preset_path)
        diagnostics['preset_settings'] = preset_settings
        for ci in custom_items:
            diagnostics['preset_items'].append({
                'name': ci['name'],
                'role': ci['role'],
                'depth': ci['injection_depth'],
                'tokens_est': estimate_tokens(ci['content']),
            })

    # ══════════════════════════════════════════════════════
    # ASSEMBLY: Build system prompt following marker order
    # ══════════════════════════════════════════════════════
    # When preset is loaded, we follow the marker order to interleave:
    #   custom preset items + card fields (description, personality, etc.)
    # When no preset, we use the old simple approach.

    if enabled_markers:
        # ── WITH PRESET: Follow prompt_order markers ──
        system_parts = []

        # Separate custom items by injection_depth for proper placement
        # depth=4 items go into the main system prompt
        # depth=1 or depth=0 items go near the end (close to chat)
        depth4_items = [ci for ci in custom_items if ci['injection_depth'] >= 4]
        depth1_items = [ci for ci in custom_items if ci['injection_depth'] == 1]
        depth0_items = [ci for ci in custom_items if ci['injection_depth'] == 0]

        # Inject depth-4 custom items BEFORE markers (they form the "Celia persona" layer)
        for ci in depth4_items:
            content = replace_macros(ci['content'], char_name, user_name)
            label = f"preset: {ci['name']}"
            system_parts.append((label, content, ci['role']))
            diagnostics['sections'].append({
                'label': label,
                'tokens_est': estimate_tokens(content),
                'char_count': len(content)
            })

        # Now process markers in their configured order
        for marker in enabled_markers:
            if marker == 'main':
                # Main prompt from card (system_prompt field)
                if char.get('system_prompt'):
                    sp = replace_macros(char['system_prompt'], char_name, user_name)
                    # Check if preset forbids override
                    main_item = None
                    for p in (preset or {}).get('prompts', []):
                        if p.get('identifier') == 'main':
                            main_item = p
                            break
                    if main_item and not main_item.get('forbid_overrides', False):
                        system_parts.append(('system_prompt (card)', sp, 'system'))
                        diagnostics['sections'].append({
                            'label': 'system_prompt (card)',
                            'tokens_est': estimate_tokens(sp),
                            'char_count': len(sp)
                        })

            elif marker == 'charDescription':
                if char.get('description'):
                    desc = replace_macros(char['description'], char_name, user_name)
                    system_parts.append(('charDescription', desc, 'system'))
                    diagnostics['sections'].append({
                        'label': 'charDescription',
                        'tokens_est': estimate_tokens(desc),
                        'char_count': len(desc)
                    })

            elif marker == 'charPersonality':
                if char.get('personality'):
                    fmt = preset_settings.get('personality_format', '{{personality}}')
                    pers = replace_macros(fmt, char_name, user_name)
                    pers = pers.replace('{{personality}}', char.get('personality', ''))
                    system_parts.append(('charPersonality', pers, 'system'))
                    diagnostics['sections'].append({
                        'label': 'charPersonality',
                        'tokens_est': estimate_tokens(pers),
                        'char_count': len(pers)
                    })

            elif marker == 'scenario':
                if char.get('scenario'):
                    fmt = preset_settings.get('scenario_format', '{{scenario}}')
                    scen = replace_macros(fmt, char_name, user_name)
                    scen = scen.replace('{{scenario}}', char.get('scenario', ''))
                    system_parts.append(('scenario', scen, 'system'))
                    diagnostics['sections'].append({
                        'label': 'scenario',
                        'tokens_est': estimate_tokens(scen),
                        'char_count': len(scen)
                    })

            elif marker == 'nsfw':
                pass  # Usually empty or handled by custom items

            elif marker == 'jailbreak':
                pass  # Usually empty or handled by custom items

            elif marker == 'worldInfoBefore' or marker == 'worldInfoAfter':
                pass  # Handled in lorebook stage below

            elif marker == 'dialogueExamples':
                pass  # Handled in mes_example stage below

            elif marker == 'chatHistory':
                pass  # Handled in chat history stage below

        # Build the main system message from all parts
        sys_role_groups = {}  # group by role
        for label, content, role in system_parts:
            if role not in sys_role_groups:
                sys_role_groups[role] = []
            sys_role_groups[role].append(content)

        # System role items get merged into one big system message
        if 'system' in sys_role_groups:
            system_content = "\n\n".join(sys_role_groups['system'])
            messages.append({"role": "system", "content": system_content})

        # Assistant role items (like prefill) go separately
        if 'assistant' in sys_role_groups:
            for content in sys_role_groups['assistant']:
                messages.append({
                    "role": "assistant",
                    "content": content,
                    "_meta": {"type": "preset_prefill"}
                })

    else:
        # ── WITHOUT PRESET: Simple card-only assembly ──
        system_parts = []

        if char.get('system_prompt'):
            sp = replace_macros(char['system_prompt'], char_name, user_name)
            system_parts.append(('system_prompt (card)', sp))

        if char.get('description'):
            desc = replace_macros(char['description'], char_name, user_name)
            system_parts.append(('description', desc))

        if char.get('personality'):
            pers = replace_macros(char['personality'], char_name, user_name)
            system_parts.append(('personality', pers))

        if char.get('scenario'):
            scen = replace_macros(char['scenario'], char_name, user_name)
            system_parts.append(('scenario', scen))

        system_content = "\n\n".join([part[1] for part in system_parts])
        messages.append({"role": "system", "content": system_content})

        for label, content in system_parts:
            diagnostics['sections'].append({
                'label': label,
                'tokens_est': estimate_tokens(content),
                'char_count': len(content)
            })

    # ══════════════════════════════════════════════════════
    # STAGE 2: Lorebook / World Info Entries
    # ══════════════════════════════════════════════════════
    lorebook = char.get('character_book', {})
    entries = lorebook.get('entries', [])

    if entries:
        triggered = trigger_lorebook(entries, all_chat_text, char_name, user_name)
        triggered.sort(key=lambda e: e.get('insertion_order', 0))

        for entry in triggered:
            content = replace_macros(entry.get('content', ''), char_name, user_name)
            comment = entry.get('comment', f"Entry #{entry.get('id', '?')}")
            position = entry.get('position', 'after_char')
            ext = entry.get('extensions', {})
            depth = ext.get('depth', 4)

            diagnostics['lorebook_triggered'].append({
                'comment': comment,
                'keys': entry.get('keys', []),
                'position': position,
                'depth': depth,
                'tokens_est': estimate_tokens(content)
            })

            messages.append({
                "role": "system",
                "content": f"[Lorebook: {comment}]\n{content}",
                "_meta": {"type": "lorebook", "depth": depth, "position": position}
            })

    # ══════════════════════════════════════════════════════
    # STAGE 3: Example Messages (mes_example)
    # ══════════════════════════════════════════════════════
    if char.get('mes_example'):
        examples = replace_macros(char['mes_example'], char_name, user_name)
        diagnostics['sections'].append({
            'label': 'mes_example',
            'tokens_est': estimate_tokens(examples),
            'char_count': len(examples)
        })

    # ══════════════════════════════════════════════════════
    # STAGE 4: Depth Prompt (from card extensions)
    # ══════════════════════════════════════════════════════
    depth_prompt = char.get('extensions', {}).get('depth_prompt', {})
    if depth_prompt and depth_prompt.get('prompt'):
        dp_content = replace_macros(depth_prompt['prompt'], char_name, user_name)
        dp_depth = depth_prompt.get('depth', 4)
        dp_role = depth_prompt.get('role', 'system')

        diagnostics['sections'].append({
            'label': f'depth_prompt (depth={dp_depth})',
            'tokens_est': estimate_tokens(dp_content),
            'char_count': len(dp_content)
        })

        messages.append({
            "role": dp_role,
            "content": dp_content,
            "_meta": {"type": "depth_prompt", "depth": dp_depth}
        })

    # ══════════════════════════════════════════════════════
    # STAGE 5: Depth-1 Preset Items (near chat, e.g. word count, COT)
    # ══════════════════════════════════════════════════════
    if preset_path:
        for ci in depth1_items:
            content = replace_macros(ci['content'], char_name, user_name)
            messages.append({
                "role": ci['role'],
                "content": content,
                "_meta": {"type": "preset_depth1", "name": ci['name'], "depth": 1}
            })

    # ══════════════════════════════════════════════════════
    # STAGE 6: Chat History
    # ══════════════════════════════════════════════════════
    if chat_history:
        for msg in chat_history:
            role = msg.get('role', 'user')
            content = replace_macros(msg.get('content', ''), char_name, user_name)
            messages.append({"role": role, "content": content})

    # ══════════════════════════════════════════════════════
    # STAGE 7: Current User Message (with post-history injection)
    # ══════════════════════════════════════════════════════
    if user_msg:
        resolved_msg = replace_macros(user_msg, char_name, user_name)

        # Post-history instructions (from card)
        post_hist = char.get('post_history_instructions', '')
        if post_hist:
            post_hist = replace_macros(post_hist, char_name, user_name)
            resolved_msg += f"\n\n{post_hist}"
            diagnostics['sections'].append({
                'label': 'post_history_instructions (depth=0)',
                'tokens_est': estimate_tokens(post_hist),
                'char_count': len(post_hist)
            })

        messages.append({"role": "user", "content": resolved_msg})
    elif not chat_history:
        first_mes = char.get('first_mes', '')
        if first_mes:
            first_mes = replace_macros(first_mes, char_name, user_name)
            messages.append({"role": "assistant", "content": first_mes})

    # ══════════════════════════════════════════════════════
    # STAGE 8: Depth-0 Preset Items (after user msg, e.g. dice rolls)
    # ══════════════════════════════════════════════════════
    if preset_path:
        for ci in depth0_items:
            content = replace_macros(ci['content'], char_name, user_name)
            messages.append({
                "role": ci['role'],
                "content": content,
                "_meta": {"type": "preset_depth0", "name": ci['name'], "depth": 0}
            })

    # ── Prefill: assistant message from preset (if any) ──
    # The prefill is already added in the system assembly stage above

    # ── Compute totals ──
    total_tokens = 0
    for msg in messages:
        total_tokens += estimate_tokens(msg['content'])

    diagnostics['total_messages'] = len(messages)
    diagnostics['total_tokens_est'] = total_tokens

    return messages, diagnostics


# ── Display ──────────────────────────────────────────────
def display_results(messages, diagnostics, verbose=False):
    """Pretty-print the assembled prompt pipeline."""
    
    print()
    print(c(C.BOLD + C.CYAN, "╔══════════════════════════════════════════════════════════╗"))
    print(c(C.BOLD + C.CYAN, "║     SILLYTAVERN PROMPT PIPELINE TESTER                  ║"))
    print(c(C.BOLD + C.CYAN, "╚══════════════════════════════════════════════════════════╝"))
    print()
    
    # ── Summary ──
    print(c(C.BOLD + C.WHITE, "📋 SUMMARY"))
    print(c(C.DIM, "─" * 58))
    print(f"  Character:     {c(C.GREEN, diagnostics['char_name'])}")
    print(f"  User:          {c(C.GREEN, diagnostics['user_name'])}")
    print(f"  Messages:      {c(C.YELLOW, str(diagnostics['total_messages']))}")
    print(f"  Est. Tokens:   {c(C.YELLOW, str(diagnostics['total_tokens_est']))}")
    if diagnostics.get('preset_name'):
        print(f"  Preset:        {c(C.MAGENTA, diagnostics['preset_name'])}")
    print()

    # ── Preset Settings ──
    if diagnostics.get('preset_settings'):
        ps = diagnostics['preset_settings']
        print(c(C.BOLD + C.WHITE, "⚙️  PRESET SETTINGS"))
        print(c(C.DIM, "─" * 58))
        print(f"  Temperature:   {c(C.CYAN, str(ps.get('temperature', '?')))}")
        print(f"  Top-P:         {c(C.CYAN, str(ps.get('top_p', '?')))}")
        print(f"  Max Tokens:    {c(C.CYAN, str(ps.get('max_tokens', '?')))}")
        if ps.get('model'):
            print(f"  Model:         {c(C.CYAN, ps['model'])}")
        print()

    # ── Preset Custom Items ──
    if diagnostics.get('preset_items'):
        print(c(C.BOLD + C.WHITE, "🎭 PRESET PROMPT ITEMS (enabled)"))
        print(c(C.DIM, "─" * 58))
        for pi in diagnostics['preset_items']:
            role_c = C.CYAN if pi['role'] == 'system' else C.GREEN if pi['role'] == 'user' else C.YELLOW
            print(f"  {c(role_c, '●')} {pi['name']:35s} [{pi['role']:9s}]  depth={pi['depth']}  ~{pi['tokens_est']} tok")
        print()

    # ── Token Breakdown ──
    if verbose and diagnostics['sections']:
        print(c(C.BOLD + C.WHITE, "📊 TOKEN BREAKDOWN"))
        print(c(C.DIM, "─" * 58))
        for sec in diagnostics['sections']:
            bar_len = min(40, sec['tokens_est'] // 20)
            bar = "█" * bar_len
            print(f"  {sec['label']:40s} {c(C.YELLOW, str(sec['tokens_est']).rjust(6))} tok  {c(C.BLUE, bar)}")
        print()

    # ── Lorebook ──
    if diagnostics['lorebook_triggered']:
        print(c(C.BOLD + C.WHITE, "📚 LOREBOOK ENTRIES TRIGGERED"))
        print(c(C.DIM, "─" * 58))
        for lb in diagnostics['lorebook_triggered']:
            keys_str = ", ".join(lb['keys'][:3])
            print(f"  {c(C.MAGENTA, '●')} {c(C.WHITE, lb['comment']):30s}  keys=[{keys_str}]  depth={lb['depth']}  ~{lb['tokens_est']} tok")
        print()
    else:
        print(c(C.DIM, "  (No lorebook entries triggered)"))
        print()
    
    # ── Messages Array ──
    print(c(C.BOLD + C.WHITE, "💬 MESSAGES ARRAY (what the model receives)"))
    print(c(C.DIM, "═" * 58))
    
    role_colors = {
        'system': C.CYAN,
        'user': C.GREEN,
        'assistant': C.YELLOW
    }
    
    for i, msg in enumerate(messages):
        role = msg['role']
        color = role_colors.get(role, C.WHITE)
        meta = msg.get('_meta', {})
        meta_str = ""
        if meta:
            meta_str = f" {c(C.DIM, str(meta))}"
        
        tokens = estimate_tokens(msg['content'])
        
        print()
        print(c(C.BOLD + color, f"┌─ Message {i} [{role.upper()}] ") + c(C.DIM, f"(~{tokens} tokens)") + meta_str)
        print(c(color, "│"))
        
        # Show content (truncated for readability)
        lines = msg['content'].split('\n')
        max_lines = 30 if not meta else 10
        for j, line in enumerate(lines[:max_lines]):
            display_line = line[:120] + ("..." if len(line) > 120 else "")
            print(c(color, "│ ") + display_line)
        
        if len(lines) > max_lines:
            print(c(C.DIM, f"│ ... ({len(lines) - max_lines} more lines)"))
        
        print(c(color, "└" + "─" * 57))
    
    print()
    print(c(C.BOLD + C.CYAN, "═" * 58))
    print(c(C.DIM, f"  Generated at {datetime.now().isoformat()}"))
    print()


# ── OpenRouter API ───────────────────────────────────────
def send_to_openrouter(messages, model="arcee-ai/trinity-large-preview:free",
                       temperature=1.0, max_tokens=8192, top_p=0.92):
    """
    Send the assembled messages to OpenRouter API and stream the response.
    Uses only stdlib (urllib) — no pip dependencies.
    """
    api_key = os.environ.get('OPEN_ROUTER_API_KEY', '')
    if not api_key:
        print(c(C.RED, "❌ OPEN_ROUTER_API_KEY not found. Set it in .env or environment."))
        return None

    # Clean messages: strip _meta
    clean = [{"role": m["role"], "content": m["content"]} for m in messages]

    payload = {
        "messages": clean,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "stream": False,  # use non-streaming for simplicity in urllib
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://lnd-studio.local",
        "X-Title": "LND ST Prompt Tester",
    }

    print()
    print(c(C.BOLD + C.MAGENTA, "╔══════════════════════════════════════════════════════════╗"))
    print(c(C.BOLD + C.MAGENTA, "║     SENDING TO OPENROUTER API                           ║"))
    print(c(C.BOLD + C.MAGENTA, "╚══════════════════════════════════════════════════════════╝"))
    print(f"  Model:  {c(C.GREEN, model)}")
    print(f"  Temp:   {temperature}  |  Top-P: {top_p}  |  Max: {max_tokens}")
    print(c(C.DIM, "  Sending request..."))
    print()

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=data,
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='replace')
        print(c(C.RED, f"❌ API Error {e.code}: {error_body[:500]}"))
        return None
    except Exception as e:
        print(c(C.RED, f"❌ Request failed: {e}"))
        return None

    # ── Display Response ──
    choice = body.get('choices', [{}])[0]
    content = choice.get('message', {}).get('content', '(empty response)')
    finish = choice.get('finish_reason', '?')
    usage = body.get('usage', {})

    print(c(C.BOLD + C.YELLOW, "┌─ ASSISTANT RESPONSE ─────────────────────────────────────"))
    print()
    if has_rich:
        console = Console()
        md = Markdown(content)
        console.print(md)
    else:
        for line in content.split('\n'):
            print(c(C.YELLOW, "│ ") + line)
    print()
    print(c(C.BOLD + C.YELLOW, "└" + "─" * 57))
    print()

    # ── Usage Stats ──
    print(c(C.BOLD + C.WHITE, "📊 API USAGE"))
    print(c(C.DIM, "─" * 58))
    print(f"  Prompt tokens:      {c(C.CYAN, str(usage.get('prompt_tokens', 0)))}")
    print(f"  Completion tokens:  {c(C.CYAN, str(usage.get('completion_tokens', 0)))}")
    print(f"  Total tokens:       {c(C.CYAN, str(usage.get('total_tokens', 0)))}")
    finish_c = C.GREEN if finish == 'stop' else C.RED
    print(f"  Finish reason:      {c(finish_c, finish)}")
    cost = usage.get('cost', 0)
    if cost:
        print(f"  Cost:              ${cost:.6f}")
    print()

    return body


# ── Main ─────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="SillyTavern Prompt Pipeline Tester — inspect the messages[] sent to AI",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("char_card", help="Path to character card JSON (V2 or V3)")
    parser.add_argument("--preset", "-p", help="Path to Chat Completion Preset JSON")
    parser.add_argument("--chat", help="Path to mock chat history JSON (array of {role, content})")
    parser.add_argument("--user-msg", "-m", help="Single user message to test with")
    parser.add_argument("--user-name", "-u", default="Kurosaki Dat", help="User's display name")
    parser.add_argument("--output", "-o", help="Write assembled payload to JSON file")
    parser.add_argument("--send", "-s", action="store_true", help="Send payload to OpenRouter API")
    parser.add_argument("--model", default=None,
                       help="Model to use with --send (default: from preset or arcee-ai/trinity-large-preview:free)")
    parser.add_argument("--temperature", "-t", type=float, default=None, help="Temperature (default: from preset or 1.0)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show token breakdown")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--greeting", "-g", type=int, default=None,
                       help="Use alternate greeting N (0=first_mes, 1+=alternate_greetings index)")
    
    args = parser.parse_args()
    
    global NO_COLOR
    NO_COLOR = args.no_color
    
    # Load .env
    env_path = load_env()
    if env_path and args.verbose:
        print(c(C.DIM, f"  Loaded env from: {env_path}"))
    
    # Load chat history
    chat_history = None
    if args.chat:
        chat_history = load_json(args.chat)
    
    # Default user message if none provided
    user_msg = args.user_msg
    if not user_msg and not chat_history:
        user_msg = None  # Will use first_mes as greeting instead
    
    # ── Resolve preset path ──
    preset_path = args.preset

    # Build the pipeline
    messages, diagnostics = build_prompt_pipeline(
        char_path=args.char_card,
        preset_path=preset_path,
        chat_history=chat_history,
        user_msg=user_msg,
        user_name=args.user_name
    )

    # Resolve model/temperature: CLI flag > preset > default
    ps = diagnostics.get('preset_settings', {})
    effective_model = args.model or ps.get('model') or 'arcee-ai/trinity-large-preview:free'
    effective_temp = args.temperature if args.temperature is not None else ps.get('temperature', 1.0)
    effective_top_p = ps.get('top_p', 0.92)
    effective_max_tokens = ps.get('max_tokens', 8192)

    # Display
    display_results(messages, diagnostics, verbose=args.verbose)

    # Save output
    if args.output:
        out_path = args.output
        if os.path.isdir(out_path):
            out_path = os.path.join(out_path, "payload.json")
        os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)

        clean_messages = [{"role": m["role"], "content": m["content"]} for m in messages]
        payload = {
            "messages": clean_messages,
            "model": effective_model,
            "temperature": effective_temp,
            "max_tokens": effective_max_tokens,
            "top_p": effective_top_p,
            "_diagnostics": diagnostics
        }
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(c(C.GREEN, f"✅ Payload saved to {out_path}"))

    # Send to API
    if args.send:
        response = send_to_openrouter(
            messages,
            model=effective_model,
            temperature=effective_temp,
            max_tokens=effective_max_tokens,
            top_p=effective_top_p,
        )
        
        # Save response if output path specified
        if response and args.output:
            # Save raw JSON response
            resp_path_json = args.output
            if os.path.isdir(resp_path_json):
                resp_path_json = os.path.join(resp_path_json, "payload_response.json")
            else:
                base, ext = os.path.splitext(resp_path_json)
                resp_path_json = f"{base}_response.json"
            with open(resp_path_json, 'w', encoding='utf-8') as f:
                json.dump(response, f, ensure_ascii=False, indent=2)
            
            # Save markdown response
            content_text = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            if content_text:
                resp_path_md = os.path.join(os.path.dirname(resp_path_json) or '.', "response.md")
                with open(resp_path_md, 'w', encoding='utf-8') as f:
                    f.write(content_text)
                print(c(C.GREEN, f"✅ Assistant response saved to {resp_path_md}"))
            print(c(C.GREEN, f"✅ Response saved to {resp_path_json}"))


if __name__ == "__main__":
    main()
