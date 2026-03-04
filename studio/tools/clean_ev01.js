const fs = require('fs');
const path = require('path');

const inputFile = '/home/datdang/working/lnd_dev/_lnd-output/_analysis/scene_scripts/EV01.md';
const outputDir = '/home/datdang/working/lnd_dev/_lnd-output/_analysis/scene_scripts/EV01_chapters';

fs.mkdirSync(outputDir, { recursive: true });

const lines = fs.readFileSync(inputFile, 'utf8').split('\n');
console.log(`Total lines in EV01.md: ${lines.length}`);

// Filter out non-dialogue lines (system data, code, plugin descriptions)
const isNarrativeLine = (line) => {
    if (!line || line.trim() === '') return false;
    // Skip code/system lines
    if (line.startsWith('$game')) return false;
    if (line.startsWith('"')) return false; // JSON-like ero-status entries
    if (line.match(/^[a-zA-Z_${}()\[\]0-9;<>=!|&+\-*\/\.]+$/)) return false;
    if (line.includes('plugin') || line.includes('Plugin') || line.includes('プラグイン')) return false;
    if (line.match(/^\d+[;,]?$/)) return false;
    if (line.includes('.png') || line.includes('.ogg') || line.includes('.json')) return false;
    if (line.startsWith('//') || line.startsWith('/*')) return false;
    if (line.match(/^[\s]*[{}()\[\]]+[\s]*$/)) return false;
    if (line.match(/^var |^let |^const |^function |^if |^else|^for |^while /)) return false;
    if (line.includes('Graphics.') || line.includes('Bitmap') || line.includes('Window_')) return false;
    if (line.includes('backlog') || line.includes('scrollBar') || line.includes('padding')) return false;
    if (line.startsWith('data[')) return false;
    if (line.match(/^\d+,\d+$/)) return false;
    // Keep Chinese/Japanese dialogue and narrative
    if (line.match(/[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]/)) return true;
    if (line.startsWith('「') || line.startsWith('（')) return true;
    if (line.includes('♥') || line.includes('♡')) return true;
    return false;
};

// Extract all narrative lines with their original line numbers
let narrativeBlocks = [];
let currentBlock = [];
let blockStartLine = 0;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (isNarrativeLine(line)) {
        if (currentBlock.length === 0) blockStartLine = i + 1;
        currentBlock.push(line);
    } else {
        if (currentBlock.length > 2) { // Only save blocks with more than 2 consecutive dialogue lines
            narrativeBlocks.push({
                startLine: blockStartLine,
                lines: [...currentBlock]
            });
        }
        currentBlock = [];
    }
}
// Don't forget the last block
if (currentBlock.length > 2) {
    narrativeBlocks.push({
        startLine: blockStartLine,
        lines: [...currentBlock]
    });
}

console.log(`Found ${narrativeBlocks.length} narrative blocks.`);

// Save each block as a separate chapter file
let totalNarrativeLines = 0;
narrativeBlocks.forEach((block, idx) => {
    const chapterNum = String(idx + 1).padStart(2, '0');
    const fileName = `Ch${chapterNum}_L${block.startLine}.md`;
    const filePath = path.join(outputDir, fileName);
    
    let content = `# Chapter Fragment ${chapterNum}\n`;
    content += `> Source: EV01.md, starting at line ${block.startLine}\n`;
    content += `> Lines: ${block.lines.length}\n\n`;
    content += block.lines.join('\n') + '\n';
    
    fs.writeFileSync(filePath, content);
    totalNarrativeLines += block.lines.length;
    console.log(`  ${fileName}: ${block.lines.length} lines`);
});

console.log(`\nTotal narrative lines extracted: ${totalNarrativeLines} / ${lines.length} original`);
console.log(`Compression ratio: ${((totalNarrativeLines / lines.length) * 100).toFixed(1)}%`);
