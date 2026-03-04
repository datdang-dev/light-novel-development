const fs = require('fs');
const path = require('path');

const gameDir = '/mnt/d/nsfw_stuff/BigTitsPartyNTRSver1.12/爆乳パーティーNTR 体験版Sver1.12/www';
const outDir = '/home/datdang/working/lnd_dev/_lnd-output/_analysis/decrypted_assets';

const PNG_HEADER = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52]);

function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}

function findKey(sampleFile) {
    const data = fs.readFileSync(sampleFile);
    // RPGMaker MV Header is 16 bytes. The next 16 bytes are the encrypted PNG header.
    const encryptedHeader = data.slice(16, 32);
    const key = Buffer.alloc(16);
    for (let i = 0; i < 16; i++) {
        key[i] = encryptedHeader[i] ^ PNG_HEADER[i];
    }
    console.log(`Extracted Key: ${key.toString('hex')}`);
    return key;
}

function decryptFile(filePath, key, outFolder) {
    const ext = path.extname(filePath);
    let outExt = ext;
    if (ext === '.rpgmvp') outExt = '.png';
    else if (ext === '.rpgmvo') outExt = '.ogg';
    else if (ext === '.rpgmvm') outExt = '.m4a';
    else return; // unhandled extension

    const data = fs.readFileSync(filePath);
    const header = data.slice(0, 16);
    const signature = header.slice(0, 6).toString('ascii');
    if (signature !== "RPGMV\0" && signature !== "RPGMZ\0") {
        console.log(`Skipping non-RPGMV file: ${filePath}`);
        return;
    }

    const payload = data.slice(16);
    
    // Decrypt the first 16 bytes of the payload
    for (let i = 0; i < 16; i++) {
        payload[i] ^= key[i];
    }

    const outFile = path.join(outFolder, path.basename(filePath, ext) + outExt);
    fs.writeFileSync(outFile, payload);
}

function processDirectory(srcDir, destDir, key) {
    ensureDir(destDir);
    const items = fs.readdirSync(srcDir);
    for (const item of items) {
        const srcPath = path.join(srcDir, item);
        const destPath = path.join(destDir, item);
        const stat = fs.statSync(srcPath);
        if (stat.isDirectory()) {
            processDirectory(srcPath, destPath, key);
        } else {
            decryptFile(srcPath, key, destDir);
        }
    }
}

// 1. Find a key from any rpgmvp file
function getKeyFromAnyImage(dir) {
    const items = fs.readdirSync(dir);
    for (const item of items) {
        const fullPath = path.join(dir, item);
        if (fs.statSync(fullPath).isDirectory()) {
            const k = getKeyFromAnyImage(fullPath);
            if (k) return k;
        } else if (fullPath.endsWith('.rpgmvp')) {
            return findKey(fullPath);
        }
    }
    return null;
}

console.log("Starting decryption process...");
const imgDir = path.join(gameDir, 'img');
const audioDir = path.join(gameDir, 'audio');

ensureDir(outDir);
const key = getKeyFromAnyImage(imgDir);

if (!key) {
    console.error("Could not find any .rpgmvp file to extract key.");
    process.exit(1);
}

console.log("Decrypting Images...");
processDirectory(imgDir, path.join(outDir, 'img'), key);

if (fs.existsSync(audioDir)) {
    console.log("Decrypting Audio...");
    processDirectory(audioDir, path.join(outDir, 'audio'), key);
}

console.log("Decryption Complete! Assets saved to:", outDir);
