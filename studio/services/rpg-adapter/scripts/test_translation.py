import json
import os
import shutil

MAP_FILE = "/mnt/d/nsfw_stuff/nymphomana_priesstess_v2/data/Map004.json"
BACKUP_FILE = "/mnt/d/nsfw_stuff/nymphomana_priesstess_v2/data/Map004.json.backup"

# Our hardcoded POC translation dictionary
TRANSLATION_DICT = {
    "嗝～！……嗝！": "Ợ~! ...Ợ!",
    "那边的小哥哥小姐姐，一起来喝酒啊！": "Cậu em và cô em gái đằng kia, lại đây uống rượu cùng nào!",
    "让祭司给他口交": "Bắt Nữ tu sĩ bú cặc lão",
    "算了": "Bỏ đi",
    "嗝～！": "Ợ~!",
    "这里的酒和其他地方不同！": "Rượu ở đây khác biệt lắm đấy!",
    "小哥哥你们是冒险者吗？": "Cậu em đây là mạo hiểm giả hả?",
    "情侣冒险者的话会快乐很多呢……嗝！": "Là mạo hiểm giả cặp đôi thì chắc là vui lắm nhỉ... Ợ!",
    "已经去过各种各样的地方啪啪啪了吧？": "Chắc hẳn đã đi chịch nhau ở đủ mọi nơi rồi phải không?",
    "印象最深的是哪里呢？嗯？": "Ấn tượng nhất là làm ở đâu hả? Hửm?",
    "别摆出这么难看的脸，喝吧，喝吧！": "Đừng làm cái mặt khó coi thế chứ, uống đi, uống đi!",
    "小哥哥也是，别客气～喝！": "Cậu em cũng thế, đừng khách sáo~ Uống!",
    "但是，和这么色情的小姐姐一起冒险": "Nhưng mà, đi mạo hiểm cùng một cô em gợi tình thế này...",
    "那里撑得住吗？": "Chỗ đó có chịu nổi không hả?",
    "肉棒啊，肉棒！": "Là cái con cặc ấy, con cặc ấy!",
    "如果我像你这个年纪和这种色情的小姐姐一起旅行的话": "Nếu tao mà ở tuổi mày, đi du lịch với con đĩ như này...",
    "冒险什么的早就丢在一边了，每天像猴子一样交配！……嗝！": "Thì tao đã vứt mẹ việc mạo hiểm sang một bên, ngày nào cũng giao phối như khỉ rồi! ...Ợ!",
    "喂小姐，告诉我！": "Này cô em, nói tao nghe!",
    "你和小哥哥做了多少次？": "Mày và thằng nhóc này đã làm nhau bao nhiêu lần rồi?",
    "哎呀，不好！被大叔吸引住了……": "Ây da, không xong rồi! Bị ông chú thu hút mất rồi...",
    "那个……！": "Dạ...!",
    "我已经不是处女了，非常淫荡哦……！": "Cháu không còn là trinh nữ nữa, cháu dâm đãng lắm luôn ạ...!",
    "哦哦，小姐你真大胆啊！这身体真是丰满！": "Ồ ồ, cô em mạnh bạo thật đấy! Cơ thể này đúng là mlem mlem!",
    "让我看看，让我看看……": "Cho tao xem nào, cho tao xem nào..."
}


def create_backup():
    if not os.path.exists(BACKUP_FILE):
        print(f"Creating backup: {BACKUP_FILE}")
        shutil.copy2(MAP_FILE, BACKUP_FILE)
    else:
        print("Backup already exists.")

def patch_map():
    with open(MAP_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    replacements = 0
    # Map data has 'events', which is a list (index 0 is null usually)
    for ev in data.get('events', []):
        if not ev:
            continue
        
        # We only care about Event 24 for the POC
        if ev.get('id') != 24:
            continue
            
        for page in ev.get('pages', []):
            for cmd in page.get('list', []):
                code = cmd.get('code')
                params = cmd.get('parameters', [])
                
                # 401 is Show Text
                if code == 401 and params:
                    original_text = params[0]
                    # Direct lookup
                    if original_text in TRANSLATION_DICT:
                        print(f"[Text] Rep: {original_text} -> {TRANSLATION_DICT[original_text]}")
                        cmd['parameters'][0] = TRANSLATION_DICT[original_text]
                        replacements += 1
                        
                # 102 is Show Choices
                elif code == 102 and params and len(params) > 0:
                    choices = params[0]  # List of choices
                    for i, choice in enumerate(choices):
                        if choice in TRANSLATION_DICT:
                            print(f"[Choice] Rep: {choice} -> {TRANSLATION_DICT[choice]}")
                            choices[i] = TRANSLATION_DICT[choice]
                            replacements += 1

    print(f"\nTotal replacements made: {replacements}")
    
    if replacements > 0:
        with open(MAP_FILE, 'w', encoding='utf-8') as f:
            # Note: ensure_ascii=False is critical to avoid encoding Unicode characters to \uXXXX
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Successfully patched {MAP_FILE}!")
    else:
        print("No matches found to patch.")


if __name__ == "__main__":
    create_backup()
    patch_map()
