#!/bin/bash
# LND Studio - Suki Local Execution Wrapper
# Uses Hermes CLI (Local Model) for Prose Generation

FORENSIC_FILE=$1
OUTPUT_FILE=$2
HERMES_BIN="$HOME/.hermes/hermes-agent/venv/bin/hermes"

if [ -z "$FORENSIC_FILE" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: $0 <path_to_forensic.json> <path_to_output.md>"
    exit 1
fi

if [ ! -f "$FORENSIC_FILE" ]; then
    echo "❌ Error: Forensic file not found at $FORENSIC_FILE"
    exit 1
fi

echo "🧠 [Layer 3] Injecting JIT Rules for Suki (prose-generation)..."
export PATH="/usr/bin:/bin:$PATH"
RULES=$(./studio/scripts/venv/bin/python3 studio/scripts/rule_injector.py prose-generation)
FORENSIC_DATA=$(cat "$FORENSIC_FILE")

PROMPT="Bạn là Suki, chuyên gia viết văn R18 (R18 Prose Specialist).
Nhiệm vụ của bạn là chuyển đổi dữ liệu phân tích ảnh (Forensic Data) thành một trang truyện dâm thư tiếng Việt chất lượng cao.

=== LUẬT BẮT BUỘC (Layer 1 + JIT) ===
$RULES

=== DỮ LIỆU PHÂN TÍCH (Forensic Data) ===
$FORENSIC_DATA

=== YÊU CẦU ĐẦU RA ===
Viết phần văn xuôi (prose) cho trang này bằng tiếng Việt.
CHỈ TRẢ VỀ NỘI DUNG TRUYỆN. Không giải thích, không xin chào, không phân tích."

echo "✍️  [Local LLM] Invoking Hermes as Suki to generate prose..."
# Run Hermes in one-shot mode (-z) and pipe exactly the response to the output file
$HERMES_BIN -z "$PROMPT" > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Output saved to: $OUTPUT_FILE"
    echo "🧐 [Layer 4] Running Output Validator (Riko Audit)..."
    ./studio/scripts/venv/bin/python3 studio/scripts/output_validator.py audit "$OUTPUT_FILE"
else
    echo "❌ Error: Hermes CLI failed to generate prose."
    exit 1
fi
