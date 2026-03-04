const fs = require('fs');
const path = require('path');

const transFilePath = '/mnt/d/nsfw_stuff/BigTitsPartyNTRSver1.12/爆乳パーティーNTR 体験版Sver1.12/ManualTransFile.json';
const outputDir = '/home/datdang/working/lnd_dev/_lnd-output/_analysis/scene_scripts agricoles';

// Ensure fresh directory
if (fs.existsSync(outputDir)) {
    fs.rmSync(outputDir, { recursive: true, force: true });
}
fs.mkdirSync(outputDir);

function extractScenes() {
    try {
        console.log(`Loading translation file...`);
        const data = JSON.parse(fs.readFileSync(transFilePath, 'utf8'));
        const keys = Object.keys(data);
        
        let currentScene = "System_Data";
        let sceneContent = [];
        let sceneFilesCreated = 0;
        
        const saveScene = (sceneName, textLines) => {
            if (textLines.length === 0) return;
            const cleanedLines = textLines.filter(line => {
                if (typeof line !== 'string') return false;
                if (line.trim() === '') return false;
                if (line.match(/^[a-zA-Z0-9_\-<>:=]+$/)) return false; 
                if (line.length < 2 && line.match(/[a-zA-Z]/)) return false;
                return true;
            });
            
            if (cleanedLines.length === 0) return;
            
            const fileName = `${sceneName}.md`;
            const filePath = path.join(outputDir, fileName);
            
            let markdown = `# Section: ${sceneName}\n\n`;
            cleanedLines.forEach(line => {
                markdown += `${line.replace(/\\\\n/g, ' ')}\n`;
            });
            
            fs.writeFileSync(filePath, markdown);
            sceneFilesCreated++;
        };
        
        for (let i = 0; i < keys.length; i++) {
            const val = data[keys[i]];
            
            // We split on ANY key that looks like a map name, event name, or system section
            // e.g. "Map001", "EV01", "items", "skills"
            if (typeof val === 'string' && val.length < 25) {
                const isAnchor = 
                    val.match(/^EV[0-9]{2}[A-Za-z_0-9]*$/) || 
                    val.match(/^Map[0-9]{3}$/i) ||
                    (val.includes('System') && !val.includes(' ')) ||
                    val.match(/^Actor[0-9]+$/i) ||
                    val.match(/^Enemy[0-9]+$/i);
                    
                if (isAnchor) {
                    if (sceneContent.length > 0) {
                        saveScene(currentScene, sceneContent);
                    }
                    currentScene = val;
                    sceneContent = [];
                    continue;
                }
            }
            
            if (typeof val === 'string' && val.trim() !== '') {
                sceneContent.push(val);
            }
        }
        
        if (sceneContent.length > 0) {
            saveScene(currentScene, sceneContent);
        }
        
        console.log(`Extraction Complete! Converted translation file into ${sceneFilesCreated} segmented blocks.`);
        
    } catch (e) {
        console.error("Error during extraction:", e);
    }
}

extractScenes();
