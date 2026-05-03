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

const PROJECT_ROOT = path.resolve(__dirname, '../../');

function loadRule(ruleName) {
    const p = path.join(PROJECT_ROOT, 'studio/rules', ruleName);
    return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : '';
}

async function runRikoJudge(prosePath) {
    console.log(`\n${colors.cyan}${colors.bold}============================================================${colors.reset}`);
    console.log(`${colors.cyan}${colors.bold}  LND STUDIO - LLM-AS-A-JUDGE (RIKO EVALUATOR)              ${colors.reset}`);
    console.log(`${colors.cyan}${colors.bold}============================================================${colors.reset}\n`);

    if (!fs.existsSync(prosePath)) {
        console.log(`${colors.red}✖ Prose file not found: ${prosePath}${colors.reset}`);
        return;
    }

    // 1. Load target prose
    let targetProse = "";
    try {
        const data = JSON.parse(fs.readFileSync(prosePath, 'utf8'));
        targetProse = Array.isArray(data.content) ? data.content.join('\n') : (data.prose_content || JSON.stringify(data));
    } catch (e) {
        targetProse = fs.readFileSync(prosePath, 'utf8');
    }

    // 2. Load Evaluation Context (Rules)
    const mechanics = loadRule('lewd_writing_mechanics.md');
    const antislop = loadRule('anti_slop.md');
    
    // 3. Assemble the Prompt for Riko
    const systemPrompt = `You are Riko, the Quality Audit Agent for LND Studio.
Your job is to act as an aggressive, highly critical editor for R18 Light Novel prose.

EVALUATION CRITERIA:
1. Sensory Density: Does it engage multiple senses?
2. Anti-Slop: Does it use banned tropes or sound like a generic AI?
3. Escalation: Is the pacing visceral and grounded?

### RULE: LEWD MECHANICS
${mechanics}

### RULE: ANTI-SLOP
${antislop}

INSTRUCTIONS:
Evaluate the following draft prose based on the criteria above.
Output your response as JSON matching this format:
{
  "score": <0-100>,
  "verdict": "<PASS|FAIL>",
  "critique_points": ["point 1", "point 2"],
  "rewrite_suggestions": "..."
}`;

    console.log(`${colors.bold}Step 1: Assembled Evaluation Payload${colors.reset}`);
    console.log(`  -> Loaded System Prompt & Persona (Riko)`);
    console.log(`  -> Injected Rule: lewd_writing_mechanics.md`);
    console.log(`  -> Injected Rule: anti_slop.md`);
    console.log(`  -> Loaded Target Prose (${targetProse.length} chars)`);

    console.log(`\n${colors.bold}Step 2: LLM API Invocation${colors.reset}`);
    const apiKey = process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY;
    
    if (!apiKey) {
        console.log(`  ${colors.yellow}⚠ No API Key found in environment variables.${colors.reset}`);
        console.log(`  ${colors.cyan}MOCKING LLM RESPONSE...${colors.reset}\n`);
        
        // Mock Response simulation for testing the pipeline
        const mockResponse = {
            score: 45,
            verdict: "FAIL",
            critique_points: [
                "Prose contains banned phrase 'shiver went down her spine' (Violation of Anti-Slop).",
                "Sensory density is extremely poor. Relies heavily on visual descriptions.",
                "Uses Western quotes instead of Japanese brackets for dialogue."
            ],
            rewrite_suggestions: "Remove all English phrases. Convert dialogue to 「」. Inject tactile sensations (temperature, texture) when the character is touched."
        };

        console.log(`${colors.red}✖ VERDICT: ${mockResponse.verdict}${colors.reset} (Score: ${mockResponse.score}/100)`);
        console.log(`\n${colors.bold}Critique Points:${colors.reset}`);
        mockResponse.critique_points.forEach(p => console.log(`  - ${p}`));
        console.log(`\n${colors.bold}Rewrite Instructions for Suki:${colors.reset}`);
        console.log(`  > ${mockResponse.rewrite_suggestions}`);
        
    } else {
        console.log(`  ${colors.green}✔ API Key detected. Real LLM invocation would happen here.${colors.reset}`);
        console.log(`  (Implementation of fetch() to OpenAI/Anthropic omitted for dry-run)`);
    }

    console.log(`\n${colors.cyan}${colors.bold}============================================================${colors.reset}`);
    console.log(`To execute with real LLM: export OPENAI_API_KEY='your_key' && node riko_judge.js <file>`);
    console.log(`${colors.cyan}${colors.bold}============================================================${colors.reset}\n`);
}

const targetPath = process.argv[2] || path.join(__dirname, '../fixtures/test_case_vanilla.json');
runRikoJudge(targetPath);
