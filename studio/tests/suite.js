const fs = require('fs');
const path = require('path');
const yaml = require('yaml');

// Colors for output
const colors = {
    reset: "\x1b[0m",
    green: "\x1b[32m",
    red: "\x1b[31m",
    yellow: "\x1b[33m",
    cyan: "\x1b[36m",
    bold: "\x1b[1m"
};

const PROJECT_ROOT = path.resolve(__dirname, '../../');
const ORCHESTRATOR_PATH = path.join(PROJECT_ROOT, 'studio/agents/lnd-orchestrator.agent.yaml');
const AGENTS_DIR = path.join(PROJECT_ROOT, 'studio/agents');

// Global Stats
let globalStats = { pass: 0, fail: 0, warn: 0 };
let allMissingFiles = new Set();

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
        return null;
    }
}

function logResult(name, status, details = '') {
    if (status === 'PASS') {
        console.log(`  ${colors.green}✔ ${name}${colors.reset} ${details}`);
        globalStats.pass++;
    } else if (status === 'FAIL') {
        console.log(`  ${colors.red}✖ ${name}${colors.reset} ${details}`);
        globalStats.fail++;
    } else if (status === 'WARN') {
        console.log(`  ${colors.yellow}⚠ ${name}${colors.reset} ${details}`);
        globalStats.warn++;
    }
}

function extractDependenciesFromAction(actionStr) {
    const agents = [];
    const skills = [];
    
    // Match anything ending in .agent.yaml
    const agentMatches = actionStr.match(/([a-zA-Z0-9-]+\.agent\.yaml)/g);
    if (agentMatches) agents.push(...agentMatches);

    // Match core/.../SKILL.md or services/.../SKILL.md
    const skillMatches = actionStr.match(/(core\/[a-zA-Z0-9-]+\/SKILL\.md|services\/[a-zA-Z0-9-]+\/SKILL\.md)/g);
    if (skillMatches) skills.push(...skillMatches);

    return {
        agents: [...new Set(agents)],
        skills: [...new Set(skills)]
    };
}

function validateSkillDependencies(skillPath) {
    const fullPath = path.join(PROJECT_ROOT, 'studio', skillPath);
    if (!fileExists(fullPath)) {
        logResult(skillPath, 'FAIL', '(Skill file not found)');
        return;
    }

    const content = fs.readFileSync(fullPath, 'utf8');
    const meta = parseFrontmatter(content);
    if (!meta) {
        logResult(skillPath, 'WARN', '(No YAML frontmatter or parse error)');
        return;
    }

    logResult(skillPath, 'PASS');

    // Validate Injection Always
    if (meta.injection && meta.injection.always) {
        meta.injection.always.forEach(file => {
            const resolved = resolvePath(file);
            if (!fileExists(resolved)) {
                logResult(`Injection Always: ${path.basename(file)}`, 'FAIL', `(${file})`);
                allMissingFiles.add(resolved);
            } else {
                logResult(`Injection Always: ${path.basename(file)}`, 'PASS');
            }
        });
    }

    // Validate Injection Triggers
    if (meta.injection && meta.injection.triggers) {
        meta.injection.triggers.forEach(trigger => {
            if (trigger.loads) {
                trigger.loads.forEach(file => {
                    const resolved = resolvePath(file);
                    if (!fileExists(resolved)) {
                        logResult(`Injection Trigger [${trigger.scene_tag}]: ${path.basename(file)}`, 'FAIL', `(${file})`);
                        allMissingFiles.add(resolved);
                    } else {
                        logResult(`Injection Trigger [${trigger.scene_tag}]: ${path.basename(file)}`, 'PASS');
                    }
                });
            }
        });
    }

    // Validate Dependencies.Knowledge
    if (meta.dependencies && meta.dependencies.knowledge) {
        meta.dependencies.knowledge.forEach(k => {
            if (k.path) {
                const resolved = resolvePath(k.path);
                if (!fileExists(resolved)) {
                    logResult(`Knowledge Dep: ${path.basename(k.path)}`, 'FAIL', `(${k.path})`);
                    allMissingFiles.add(resolved);
                } else {
                    logResult(`Knowledge Dep: ${path.basename(k.path)}`, 'PASS');
                }
            }
        });
    }
}

function runFullSuite() {
    console.log(`\n${colors.cyan}${colors.bold}============================================================${colors.reset}`);
    console.log(`${colors.cyan}${colors.bold}  LND STUDIO v7.0 - FULL COVERAGE TEST SUITE${colors.reset}`);
    console.log(`${colors.cyan}${colors.bold}============================================================${colors.reset}\n`);

    // 1. Validate Orchestrator
    console.log(`${colors.bold}1. Orchestrator Configuration${colors.reset}`);
    if (!fileExists(ORCHESTRATOR_PATH)) {
        logResult('lnd-orchestrator.agent.yaml', 'FAIL', 'Not found');
        return;
    }
    
    let orchYaml;
    try {
        const orchContent = fs.readFileSync(ORCHESTRATOR_PATH, 'utf8');
        orchYaml = yaml.parse(orchContent);
        logResult('Parse lnd-orchestrator.agent.yaml', 'PASS');
    } catch (e) {
        logResult('Parse lnd-orchestrator.agent.yaml', 'FAIL', e.message);
        return;
    }

    // 2. Validate all Triggers in Menu
    const menu = orchYaml.agent?.menu || [];
    console.log(`\n${colors.bold}2. Menu Triggers Coverage (${menu.length} found)${colors.reset}`);
    
    let allFoundSkills = new Set();
    let allFoundAgents = new Set();

    menu.forEach(item => {
        console.log(`\n▶ Trigger: ${colors.cyan}${item.trigger}${colors.reset}`);
        if (!item.action) {
            logResult('Action Flow Definition', 'FAIL', 'Missing action block');
            return;
        }

        const deps = extractDependenciesFromAction(item.action);
        
        // Check Agents
        deps.agents.forEach(agentFile => {
            allFoundAgents.add(agentFile);
            if (fileExists(path.join(AGENTS_DIR, agentFile))) {
                logResult(`Agent: ${agentFile}`, 'PASS');
            } else {
                logResult(`Agent: ${agentFile}`, 'FAIL', '(Not found in studio/agents/)');
            }
        });

        // Collect Skills for deeper validation later
        deps.skills.forEach(skill => allFoundSkills.add(skill));
    });

    // 3. Deep Validate All Discovered Skills
    console.log(`\n${colors.bold}3. SKILL.md Dependencies & Injections (${allFoundSkills.size} found)${colors.reset}`);
    allFoundSkills.forEach(skillPath => {
        console.log(`\n▶ Skill Context: ${colors.cyan}${skillPath}${colors.reset}`);
        validateSkillDependencies(skillPath);
    });

    // 4. Validate Global Schemas
    console.log(`\n${colors.bold}4. JSON Schema Validation${colors.reset}`);
    const schemaDir = path.join(PROJECT_ROOT, 'studio/schemas');
    if (fileExists(schemaDir)) {
        const schemas = fs.readdirSync(schemaDir).filter(f => f.endsWith('.schema.json'));
        if (schemas.length === 0) {
            logResult('Schemas Directory', 'WARN', 'No .schema.json files found');
        }
        schemas.forEach(schemaFile => {
            try {
                JSON.parse(fs.readFileSync(path.join(schemaDir, schemaFile), 'utf8'));
                logResult(`Schema: ${schemaFile}`, 'PASS', '(Valid JSON)');
            } catch (e) {
                logResult(`Schema: ${schemaFile}`, 'FAIL', `Invalid JSON - ${e.message}`);
            }
        });
    } else {
        logResult('studio/schemas directory', 'WARN', 'Directory not found');
    }

    // Print Final Summary
    console.log(`\n${colors.cyan}${colors.bold}============================================================${colors.reset}`);
    console.log(`${colors.bold}TEST SUITE SUMMARY${colors.reset}`);
    console.log(`  Total Passed   : ${colors.green}${globalStats.pass}${colors.reset}`);
    console.log(`  Total Failed   : ${colors.red}${globalStats.fail}${colors.reset}`);
    console.log(`  Total Warnings : ${colors.yellow}${globalStats.warn}${colors.reset}`);
    
    if (globalStats.fail === 0) {
        console.log(`\n  ${colors.green}✔ PIPELINE IS FULLY CONSISTENT AND READY FOR PRODUCTION.${colors.reset}`);
    } else {
        console.log(`\n  ${colors.red}✖ PIPELINE HAS BROKEN DEPENDENCIES OR ERRORS.${colors.reset}`);
        console.log(`\n  ${colors.bold}Missing Files to Fix:${colors.reset}`);
        allMissingFiles.forEach(f => console.log(`  - ${f}`));
    }
    console.log(`${colors.cyan}${colors.bold}============================================================${colors.reset}\n`);
}

runFullSuite();
