const fs = require('fs');
const path = require('path');

// NOTE: Requires 'yaml' package. Install via: npm install yaml
let yaml;
try {
    yaml = require('yaml');
} catch (e) {
    console.error("❌ Mising dependency. Please run: npm install yaml");
    process.exit(1);
}

// Configuration
const PROJECT_ROOT = path.resolve(__dirname, '../../');
const ORCHESTRATOR_PATH = path.join(PROJECT_ROOT, 'studio/agents/lnd-orchestrator.agent.yaml');

function resolvePath(rawPath) {
    if (!rawPath) return '';
    return rawPath.replace('{project-root}', PROJECT_ROOT);
}

function fileExists(filePath) {
    try {
        return fs.existsSync(filePath);
    } catch (err) {
        return false;
    }
}

function parseFrontmatter(fileContent) {
    const match = fileContent.match(/^-{3,}\s*([\s\S]*?)-{3,}/);
    if (!match) return null;
    try {
        return yaml.parse(match[1]);
    } catch (e) {
        console.error("YAML Parse Error in frontmatter:", e.message);
        return null;
    }
}

async function runValidation(triggerCode, targetSceneTag = null) {
    console.log(`\n[TEST RUN] Trigger: ${triggerCode} | Scene Tag: ${targetSceneTag || 'None'}`);
    console.log("=".repeat(60));

    let stats = { pass: 0, warn: 0, fail: 0 };
    let assembledPromptText = "";

    // 1. Load Orchestrator
    process.stdout.write("1. Orchestrator Resolution ... ");
    if (!fileExists(ORCHESTRATOR_PATH)) {
        console.log("[❌ FAIL] lnd-orchestrator.agent.yaml not found.");
        stats.fail++;
        return;
    }

    const orchContent = fs.readFileSync(ORCHESTRATOR_PATH, 'utf8');
    const orchYaml = yaml.parse(orchContent);

    // Find the trigger in the menu
    const menu = orchYaml.agent?.menu || [];
    const triggerItem = menu.find(m => m.trigger && m.trigger.startsWith(triggerCode));
    
    if (!triggerItem) {
        console.log(`[❌ FAIL] Trigger '${triggerCode}' not found in Orchestrator menu.`);
        stats.fail++;
        return;
    }
    console.log("[✅ PASS]");
    stats.pass++;

    console.log(`   -> Action Flow:\n${triggerItem.action.split('\n').map(l => '      ' + l).join('\n')}`);

    // Since a trigger can call multiple agents (e.g. MA calls Kana -> Aria -> Suki -> Riko),
    // for this test framework, we will focus on validating the 'lewd-writer' (Suki) SKILL.md 
    // as it contains the complex injection logic shown in the briefing. 
    // In a fully expanded script, we would parse the action flow and validate EVERY skill.
    
    // Hardcoded target for this specific test based on the context:
    const targetSkillPath = path.join(PROJECT_ROOT, 'studio/core/lewd-writer/SKILL.md');
    const targetAgentPath = path.join(PROJECT_ROOT, 'studio/agents/lewd-writer.agent.yaml');

    // 2. Persona / Agent Loading
    process.stdout.write("\n2. Persona Loading (lewd-writer) ... ");
    if (fileExists(targetAgentPath)) {
        console.log("[✅ PASS]");
        const agentContent = fs.readFileSync(targetAgentPath, 'utf8');
        assembledPromptText += agentContent + "\n\n";
        stats.pass++;
    } else {
        console.log("[⚠️ WARN] lewd-writer.agent.yaml not found. Skipping persona.");
        stats.warn++;
    }

    // 3. SKILL.md Loading & Knowledge Injection
    process.stdout.write("\n3. Knowledge Injection Loading ... ");
    if (!fileExists(targetSkillPath)) {
        console.log(`[❌ FAIL] Target skill file not found: ${targetSkillPath}`);
        stats.fail++;
        return;
    }

    const skillContent = fs.readFileSync(targetSkillPath, 'utf8');
    assembledPromptText += skillContent + "\n\n";
    const skillMeta = parseFrontmatter(skillContent);

    let injectionStats = { always: 0, triggers: 0, missing: 0 };

    if (skillMeta && skillMeta.injection) {
        // Load Always
        if (skillMeta.injection.always) {
            for (const file of skillMeta.injection.always) {
                const resolved = resolvePath(file);
                if (fileExists(resolved)) {
                    assembledPromptText += fs.readFileSync(resolved, 'utf8') + "\n\n";
                    injectionStats.always++;
                } else {
                    console.log(`\n      [❌ MISSING] ALWAYS: ${resolved}`);
                    injectionStats.missing++;
                }
            }
        }

        // Load Triggers
        if (skillMeta.injection.triggers && targetSceneTag) {
            // Fuzzy match the scene tag against regex in scene_tag
            for (const trigger of skillMeta.injection.triggers) {
                const tagRegex = new RegExp(trigger.scene_tag, 'i');
                if (tagRegex.test(targetSceneTag)) {
                    console.log(`\n      -> Matched trigger block: '${trigger.scene_tag}'`);
                    for (const file of trigger.loads) {
                        const resolved = resolvePath(file);
                        if (fileExists(resolved)) {
                            assembledPromptText += fs.readFileSync(resolved, 'utf8') + "\n\n";
                            injectionStats.triggers++;
                        } else {
                            console.log(`\n      [❌ MISSING] TRIGGER: ${resolved}`);
                            injectionStats.missing++;
                        }
                    }
                }
            }
        }
    }

    if (injectionStats.missing === 0) {
        console.log(`[✅ PASS]`);
        stats.pass++;
    } else {
        console.log(`[❌ FAIL] Found ${injectionStats.missing} missing files.`);
        stats.fail++;
    }
    console.log(`   -> ALWAYS (${injectionStats.always} files loaded)`);
    console.log(`   -> TRIGGERS matching '${targetSceneTag}' (${injectionStats.triggers} files loaded)`);
    console.log(`   -> Missing files: ${injectionStats.missing}`);

    // 4. Schema Validation (Example check for draft-prose.schema.json)
    process.stdout.write("\n4. Schema Validation ... ");
    const schemaPath = path.join(PROJECT_ROOT, 'studio/schemas/draft-prose.schema.json');
    if (fileExists(schemaPath)) {
        try {
            JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
            console.log("[✅ PASS]");
            console.log(`   -> draft-prose.schema.json is valid JSON.`);
            stats.pass++;
        } catch (e) {
            console.log("[❌ FAIL]");
            console.log(`   -> draft-prose.schema.json has invalid JSON syntax: ${e.message}`);
            stats.fail++;
        }
    } else {
        console.log("[⚠️ WARN]");
        console.log(`   -> Schema file not found: ${schemaPath}`);
        stats.warn++;
    }

    // 5. Final Prompt Assembly Check
    process.stdout.write("\n5. Final Prompt Assembly ... ");
    const charCount = assembledPromptText.length;
    const wordCount = assembledPromptText.split(/\s+/).length;
    // Rough estimation: 1 word ~ 1.3 tokens
    const estTokens = Math.round(wordCount * 1.3);

    let status = "[✅ PASS]";
    if (estTokens > 150000) {
        status = "[❌ FAIL]";
        stats.fail++;
    } else if (estTokens > 80000) {
        status = "[⚠️ WARN]";
        stats.warn++;
    } else {
        stats.pass++;
    }

    console.log(status);
    console.log(`   -> Total size: ~${wordCount.toLocaleString()} words (Approx ${estTokens.toLocaleString()} tokens)`);
    if (estTokens > 80000) {
        console.log(`   -> Warning: Context size is very large. Consider optimizing injection rules.`);
    }

    // Conclusion
    console.log("\n" + "=".repeat(60));
    console.log(`[RESULT] ${stats.pass} PASS, ${stats.warn} WARNING, ${stats.fail} FAIL.`);
    if (stats.fail === 0) {
        console.log("Pipeline is CONSISTENT. ✅");
    } else {
        console.log("Pipeline has INCONSISTENCIES. ❌");
    }
    console.log("=".repeat(60) + "\n");
    
    return assembledPromptText;
}

// CLI Execution
if (require.main === module) {
    const args = process.argv.slice(2);
    let trigger = 'MA'; // Default
    let tag = 'explicit'; // Default

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--trigger' && args[i+1]) trigger = args[i+1];
        if (args[i] === '--scene' && args[i+1]) tag = args[i+1];
    }

    runValidation(trigger, tag);
}

module.exports = { runValidation };
