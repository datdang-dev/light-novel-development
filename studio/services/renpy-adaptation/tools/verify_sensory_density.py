#!/usr/bin/env python3
import sys
import json
import os
import re
import argparse
from typing import Dict, List, Any, Tuple

class SensoryDensityValidator:
    """Validator that checks screenplay JSON or written prose drafts for strict LND sensory density guidelines."""
    
    def __init__(self):
        # Vietnamese R18 sensory keywords
        self.k_sensory = [
            "hơi thở", "nhịp tim", "giật bắn", "thở dốc", "run rẩy", "ẩm ướt", "nóng ran", 
            "rùng mình", "mồ hôi", "da thịt", "siết chặt", "rên", "căng", "khít", 
            "nước", "môi", "lưỡi", "ngực", "đùi", "eo", "mông", "nhấp", "giật", 
            "rên rỉ", "kích thích", "dịch nhầy", "ướt át", "hưng phấn", "nhạy cảm",
            "mơn trớn", "đút", "vào trong", "chạm", "ôm chặt", "nóng bừng"
        ]
        
        # Forbidden AI slop/cliché keywords in Vietnamese
        self.k_forbidden = [
            "hỗn hợp giữa", "pha trộn giữa", "không thể cưỡng lại", 
            "như thể thời gian ngừng trôi", "bí ẩn và", "khó tả",
            "cảm xúc hỗn độn", "khoảnh khắc định mệnh", "vừa sợ hãi vừa"
        ]

    def verify_screenplay_packet(self, packet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify the pre-Suki screenplay packet for sufficient multimodal hooks."""
        elements = packet_data.get("elements", [])
        
        dialogue_count = 0
        visual_count = 0  # show, scene
        audio_count = 0   # play_music, play_sound, play_movie
        punch_count = 0   # vpunch, hpunch active dialogue
        
        for elem in elements:
            elem_type = elem.get("type")
            if elem_type == "dialogue":
                dialogue_count += 1
                if elem.get("vpunch"):
                    punch_count += 1
            elif elem_type in ("show", "scene"):
                visual_count += 1
            elif elem_type in ("play_music", "play_sound", "play_movie"):
                audio_count += 1
                
        # Scoring Logic (Max 100)
        # 1. Visual density (max 45 points)
        # Ideal: 1 visual cue per 2 dialogue lines (ratio >= 0.5)
        r_v = visual_count / max(1, dialogue_count)
        visual_score = min(45, int(r_v * 90))
        
        # 2. Audio density (max 35 points)
        # Ideal: at least 1-2 audio cues per packet (ratio >= 0.1)
        r_a = audio_count / max(1, dialogue_count)
        audio_score = min(25, int(r_a * 250))
        if audio_count > 0:
            audio_score += 10 # 10 pts bonus for having at least 1 sound trigger
            
        # 3. Punch density (max 20 points)
        # Having at least one vpunch/hpunch shock trigger
        punch_score = 20 if punch_count > 0 else 0
        
        total_score = visual_score + audio_score + punch_score
        
        # Default high score for purely narrative-less action packets
        if dialogue_count == 0 and len(elements) > 0:
            total_score = 90
            
        passed = total_score >= 35 # Screenplay gate is light, just ensuring *some* hooks exist
        
        return {
            "type": "screenplay",
            "dialogue_count": dialogue_count,
            "visual_count": visual_count,
            "audio_count": audio_count,
            "punch_count": punch_count,
            "sensory_score": total_score,
            "passed": passed,
            "critique": self._screenplay_critique(dialogue_count, visual_count, audio_count, punch_count, total_score)
        }
        
    def _screenplay_critique(self, d: int, v: int, a: int, p: int, score: int) -> List[str]:
        warnings = []
        if score < 35:
            warnings.append("Tổng điểm sensory dưới chuẩn (cần >= 35). Cần bổ sung thêm chỉ dẫn bối cảnh/âm thanh.")
        if d > 5 and v == 0:
            warnings.append("Thiếu hoàn toàn mô tả hình ảnh (show/scene) giữa hội thoại. Suki sẽ không có điểm tựa miêu tả biểu cảm.")
        if a == 0:
            warnings.append("Không có nhạc nền (play_music) hoặc hiệu ứng âm thanh (play_sound). Không gian âm thanh bị trống rỗng.")
        if d > 10 and p == 0:
            warnings.append("Thiếu các kích thích cơ học đột ngột (vpunch/hpunch) trong các đoạn hội thoại dài.")
        return warnings

    def verify_prose(self, prose_content: str) -> Dict[str, Any]:
        """Verify the written R18 prose draft for sensory density and AI slop."""
        # Simple word count approximation (spaces split)
        words = prose_content.split()
        word_count = len(words)
        
        # Word counts of sensory words
        sensory_matches = []
        prose_lower = prose_content.lower()
        for kw in self.k_sensory:
            count = len(re.findall(r'\b' + re.escape(kw) + r'\b', prose_lower))
            if count > 0:
                sensory_matches.append((kw, count))
                
        total_sensory_words = sum(c for _, c in sensory_matches)
        
        # Word counts of forbidden cliches
        forbidden_matches = []
        for kw in self.k_forbidden:
            count = prose_lower.count(kw)
            if count > 0:
                forbidden_matches.append((kw, count))
                
        total_forbidden_words = sum(c for _, c in forbidden_matches)
        
        # Scoring Logic (Max 100)
        # Sensory Keyword Density Ratio (ratio of sensory words to total words)
        # Target is >= 2.5% sensory keyword density (e.g. 25 keywords in a 1000-word text)
        kw_ratio = total_sensory_words / max(1, word_count)
        sensory_score = min(100, int(kw_ratio * 3000))  # 3.3% ratio gets 100
        
        # Subtract penalty for forbidden cliches (10 points per occurrence)
        cliche_penalty = total_forbidden_words * 12
        final_score = max(0, sensory_score - cliche_penalty)
        
        passed = final_score >= 80 # Prose gate is high, Suki must deliver excellent sensory prose
        
        # Compile critiques
        critiques = []
        if final_score < 80:
            critiques.append(f"Điểm prose sensory thấp ({final_score}/100, yêu cầu >= 80). Cần tăng mật độ tả cơ thể, hơi thở, xúc giác.")
        if kw_ratio < 0.02:
            critiques.append(f"Mật độ từ vựng cảm giác quá thấp ({kw_ratio * 100:.2f}%). Thiếu các từ tả nhịp tim, hơi thở, dịch bôi trơn.")
        for kw, c in forbidden_matches:
            critiques.append(f"Phát hiện AI-slop cliché: '{kw}' xuất hiện {c} lần. Hãy viết lại cụ thể sinh học, loại bỏ từ sáo rỗng.")
            
        return {
            "type": "prose",
            "word_count": word_count,
            "sensory_words_count": total_sensory_words,
            "forbidden_words_count": total_forbidden_words,
            "sensory_score": final_score,
            "passed": passed,
            "critique": critiques,
            "matches": dict(sensory_matches)
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LND Studio Sensory Density Validator")
    parser.add_argument("--path", required=True, help="Path to screenplay JSON or prose Markdown file")
    parser.add_argument("--type", choices=["screenplay", "prose"], required=True, help="Type of file to evaluate")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: file not found: {args.path}", file=sys.stderr)
        sys.exit(1)
        
    validator = SensoryDensityValidator()
    
    try:
        if args.type == "screenplay":
            with open(args.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            result = validator.verify_screenplay_packet(data)
        else:
            with open(args.path, 'r', encoding='utf-8') as f:
                content = f.read()
            result = validator.verify_prose(content)
            
        # Output evaluation report
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if not result["passed"]:
            sys.exit(2) # Exit with code 2 to indicate sensory gate failure
            
    except Exception as e:
        print(f"Validation Failed: {e}", file=sys.stderr)
        sys.exit(1)
