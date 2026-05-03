const fs = require('fs');
const path = require('path');

const transFilePath = '/mnt/d/nsfw_stuff/BigTitsPartyNTRSver1.12/爆乳パーティーNTR 体験版Sver1.12/ManualTransFile.json';
const outputDir = '/home/datdang/working/lnd_dev/_lnd-output/_analysis/scene_scripts';

// The pattern we are looking for is EV[0-9]{2}
// The translation file has keys like "EV01", "EV02" etc. We want to extract
// all text between these markers.

function extractScenes() {
    try {
        console.log(`Loading translation file from ${transFilePath}...`);
        const data = JSON.parse(fs.readFileSync(transFilePath, 'utf8'));
        const keys = Object.keys(data);
        
        console.log(`File loaded. Total keys: ${keys.length}`);
        
        let currentScene = "Prologue";
        let sceneContent = [];
        let sceneFilesCreated = 0;
        
        // Helper function to save a scene
        const saveScene = (sceneName, textLines) => {
            if (textLines.length === 0) return;
            // Clean up lines: ignore system keys, single character english letters, and empty lines
            const cleanedLines = textLines.filter(line => {
                if (typeof line !== 'string') return false;
                if (line.trim() === '') return false;
                if (line.match(/^[a-zA-Z0-9_\-<>:=]+$/)) return false; // System keys
                if (line.length < 2 && line.match(/[a-zA-Z]/)) return false; // Single letters
                return true;
            });
            
            if (cleanedLines.length === 0) return;
            
            const fileName = `${sceneName}.md`;
            const filePath = path.join(outputDir, fileName);
            
            let markdown = `# Scene: ${sceneName}\n\n`;
            markdown += `## Raw Translated Text\n\n`;
            cleanedLines.forEach(line => {
                markdown += `${line.replace(/\\\\n/g, ' ')}\n`;
            });
            
            fs.writeFileSync(filePath, markdown);
            console.log(`Saved: ${fileName} (${cleanedLines.length} lines)`);
            sceneFilesCreated++;
        };
        
        for (let i = 0; i < keys.length; i++) {
            const key = keys[i];
            const val = data[key];
            
            // Check if this key indicates a new EV event (e.g., "EV01", "EV12")
            if (typeof val === 'string' && val.match(/^EV[0-9]{2}[A-Za-z_0-9]*$/) && val.length < 15) {
                // We found a new anchor point. Save the previous scene.
                if (sceneContent.length > 0) {
                    saveScene(currentScene, sceneContent);
                }
                currentScene = val;
                sceneContent = [];
                continue;
            }
            
            // If it's not a new scene marker, add the translated value to the current scene
            if (typeof val === 'string' && val.trim() !== '') {
                sceneContent.push(val);
            }
        }
        
        // Save the last scene
        if (sceneContent.length > 0) {
            saveScene(currentScene, sceneContent);
        }
        
        console.log(`\nExtraction Complete! Converted translation file into ${sceneFilesCreated} scene scripts.`);
        console.log(`Check the output directory: ${outputDir}`);
        
    } catch (e) {
        console.error("Error during extraction:", e);
    }
}

extractScenes();
