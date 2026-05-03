const fs = require('fs');
const path = require('path');

let Ajv;
try {
    Ajv = require('ajv');
} catch (e) {
    console.error("❌ Mising dependency. Please run: npm install ajv");
    process.exit(1);
}

const colors = {
    reset: "\x1b[0m",
    green: "\x1b[32m",
    red: "\x1b[31m",
    yellow: "\x1b[33m",
    cyan: "\x1b[36m",
    bold: "\x1b[1m"
};

function runSchemaValidation(schemaPath, dataPath) {
    console.log(`\n${colors.cyan}${colors.bold}============================================================${colors.reset}`);
    console.log(`${colors.cyan}${colors.bold}  LND STUDIO - DYNAMIC SCHEMA VALIDATOR                     ${colors.reset}`);
    console.log(`${colors.cyan}${colors.bold}============================================================${colors.reset}\n`);

    if (!fs.existsSync(schemaPath)) {
        console.log(`${colors.red}✖ Schema file not found: ${schemaPath}${colors.reset}`);
        process.exit(1);
    }
    if (!fs.existsSync(dataPath)) {
        console.log(`${colors.red}✖ Data file not found: ${dataPath}${colors.reset}`);
        process.exit(1);
    }

    console.log(`${colors.bold}Loading Schema:${colors.reset} ${path.basename(schemaPath)}`);
    console.log(`${colors.bold}Loading Target:${colors.reset} ${path.basename(dataPath)}\n`);

    let schemaObj, dataObj;
    try {
        schemaObj = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
    } catch (e) {
        console.log(`${colors.red}✖ Schema is invalid JSON: ${e.message}${colors.reset}`);
        process.exit(1);
    }

    try {
        dataObj = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    } catch (e) {
        console.log(`${colors.red}✖ Target data is invalid JSON (Syntax Error):${colors.reset}`);
        console.log(`  ${e.message}`);
        console.log(`\n${colors.yellow}⚠ FIX: You must pass this error back to the LLM to correct the JSON syntax.${colors.reset}`);
        process.exit(1);
    }

    const ajv = new Ajv({ allErrors: true });
    
    // Add custom formats if your schemas use them (optional, but good for robust validation)
    // require("ajv-formats")(ajv); 

    let validate;
    try {
        validate = ajv.compile(schemaObj);
    } catch (e) {
         console.log(`${colors.red}✖ Failed to compile Schema: ${e.message}${colors.reset}`);
         process.exit(1);
    }

    const valid = validate(dataObj);

    if (valid) {
        console.log(`${colors.green}✔ VALIDATION PASSED.${colors.reset} Data strictly conforms to schema.`);
    } else {
        console.log(`${colors.red}✖ VALIDATION FAILED.${colors.reset} Schema Violations Found:\n`);
        
        validate.errors.forEach((err, idx) => {
            console.log(`  ${colors.red}${idx + 1}. Error at path "${err.instancePath || 'root'}":${colors.reset} ${err.message}`);
            // Provide context for missing properties or specific constraints
            if (err.params) {
                const paramsStr = Object.entries(err.params).map(([k, v]) => `${k}=${v}`).join(', ');
                console.log(`     ${colors.yellow}Context: [${paramsStr}]${colors.reset}`);
            }
        });

        console.log(`\n${colors.yellow}⚠ NEXT ACTION: Append these errors to the Agent's prompt and trigger a regeneration loop.${colors.reset}`);
    }
    
    console.log(`\n${colors.cyan}${colors.bold}============================================================${colors.reset}\n`);
}

const args = process.argv.slice(2);
if (args.length < 2) {
    console.log("Usage: node schema_validator.js <path/to/schema.json> <path/to/data.json>");
    process.exit(1);
}

runSchemaValidation(args[0], args[1]);
