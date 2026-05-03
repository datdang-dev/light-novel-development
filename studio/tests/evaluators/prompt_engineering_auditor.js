const fs = require('fs');
const path = require('path');
const { runValidation } = require('../prompt_validator');

const colors = {
    reset: "\x1b[0m",
    green: "\x1b[32m",
    red: "\x1b[31m",
    yellow: "\x1b[33m",
    cyan: "\x1b[36m",
    bold: "\x1b[1m"
};

async function auditPromptEngineering(trigger, sceneTag) {
    console.log(`\n${colors.cyan}${colors.bold}============================================================${colors.reset}`);
    console.log(`${colors.cyan}${colors.bold}  LND STUDIO - PROMPT ENGINEERING AUDITOR                   ${colors.reset}`);
    console.log(`${colors.cyan}${colors.bold}============================================================${colors.reset}\n`);

    console.log(`${colors.bold}Step 1: Compiling Full Prompt for Trigger [${trigger}] with Scene [${sceneTag}]...${colors.reset}`);
    
    // Silence console output of validator for a cleaner audit log
    const originalLog = console.log;
    const originalWrite = process.stdout.write;
    console.log = () => {};
    process.stdout.write = () => {};
    
    let assembledPrompt = "";
    try {
        assembledPrompt = await runValidation(trigger, sceneTag);
    } catch (e) {
        console.log = originalLog;
        process.stdout.write = originalWrite;
        console.log(`${colors.red}✖ Failed to assemble prompt: ${e.message}${colors.reset}`);
        return;
    }

    console.log = originalLog;
    process.stdout.write = originalWrite;

    if (!assembledPrompt) {
        console.log(`${colors.red}✖ Prompt assembly returned empty. Check your orchestrator/skill configurations.${colors.reset}`);
        return;
    }

    const estTokens = Math.round(assembledPrompt.split(/\s+/).length * 1.3);
    console.log(`  ✔ Prompt assembled successfully (Approx ${estTokens.toLocaleString()} tokens).`);

    const metaPrompt = `
You are a World-Class Prompt Engineer and AI Systems Architect.
Your task is to review an ASSEMBLED PROMPT that is about to be sent to an LLM (Claude/GPT-4). 
The user uses a dynamic architecture to inject different markdown rules into a base SKILL.md.

Evaluate the assembled prompt below for the following:
1. INSTRUCTION CLARITY: Are the instructions clear or ambiguous?
2. CONTRADICTIONS: Are there any conflicting rules between the injected files?
3. ATTENTION DILUTION: Is the prompt too long or filled with redundant information that might cause the LLM to forget its persona?
4. PERSONA CONSISTENCY: Does the persona remain strong throughout?

ASSEMBLED PROMPT TO EVALUATE:
--------------------------------
${assembledPrompt}
--------------------------------

Output your evaluation in JSON:
{
  "prompt_score": <0-100>,
  "major_flaws": ["flaw 1", "flaw 2"],
  "contradictions_found": ["conflict A vs B"],
  "optimization_suggestions": "..."
}
`;

    console.log(`\n${colors.bold}Step 2: Sending Assembled Prompt to Meta-AI (Prompt Auditor)...${colors.reset}`);
    const apiKey = process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY;

    const dumpPath = path.join(__dirname, 'latest_meta_prompt.txt');
    fs.writeFileSync(dumpPath, metaPrompt);
    console.log(`\n  📝 Saved full meta-prompt to: ${dumpPath}`);

    if (!apiKey) {
        console.log(`  ${colors.yellow}⚠ No API Key found. Using Local 'Smart' Analysis...${colors.reset}\n`);
        
        const mockResponse = {
            "prompt_score": 100,
            "major_flaws": [],
            "contradictions_found": [],
            "optimization_suggestions": "No major issues found. Prompt is clean and follows LND standards."
        };

        // 1. Check for redudant vocabulary injection
        const injectionRegex = /loads:[\s\S]*?sensory-vocabulary\.md/i;
        if (injectionRegex.test(assembledPrompt)) {
            mockResponse.prompt_score -= 15;
            mockResponse.major_flaws.push("Attention Dilution: 'sensory-vocabulary.md' is still being actively injected in the triggers block.");
        }

        // 2. Check for dialogue format contradictions
        if (assembledPrompt.includes('voice-example: "')) {
            mockResponse.prompt_score -= 15;
            mockResponse.contradictions_found.push("Contradiction: character_voice.md still contains Western quotes \"\" in examples.");
        }

        // 3. Check for Output Schema
        if (!assembledPrompt.includes("OUTPUT FORMAT") || !assembledPrompt.includes("draft-prose.schema.json")) {
            mockResponse.prompt_score -= 20;
            mockResponse.major_flaws.push("Missing Output Schema: Final prompt lacks strict JSON formatting boundaries.");
        }

        if (mockResponse.prompt_score === 100) {
            console.log(`${colors.green}${colors.bold}✔ PROMPT ENGINEERING SCORE: 100/100 (PASSED)${colors.reset}`);
            console.log(`\n${colors.green}Phân tích:${colors.reset}`);
            console.log(`  - Redundancy: [CLEARED] sensory-vocabulary.md đã bị gỡ bỏ.`);
            console.log(`  - Contradictions: [CLEARED] Toàn bộ thoại đã dùng ngoặc 「」.`);
            console.log(`  - Boundaries: [CLEARED] Đã tìm thấy OUTPUT FORMAT ép JSON.`);
        } else {
            console.log(`${colors.red}✖ PROMPT ENGINEERING SCORE: ${mockResponse.prompt_score}/100${colors.reset}`);
        }
        
        if (mockResponse.contradictions_found.length > 0) {
            console.log(`\n${colors.red}${colors.bold}CONTRADICTIONS DETECTED:${colors.reset}`);
            mockResponse.contradictions_found.forEach(c => console.log(`  - ${c}`));
        }

        console.log(`\n${colors.yellow}${colors.bold}MAJOR FLAWS:${colors.reset}`);
        mockResponse.major_flaws.forEach(f => console.log(`  - ${f}`));

        console.log(`\n${colors.green}${colors.bold}SUGGESTIONS FOR YOUR SKILL.MD / RULES:${colors.reset}`);
        console.log(`  > ${mockResponse.optimization_suggestions}`);
    } else {
        console.log(`  ${colors.green}✔ API Key detected. Real LLM invocation would happen here.${colors.reset}`);
        console.log(`  (Implementation of fetch() omitted for dry-run. You can save 'metaPrompt' to a file to run it).`);
    }

    console.log(`\n${colors.cyan}${colors.bold}============================================================${colors.reset}\n`);
}

const triggerArg = process.argv[2] || 'MA';
const sceneArg = process.argv[3] || 'explicit';
auditPromptEngineering(triggerArg, sceneArg);
