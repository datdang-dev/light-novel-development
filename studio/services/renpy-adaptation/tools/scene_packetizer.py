#!/usr/bin/env python3
import sys
import json
import os
import argparse
from typing import Dict, List, Any, Optional

# Add project root and local service directory to sys.path to resolve internal modules
script_dir = os.path.dirname(os.path.abspath(__file__))
service_dir = os.path.abspath(os.path.join(script_dir, ".."))
project_root = os.path.abspath(os.path.join(script_dir, "../../../.."))
if service_dir not in sys.path:
    sys.path.insert(0, service_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class ScenePacketizer:
    """Chunks a compiled linear screenplay JSON into context-complete, token-bounded scene packets."""
    
    def __init__(self, screenplay_path: str, max_dialogue_lines: int = 20):
        self.screenplay_path = screenplay_path
        self.max_dialogue_lines = max_dialogue_lines
        
    def load_screenplay(self) -> Dict[str, Any]:
        if not os.path.exists(self.screenplay_path):
            raise FileNotFoundError(f"Screenplay file not found: {self.screenplay_path}")
        with open(self.screenplay_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def packetize(self) -> List[Dict[str, Any]]:
        data = self.load_screenplay()
        elements = data.get("screenplay", [])
        metadata = data.get("metadata", {})
        
        packets = []
        current_packet_elements = []
        dialogue_count = 0
        packet_idx = 1
        
        # Cumulative contextual state trackers
        current_bg = None
        current_bg_effects = None
        present_characters = {}  # char_name -> expression
        current_music = None
        
        for elem in elements:
            elem_type = elem.get("type")
            
            # Maintain active environmental states
            if elem_type == "scene":
                current_bg = elem.get("value")
                current_bg_effects = elem.get("effects")
                # Clearing background usually clears present sprites in Ren'Py
                present_characters = {}
                
            elif elem_type == "show":
                char = elem.get("character")
                expr = elem.get("expression")
                if char:
                    present_characters[char] = expr or "neutral"
                    
            elif elem_type == "play_music":
                current_music = elem.get("value")
                
            elif elem_type == "stop_audio" and elem.get("channel") == "music":
                current_music = None
            
            # Decide if we need to chunk *before* adding the next element
            # A new 'scene' change is a natural boundary to start a new packet
            if elem_type == "scene" and current_packet_elements:
                packets.append(self._create_packet(
                    packet_idx, current_packet_elements, current_bg, 
                    current_bg_effects, present_characters, current_music, metadata
                ))
                packet_idx += 1
                current_packet_elements = []
                dialogue_count = 0
                
            current_packet_elements.append(elem)
            if elem_type == "dialogue":
                dialogue_count += 1
                
            # If dialogue limit reached, chunk now
            if dialogue_count >= self.max_dialogue_lines:
                packets.append(self._create_packet(
                    packet_idx, current_packet_elements, current_bg, 
                    current_bg_effects, present_characters, current_music, metadata
                ))
                packet_idx += 1
                current_packet_elements = []
                dialogue_count = 0
                
        # Append trailing elements
        if current_packet_elements:
            packets.append(self._create_packet(
                packet_idx, current_packet_elements, current_bg, 
                current_bg_effects, present_characters, current_music, metadata
            ))
            
        print(f"SUCCESS: Packetization complete! Generated {len(packets)} packets from {len(elements)} elements.")
        return packets
        
    def _create_packet(self, idx: int, elements: List[Dict[str, Any]], bg: Optional[str], 
                       bg_effects: Optional[str], chars: Dict[str, str], 
                       music: Optional[str], metadata: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "packet_id": f"packet_{idx:03d}",
            "context_state": {
                "active_background": bg,
                "active_background_effects": bg_effects,
                "present_characters": chars.copy(),
                "active_music": music
            },
            "elements": elements,
            "metadata": metadata
        }
        
    def save_packets(self, packets: List[Dict[str, Any]], output_dir: str, start_label: str) -> List[str]:
        os.makedirs(output_dir, exist_ok=True)
        paths = []
        for p in packets:
            packet_id = p["packet_id"]
            filename = f"playthrough_{start_label}_{packet_id}.json"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding='utf-8') as f:
                json.dump(p, f, indent=2, ensure_ascii=False)
            paths.append(filepath)
        print(f"Saved {len(packets)} scene packets to: {output_dir}")
        return paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Linear Screenplay Scene Chunker and Packetizer")
    parser.add_argument("--screenplay-path", required=True, help="Path to playthrough screenplay.json")
    parser.add_argument("--output-dir", required=True, help="Directory to save scene packet files")
    parser.add_argument("--max-dialogue", type=int, default=20, help="Maximum dialogue lines per packet")
    
    args = parser.parse_args()
    
    # Extract start_label from screenplay filename or defaults
    basename = os.path.basename(args.screenplay_path)
    start_label = "start"
    if "playthrough_" in basename and "_screenplay.json" in basename:
        start_label = basename.replace("playthrough_", "").replace("_screenplay.json", "")
        
    packetizer = ScenePacketizer(args.screenplay_path, max_dialogue_lines=args.max_dialogue)
    try:
        packets = packetizer.packetize()
        packetizer.save_packets(packets, args.output_dir, start_label)
    except Exception as e:
        print(f"Packetization Failed: {e}", file=sys.stderr)
        sys.exit(1)
