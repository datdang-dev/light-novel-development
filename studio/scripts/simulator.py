import os
import json
from pathlib import Path

# Vị trí gốc của LND Studio
PROJECT_ROOT = Path("/home/datdang/working/lnd_dev")
OUTPUT_DIR = PROJECT_ROOT / "_bmad-output" / "_prose" / "simulation_test"

def read_file(filepath):
    """Đọc nội dung một file text."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"[WARNING] Không tìm thấy file: {filepath}"

def generate_mock_forensic():
    """Tạo một file forensic-state.json giả lập nếu chưa có sẵn."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    mock_file = OUTPUT_DIR / "forensic-state-1.json"
    
    mock_data = {
        "page_number": "1",
        "content_tags": ["intro", "bedroom", "libido_x"],
        "characters_present": ["Kida", "Aria"],
        "setting": {
            "location": "Kida's Bedroom",
            "time": "Night",
            "atmosphere": "Heavy, smelling of sweat"
        },
        "panels": [
            {"panel_number": 1, "description": "Aria standing over the bed.", "action": "Looking down haughtily"}
        ],
        "dialogue": [
            {"speaker": "Aria", "text_original": "...", "text_translated": "Dậy đi đồ rác rưởi.", "context": "Wake up call"}
        ],
        "sfx": [
            {"original": "...", "romanized": "gasa gasa", "lewd_equivalent": "rustle rustle"}
        ]
    }
    
    with open(mock_file, 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, indent=4, ensure_ascii=False)
    
    return mock_file

def simulate_jit_payload():
    """Giả lập quy trình JIT Compilation của Gooner Alchemist - Bước 4."""
    print("🎬 Khởi động Gooner Alchemist Simulation Module...")
    
    # 1. Các file tĩnh cần load như quy định trong workflow
    print("\n[+] Đang đọc Master Context...")
    pipeline_context_path = PROJECT_ROOT / "studio" / "config" / "pipeline-context.md"
    master_context = read_file(pipeline_context_path)
    
    print("[+] Đang đọc Mechanics Rules...")
    mechanics_path = PROJECT_ROOT / ".agent" / "rules" / "lewd_writing_mechanics.md"
    mechanics_rules = read_file(mechanics_path)
    
    # 2. Sinh ra Forensic Mock hoặc Load Forensic có thật
    print("[+] Đang lấy dữ liệu trinh sát (Forensic State)...")
    forensic_path = generate_mock_forensic()
    forensic_state = read_file(forensic_path)
    
    # 3. Gộp tất cả thành Payload duy nhất
    print("[+] Đang JIT Compile thành Context Payload siêu lớn...")
    
    final_payload = f"""# === GOONER ALCHEMIST FINAL PAYLOAD ===

## 1. STUDIO MASTER CONTEXT
{master_context}

---
## 2. PROJECT MECHANICS (LEWD WRITING)
{mechanics_rules}

---
## 3. CURRENT SCENE STATE (FORENSIC)
```json
{forensic_state}
```

---
## 4. ACTION REQUIRED
Hỡi Suki! Bạn đã có toàn bộ bối cảnh của studio, toàn bộ quy tắc 18+ bắt buộc, và cấu trúc chính xác của trang truyện này.
Hãy viết luồng suy nghĩ của bạn, sau đó trả về chuẩn xác theo format `draft-prose.schema.json`.
"""

    # 4. Xuất ra thư mục Test
    payload_out_path = OUTPUT_DIR / "context_payload.md"
    with open(payload_out_path, 'w', encoding='utf-8') as f:
        f.write(final_payload)
        
    print(f"\n✅ FULL SEQUENCE SIMULATED THÀNH CÔNG!")
    print(f"📁 Bạn có thể xem toàn bộ lượng text sẽ bị đẩy cho AI Suki tại:")
    print(f"➡️ {payload_out_path}")

if __name__ == "__main__":
    simulate_jit_payload()
