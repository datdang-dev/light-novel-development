from pathlib import Path

class GateRegistry:
    """Registry to manage and evaluate pipeline gate predicates."""
    
    def __init__(self):
        self._gates = {}
        self.register_default_gates()

    def register(self, name: str, predicate_fn):
        """Register a new gate predicate function."""
        self._gates[name] = predicate_fn

    def check(self, name: str | None, state: dict) -> tuple[bool, str]:
        """Check if the gate is satisfied against the state."""
        if name is None:
            return True, "No gate required"
            
        predicate = self._gates.get(name)
        if predicate is None:
            return True, f"Unknown gate '{name}' — allowing (permissive)"
            
        try:
            return predicate(state)
        except Exception as e:
            return False, f"Gate evaluation error for '{name}': {e}"

    def register_default_gates(self):
        """Register standard out-of-the-box gates."""
        
        def get_current_forensic_data(state: dict) -> dict | None:
            run_dir = Path(state["run_dir"])
            forensics_dir = run_dir / "_forensics"
            pages = state.get("pages", [])
            if not pages:
                return None
            page_idx = state.get("current_page_index", 0)
            if page_idx >= len(pages):
                return None
            page_num = pages[page_idx]
            expected = forensics_dir / f"{page_num:03d}_forensics.md"
            if not expected.exists():
                return None
            try:
                import re, json
                content = expected.read_text(encoding="utf-8").strip()
                json_str = content
                if "```json" in content:
                    match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
                    if match:
                        json_str = match.group(1)
                elif "```" in content:
                    match = re.search(r"```\s*(.*?)\s*```", content, re.DOTALL)
                    if match:
                        json_str = match.group(1)
                return json.loads(json_str)
            except Exception:
                return None

        def check_forensic_complete(state: dict) -> tuple[bool, str]:
            run_dir = Path(state["run_dir"])
            forensics_dir = run_dir / "_forensics"
            if not forensics_dir.exists():
                return False, f"Forensics directory not found: {forensics_dir}"
            
            pages = state.get("pages", [])
            if pages:
                page_idx = state.get("current_page_index", 0)
                if page_idx < len(pages):
                    page_num = pages[page_idx]
                    expected = forensics_dir / f"{page_num:03d}_forensics.md"
                    if not expected.exists():
                        return False, f"Missing forensic report: {expected.name}. Run forensic analysis first."
                    
                    # Hard-enforce evidence ledger, interactions, and grounding ratio gates
                    data = get_current_forensic_data(state)
                    if data is None:
                        return False, f"Failed to load/parse forensic data for page {page_num:03d}."
                        
                    # 1. INTERACTION_GATE validation
                    explicit = data.get("explicit_elements", {})
                    acts = explicit.get("acts", [])
                    interactions = data.get("interactions", [])
                    if acts and not interactions:
                        return False, f"INTERACTION_GATE violation: explicit acts are present, but interactions list is empty on page {page_num:03d}."
                    
                    for idx, inter in enumerate(interactions):
                        if not isinstance(inter, dict):
                            return False, f"INTERACTION_GATE violation: interaction {idx} must be a dictionary object on page {page_num:03d}."
                        sensory_tags = inter.get("sensory_tags", [])
                        if not isinstance(sensory_tags, list) or len(sensory_tags) < 2:
                            return False, f"INTERACTION_GATE violation: interaction {idx} must have at least 2 sensory_tags (found {len(sensory_tags) if isinstance(sensory_tags, list) else 0}) on page {page_num:03d}."
                        
                    # 2. EVIDENCE_LEDGER dynamic min entries floor validation
                    ledger = data.get("evidence_ledger", [])
                    if not isinstance(ledger, list):
                        return False, f"evidence_ledger is missing or not a list on page {page_num:03d}."
                    
                    panels_count = len(data.get("panels", []))
                    char_count = len(data.get("characters_present", []))
                    min_required = 1 if (panels_count <= 1 and char_count <= 1) else 2
                    
                    if len(ledger) < min_required:
                        return False, f"Evidence ledger has {len(ledger)} entries, but scene complexity requires at least {min_required} on page {page_num:03d}."
                        
                    # 3. Grounding ratio validation (pixel_ratio >= 0.5)
                    if not ledger:
                        return False, f"Evidence ledger is empty on page {page_num:03d}."
                    pixel_or_inference_count = 0
                    for entry in ledger:
                        ev_type = entry.get("evidence_type", "")
                        if ev_type in ["pixel_grounded", "verified_inference"]:
                            pixel_or_inference_count += 1
                    ratio = pixel_or_inference_count / len(ledger)
                    if ratio < 0.5:
                        return False, f"Pixel-First grounding violation: Only {ratio*100:.1f}% of entries are pixel/inference (min 50% required) on page {page_num:03d}."
                        
            return True, "Forensic gate passed with complete grounding validation"

        def check_context_loaded(state: dict) -> tuple[bool, str]:
            if "context-loading" in state.get("steps_completed", []):
                return True, "Context loaded"
            return False, "Context loading step not completed"

        def check_prose_complete(state: dict) -> tuple[bool, str]:
            if "prose-generation" in state.get("steps_completed", []):
                return True, "Prose generated"
            return False, "Prose generation step not completed"

        def check_audit_pass(state: dict) -> tuple[bool, str]:
            if "quality-audit" in state.get("steps_completed", []):
                return True, "Audit passed"
            return False, "Quality audit not completed or not passed"

        self.register("forensic_complete", check_forensic_complete)
        self.register("context_loaded", check_context_loaded)
        self.register("prose_complete", check_prose_complete)
        self.register("audit_pass", check_audit_pass)
