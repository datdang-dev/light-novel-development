import json
import os
import time
import re
from pathlib import Path

# Thư viện dịch thuật miễn phí (cần cài đặt: pip install deep-translator)
try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Vui lòng cài đặt deep-translator: pip install deep-translator")
    exit(1)

INPUT_JSON = "/mnt/d/nsfw_stuff/nymphomana_priesstess_v2/ManualTransFile.json"
OUTPUT_JSON = "/mnt/d/nsfw_stuff/nymphomana_priesstess_v2/ManualTransFile_VN.json"
CACHE_FILE = "/home/datdang/working/lnd_dev/studio/services/rpg-adapter/scripts/translation_cache.json"

CHUNK_SIZE = 100 # Dịch 100 dòng mỗi lần
DELAY_BETWEEN_CHUNKS = 1 # Tránh bị Google ban IP

def is_translatable(text):
    """Lọc bỏ các text là số, ID hệ thống, hoặc code thuần tuý."""
    if not text or len(text.strip()) == 0:
        return False
    # Nếu chỉ chứa số
    if text.isdigit():
        return False
    # Nếu là ID kiểu EV001, NPC-兵士, V100
    if re.match(r'^(EV|NPC-).*\d*$', text):
        return False
    return True

def translate_chunk(texts):
    """Gửi 1 mảng text lên Google Translate (Có thể thay bằng API LLM ở đây)"""
    translator = GoogleTranslator(source='auto', target='vi')
    try:
        translated = translator.translate_batch(texts)
        return translated
    except Exception as e:
        print(f"\n[Lỗi Dịch] {e}")
        time.sleep(5)
        return None

def main():
    print(f"Loading {INPUT_JSON}...")
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total keys: {len(data)}")

    # 1. Tải Cache nếu script bị dừng giữa chừng
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        print(f"Loaded {len(cache)} translated lines from cache.")

    # 2. Lọc danh sách cần dịch
    keys_to_translate = []
    for k, v in data.items():
        if k not in cache and is_translatable(v):
            keys_to_translate.append((k, v))
            
    # Tự động gán những dòng không cần dịch (ID, số) vào cache
    for k, v in data.items():
        if not is_translatable(v) and k not in cache:
            cache[k] = v

    print(f"Lines pending translation: {len(keys_to_translate)}")

    # 3. Dịch theo chunk
    total_chunks = len(keys_to_translate) // CHUNK_SIZE + 1
    
    for i in range(0, len(keys_to_translate), CHUNK_SIZE):
        chunk = keys_to_translate[i:i+CHUNK_SIZE]
        keys = [item[0] for item in chunk]
        texts = [item[1] for item in chunk]
        
        chunk_idx = i // CHUNK_SIZE + 1
        print(f"Translating chunk {chunk_idx}/{total_chunks} ({len(texts)} lines)...", end="", flush=True)
        
        translated_texts = translate_chunk(texts)
        
        if translated_texts and len(translated_texts) == len(texts):
            for j, k in enumerate(keys):
                cache[k] = translated_texts[j]
            print(" OK")
            
            # Lưu cache liên tục
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
                
        else:
            print(" FAILED. Retrying next loop.")
            
        time.sleep(DELAY_BETWEEN_CHUNKS)

    # 4. Gắn lại vào JSON gốc và xuất file
    print(f"\nBuilding final JSON...")
    final_output = {}
    for k, v in data.items():
        final_output[k] = cache.get(k, v) # Lấy từ cache, nếu thiếu thì xài gốc

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, ensure_ascii=False, indent=4)
        
    print(f"Done! Saved translated file to: {OUTPUT_JSON}")
    print("XÓA FILE CŨ TÊN ManualTransFile.json VÀ ĐỔI TÊN FILE NÀY THÀNH ManualTransFile.json ĐỂ GAME NHẬN.")

if __name__ == "__main__":
    main()
