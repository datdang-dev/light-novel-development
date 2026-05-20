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

from tools.scene_packetizer import ScenePacketizer
from tools.verify_sensory_density import SensoryDensityValidator

class SukiRikoOrchestrator:
    """Manages the structured synthesis-audit loop of Suki (drafting) and Riko (auditing)."""
    
    def __init__(self, max_retries: int = 3, mock: bool = False):
        self.max_retries = max_retries
        self.mock = mock
        self.validator = SensoryDensityValidator()
        self.attempt_counts = {}  # packet_id -> attempt count

    def suki_synthesize(self, packet: Dict[str, Any], attempt: int, critique: Optional[List[str]] = None) -> str:
        """Call Suki (lewd-writer) to generate R18 Vietnamese prose for a screenplay packet."""
        packet_id = packet["packet_id"]
        
        if self.mock:
            # Mock LLM generation logic
            if attempt == 1:
                # Intentionally weak, slop draft for showing the retry loop in action
                prose = (
                    f"### Chapter Draft for {packet_id}\n\n"
                    "Asuka nhìn tôi đầy thách thức. Tôi cảm thấy không thể cưỡng lại vẻ đẹp của cô ấy, "
                    "một sự pha trộn giữa kiêu kỳ và bí ẩn. Khoảnh khắc định mệnh này làm tôi vừa sợ hãi vừa "
                    "tò mò. Chúng tôi đi lên sân thượng trường học để nói chuyện."
                )
            else:
                # Sensory-rich premium draft on retry or subsequent attempts
                prose = (
                    f"### Chapter Draft for {packet_id} (Sensory Upgraded)\n\n"
                    "Trên sân thượng lộng gió, hơi thở Asuka dốc lên từng nhịp gấp gáp đầy kích thích. "
                    "Làn da nóng ran của nàng áp sát vào lồng ngực tôi, khít khao và ẩm ướt. "
                    "Nàng khẽ rùng mình, tiếng rên rỉ khẽ khàng lọt ra từ đôi môi ngọt ngào ấy. "
                    "Da thịt chạm nhau tỏa ra hơi ấm nồng nàn khiến nhịp tim cả hai cùng giật bắn thổn thức."
                )
            print(f"[SUKI MOCK] Generated prose draft for {packet_id} (Attempt {attempt})")
            return prose
        else:
            # Under a real setup, Suki would execute standard LLM API call using prompt engineering
            raise NotImplementedError("Real Suki API orchestration requires active MCP Agent bridge runtime.")

    def riko_audit(self, prose_content: str) -> Dict[str, Any]:
        """Call Riko (gooner-editor) to audit the generated Vietnamese R18 chapter."""
        # Check sensory density first
        report = self.validator.verify_prose(prose_content)
        
        # In mock mode, we align Riko's audit score directly with sensory density
        score = report["sensory_score"]
        passed = report["passed"]
        
        return {
            "score": score,
            "passed": passed,
            "critique": report["critique"]
        }

    def orchestrate_packet(self, packet: Dict[str, Any]) -> str:
        """Runs the synthesis-audit loop on a single packet."""
        packet_id = packet["packet_id"]
        self.attempt_counts[packet_id] = 0
        
        # Pre-check screenplay sensory density
        pre_report = self.validator.verify_screenplay_packet(packet)
        print(f"[ORCHESTRATOR] Pre-validation score for {packet_id}: {pre_report['sensory_score']}/100")
        if not pre_report["passed"]:
            print(f"[WARNING] Screenplay {packet_id} has extremely low sensory density. Visual hooks: {pre_report['visual_count']}")
            
        critique = None
        for attempt in range(1, self.max_retries + 1):
            self.attempt_counts[packet_id] = attempt
            print(f"\n--- {packet_id}: Synthesis-Audit Loop (Attempt {attempt}/{self.max_retries}) ---")
            
            # Suki Writes
            prose = self.suki_synthesize(packet, attempt, critique)
            
            # Riko Audits
            audit_report = self.riko_audit(prose)
            print(f"[RIKO AUDIT] Score: {audit_report['score']}/100 | Passed: {audit_report['passed']}")
            
            if audit_report["passed"]:
                print(f"[SUCCESS] {packet_id} approved after {attempt} attempts!")
                return prose
            
            critique = audit_report["critique"]
            print(f"[REJECTED] Critique for {packet_id}: {critique}")
            
        # If we exit loop without passing
        raise RuntimeError(f"Multi-Agent loop failed for {packet_id} after {self.max_retries} attempts. Last critique: {critique}")

    def run_pipeline(self, screenplay_path: str, output_dir: str) -> List[str]:
        """Runs the full novelization pipeline over a compiled screenplay."""
        # 1. Packetize
        basename = os.path.basename(screenplay_path)
        start_label = "start"
        if "playthrough_" in basename and "_screenplay.json" in basename:
            start_label = basename.replace("playthrough_", "").replace("_screenplay.json", "")
            
        packetizer = ScenePacketizer(screenplay_path)
        packets = packetizer.packetize()
        
        os.makedirs(output_dir, exist_ok=True)
        final_chapters = []
        
        for packet in packets:
            approved_prose = self.orchestrate_packet(packet)
            
            packet_id = packet["packet_id"]
            filename = f"playthrough_{start_label}_{packet_id}_draft.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(approved_prose)
            final_chapters.append(filepath)
            
        print(f"\nSUCCESS: Entire novelization pipeline completed! Saved draft files: {final_chapters}")
        return final_chapters

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LND Multi-Agent Playthrough Novelization Pipeline Orchestrator")
    parser.add_argument("--screenplay-path", required=True, help="Path to compiled linear screenplay JSON")
    parser.add_argument("--output-dir", required=True, help="Directory to save final approved chapters")
    parser.add_argument("--mock", action="store_true", help="Run with mock Suki and Riko agents")
    parser.add_argument("--max-retries", type=int, default=3, help="Maximum Suki synthesis retries on Riko audit failure")
    
    args = parser.parse_args()
    
    orchestrator = SukiRikoOrchestrator(max_retries=args.max_retries, mock=args.mock)
    try:
        orchestrator.run_pipeline(args.screenplay_path, args.output_dir)
    except Exception as e:
        print(f"Pipeline Orchestration Failed: {e}", file=sys.stderr)
        sys.exit(1)
