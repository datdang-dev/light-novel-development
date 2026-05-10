#!/bin/bash
# LND Studio - Hermes Rewrite Script
# Mục đích: Gọi Local Model qua Hermes CLI để viết lại Chương 9.

TARGET_FILE="_lnd-output/_novels/nymphomania_priestess/novel_chapter_09.md"
OUTPUT_FILE="_lnd-output/_novels/nymphomania_priestess/novel_chapter_09_revised.md"
HERMES_BIN="$HOME/.hermes/hermes-agent/venv/bin/hermes"

if [ ! -f "$TARGET_FILE" ]; then
    echo "❌ Lỗi: Không tìm thấy file $TARGET_FILE"
    exit 1
fi

export PATH="/usr/bin:/bin:$PATH"
echo "🧠 [Layer 3] Đang Compile FULL Context (Persona + JIT Rules + Knowledge)..."
# Sử dụng agent_compiler.py để nạp 100% "não bộ" của Suki
FULL_CONTEXT=$(./studio/scripts/venv/bin/python3 studio/scripts/agent_compiler.py studio/agents/lewd-writer.agent.yaml prose-generation --scene-tags explicit)
ORIGINAL_CONTENT=$(cat "$TARGET_FILE")

PROMPT="$FULL_CONTEXT

=== NHIỆM VỤ THỰC THI (TASK) ===
Nhiệm vụ của bạn là VIẾT LẠI (Rewrite) toàn bộ Chương 9 của tiểu thuyết Nymphomania Priestess dựa trên bản gốc dưới đây.

=== YÊU CẦU CẢI THIỆN CHI TIẾT ===
1. CHẬM NHỊP ĐỘ: Đặc biệt ở cảnh George ngửi chân và nách Kohaku. Kéo dài sự miêu tả.
2. SENSORY DENSITY: Thêm miêu tả chi tiết về độ nhớp nháp của mồ hôi, mùi hương (chua, nồng, tanh của dâm thủy), âm thanh (tiếng thở dốc, tiếng hít hà), và nhiệt độ cơ thể.
3. TÂM LÝ NYMPHOMANIA: Kohaku bề ngoài cố giữ giá trị Thánh Nữ, nhưng cơ thể phản bội cô. Việc bị một gã lạ mặt ngửi nách giữa quảng trường khiến cô nhục nhã nhưng lại rỉ dâm thủy vì hưng phấn tột độ.
4. TƯƠNG TÁC JIMMY: Jimmy luôn lạnh lùng, dung túng và cố tình đẩy Kohaku vào các tình huống này để ép cô bộc lộ bản chất thật. Thêm cái nhìn soi mói của Jimmy.
5. GIỮ NGUYÊN CỐT TRUYỆN: Tìm chủ nhân tất -> Là nhân yêu ở phố đèn đỏ. Nhưng biến hóa câu chữ cho đậm chất văn học Erotic.
6. FORMAT BẮT BUỘC: Đối thoại dùng 「...」, suy nghĩ dùng （...）, âm thanh dùng *in nghiêng*. Không giải thích dài dòng.

=== BẢN GỐC CẦN VIẾT LẠI ===
$ORIGINAL_CONTENT

=== YÊU CẦU ĐẦU RA ===
Viết lại toàn bộ chương 9 theo yêu cầu trên bằng tiếng Việt. 
CHỈ TRẢ VỀ NỘI DUNG TRUYỆN. Không nói thêm bất kỳ từ nào ngoài lề."

echo "✍️  [Local LLM] Đang gọi Hermes (Suki FULL CONTEXT) để tiến hành viết lại..."
$HERMES_BIN -z "$PROMPT" > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Viết lại thành công! Đã lưu tại: $OUTPUT_FILE"
    echo "🧐 [Layer 4] Đang chấm điểm Output..."
    ./studio/scripts/venv/bin/python3 studio/scripts/output_validator.py audit "$OUTPUT_FILE"
else
    echo "❌ Lỗi: Hermes CLI gặp sự cố khi generate."
fi
