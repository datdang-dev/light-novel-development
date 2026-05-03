const fs = require('fs');
const path = require('path');

/**
 * LND Studio - Prose Unwrapper Utility
 * -----------------------------------
 * Phích xuất nội dung văn xuôi từ JSON của Suki để người dùng có thể đọc trực tiếp.
 */

function unwrap(inputSource) {
    try {
        let rawContent;
        
        // 1. Kiểm tra xem input là file path hay JSON string
        if (fs.existsSync(inputSource)) {
            rawContent = fs.readFileSync(inputSource, 'utf8');
        } else {
            rawContent = inputSource;
        }

        // 2. Regex để tìm khối JSON (phòng trường hợp AI "yapping" linh tinh bên ngoài)
        const jsonMatch = rawContent.match(/\{[\s\S]*\}/);
        if (!jsonMatch) {
            throw new Error("Không tìm thấy khối JSON hợp lệ trong output.");
        }

        const data = JSON.parse(jsonMatch[0]);

        if (!data.prose_content) {
            throw new Error("JSON không chứa key 'prose_content'.");
        }

        // 3. Chuẩn bị thông tin hiển thị (Metrics)
        const metrics = data.metrics || {};
        const compliance = data.format_compliance || {};

        console.log("====================================================");
        console.log(`LND STUDIO - PROSE UNWRAPPER`);
        console.log(`Page: ${data.page_number} | Word Count: ${data.word_count}`);
        console.log(`Quality Score (Sensory): Smell: ${metrics.smell_mentions}, Sound: ${metrics.sound_mentions}, Texture: ${metrics.texture_mentions}`);
        console.log(`Compliance: ${compliance.valid_dialogue_format ? '✅ Dialogue OK' : '❌ Dialogue Error'}`);
        console.log("====================================================\n");

        // 4. Trả về nội dung văn xuôi
        return data.prose_content;

    } catch (error) {
        console.error(`[ERROR]: ${error.message}`);
        process.exit(1);
    }
}

// Chạy trực tiếp từ CLI: node unwrapper.js <file.json>
if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.log("Usage: node unwrapper.js <path_to_suki_output.json>");
        process.exit(0);
    }

    const inputPath = path.resolve(args[0]);
    const prose = unwrap(inputPath);
    
    const outputPath = inputPath.replace('.json', '.md');
    fs.writeFileSync(outputPath, prose, 'utf8');

    console.log(prose);
    console.log("\n====================================================");
    console.log(`[SUCCESS]: Đã trích xuất văn xuôi ra file: ${outputPath}`);
}
