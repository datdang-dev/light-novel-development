const fs = require('fs');
const path = require('path');

const colors = {
    reset: "\x1b[0m",
    green: "\x1b[32m",
    red: "\x1b[31m",
    yellow: "\x1b[33m",
    cyan: "\x1b[36m",
    bold: "\x1b[1m"
};

// --- RULES CONFIGURATION ---

// Banned phrases from anti_slop.md
const SLOP_BLACKLIST = [
    "shiver went down her spine",
    "shivers went down",
    "mix of fear and excitement",
    "eyes widened in shock",
    "eyes widened",
    "sending jolts of electricity",
    "a primal growl",
    "as they lay there",
    "they knew their lives would never be the same"
];

// Dialogue format patterns
const BANNED_QUOTES_REGEX = /["”‘'].+?["”’']/g;
const PROPER_DIALOGUE_REGEX = /「.+?」/g;
const PROPER_THOUGHT_REGEX = /（.+?）/g;
const PROPER_SFX_REGEX = /【.+?】|\*.+?\*/g;

// Sensory words for density check
const SENSORY_WORDS = [
    "ướt át", "lạnh", "nóng", "nhớp nháp", "rỉ nước", "nhóp nhép", 
    "dính dấp", "mồ hôi", "rên rỉ", "thở dốc", "mùi", "ngọt", "tanh", "chát"
];

function runLinter(fixturePath) {
    console.log(`\n${colors.cyan}${colors.bold}============================================================${colors.reset}`);
    console.log(`${colors.cyan}${colors.bold}  LND STUDIO - PROSE LINTER (STATIC TEXT ANALYSIS)          ${colors.reset}`);
    console.log(`${colors.cyan}${colors.bold}============================================================${colors.reset}\n`);

    if (!fs.existsSync(fixturePath)) {
        console.log(`${colors.red}✖ Fixture not found: ${fixturePath}${colors.reset}`);
        return;
    }

    const data = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));
    const contentLines = Array.isArray(data.content) ? data.content : [data.content || ""];
    const fullText = contentLines.join(" ");

    let stats = { violations: 0, warnings: 0, slop: 0, format: 0 };

    console.log(`${colors.bold}Analyzing Content (${contentLines.length} blocks)...${colors.reset}\n`);

    contentLines.forEach((line, index) => {
        const lineNum = index + 1;
        let lineHasError = false;

        // 1. Anti-Slop Check
        for (const phrase of SLOP_BLACKLIST) {
            const regex = new RegExp(phrase, 'i');
            if (regex.test(line)) {
                if (!lineHasError) console.log(`${colors.bold}Line ${lineNum}:${colors.reset} ${line}`);
                console.log(`  ${colors.red}✖ ANTI-SLOP VIOLATION:${colors.reset} Detected banned phrase "${phrase}"`);
                stats.slop++;
                stats.violations++;
                lineHasError = true;
            }
        }

        // 2. Dialogue Format Check (Banned quotes)
        if (BANNED_QUOTES_REGEX.test(line)) {
            if (!lineHasError) console.log(`${colors.bold}Line ${lineNum}:${colors.reset} ${line}`);
            console.log(`  ${colors.red}✖ FORMAT VIOLATION:${colors.reset} Used banned Western quotes (""). Must use 「」 for dialogue.`);
            stats.format++;
            stats.violations++;
            lineHasError = true;
        }
    });

    // 3. Sensory Density Check (Macro level)
    let sensoryCount = 0;
    SENSORY_WORDS.forEach(word => {
        const regex = new RegExp(word, 'gi');
        const matches = fullText.match(regex);
        if (matches) sensoryCount += matches.length;
    });

    console.log(`\n${colors.bold}Macro Analysis:${colors.reset}`);
    if (sensoryCount < 2 && fullText.length > 200) {
        console.log(`  ${colors.yellow}⚠ SENSORY DENSITY LOW:${colors.reset} Found only ${sensoryCount} sensory markers in ${fullText.length} chars.`);
        stats.warnings++;
    } else {
        console.log(`  ${colors.green}✔ SENSORY DENSITY OK:${colors.reset} Found ${sensoryCount} sensory markers.`);
    }

    const sfxMatches = fullText.match(PROPER_SFX_REGEX);
    if (sfxMatches) {
        console.log(`  ${colors.green}✔ SFX FORMAT OK:${colors.reset} Found ${sfxMatches.length} properly formatted SFX.`);
    }

    // Report
    console.log(`\n${colors.cyan}${colors.bold}============================================================${colors.reset}`);
    if (stats.violations === 0) {
        console.log(`${colors.green}✔ PROSE PASSES ALL LINTING CHECKS.${colors.reset}`);
    } else {
        console.log(`${colors.red}✖ PROSE FAILED LINTING CHECKS.${colors.reset}`);
        console.log(`  Total Violations: ${stats.violations}`);
        console.log(`  - Anti-Slop: ${stats.slop}`);
        console.log(`  - Format: ${stats.format}`);
        console.log(`  Warnings: ${stats.warnings}`);
    }
    console.log(`${colors.cyan}${colors.bold}============================================================${colors.reset}\n`);
}

const fixtureArg = process.argv[2] || path.join(__dirname, '../fixtures/test_case_vanilla.json');
runLinter(fixtureArg);
