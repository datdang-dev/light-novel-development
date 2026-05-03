#!/usr/bin/env node
/**
 * Hitomi.la Gallery Downloader
 * Usage: node download.mjs <gallery_id> [--output-dir=path] [--format=webp|jpg|png]
 * 
 * Features:
 * - Resumable (skips existing files)
 * - Auto-retry on failure (1 retry with 2s delay)
 * - Progress reporting
 * 
 * Dependencies: node-hitomi@^9.1.1
 */

import hitomi, { Extension } from 'node-hitomi';
import { writeFileSync, existsSync, mkdirSync } from 'fs';
import path from 'path';

const args = process.argv.slice(2);
const galleryId = parseInt(args.find(a => !a.startsWith('--')));
const outputDir = args.find(a => a.startsWith('--output-dir='))?.split('=')[1];
const format = args.find(a => a.startsWith('--format='))?.split('=')[1] || 'webp';

const EXT_MAP = {
    'webp': Extension.Webp,
    'jpg': Extension.Jpg,
    'png': Extension.Png,
};

async function main() {
    if (!galleryId || isNaN(galleryId)) {
        console.error('Usage: node download.mjs <gallery_id> [--output-dir=path] [--format=webp]');
        process.exit(1);
    }

    console.log(`Retrieving gallery ${galleryId}...`);
    const gallery = await hitomi.galleries.retrieve(galleryId);
    
    const title = gallery.title?.display ?? `Gallery_${galleryId}`;
    const safeTitle = title.replace(/[\/\?<>\\:\*\|":]/g, '').replace(/\s+/g, '_');
    const outDir = outputDir || path.join(process.cwd(), '..', 'sources', 'manga', safeTitle);
    
    if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });
    
    console.log(`Title: ${title}`);
    console.log(`Pages: ${gallery.files.length}`);
    console.log(`Output: ${outDir}`);
    console.log(`Format: ${format}\n`);

    let success = 0, skipped = 0, failed = 0;

    for (let i = 0; i < gallery.files.length; i++) {
        const pageNum = String(i + 1).padStart(3, '0');
        const outPath = path.join(outDir, `page_${pageNum}.${format}`);

        if (existsSync(outPath)) {
            skipped++;
            continue;
        }

        try {
            const buffer = await gallery.files[i].fetch(EXT_MAP[format] || Extension.Webp);
            writeFileSync(outPath, buffer);
            success++;
            if ((success + skipped) % 10 === 0) {
                console.log(`[${success + skipped}/${gallery.files.length}] Downloaded...`);
            }
        } catch (e) {
            // Retry once
            try {
                await new Promise(r => setTimeout(r, 2000));
                const buffer = await gallery.files[i].fetch(EXT_MAP[format] || Extension.Webp);
                writeFileSync(outPath, buffer);
                success++;
            } catch (e2) {
                failed++;
                console.error(`[page_${pageNum}] Failed: ${e2.message}`);
            }
        }
    }

    console.log(`\n✅ Done!`);
    console.log(`   Downloaded: ${success}`);
    console.log(`   Skipped:    ${skipped}`);
    console.log(`   Failed:     ${failed}`);
    console.log(`   Total:      ${gallery.files.length}`);
    console.log(`   Output:     ${outDir}`);
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
