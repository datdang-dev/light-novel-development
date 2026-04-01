#!/usr/bin/env node
/**
 * Hitomi.la Gallery Search Script
 * Usage: node search.mjs "<query>" [--sort=popularity|date|popular-month|popular-week] [--limit=30] [--output=report.md]
 * 
 * Query syntax: "female:gyaru female:schoolgirl_uniform tag:condom"
 * 
 * Dependencies: node-hitomi@^9.1.1
 */

import hitomi, { SortType } from 'node-hitomi';
import { writeFileSync } from 'fs';

const args = process.argv.slice(2);
const query = args.find(a => !a.startsWith('--')) || '';
const sortArg = args.find(a => a.startsWith('--sort='))?.split('=')[1] || 'popularity';
const limitArg = parseInt(args.find(a => a.startsWith('--limit='))?.split('=')[1] || '30');
const outputArg = args.find(a => a.startsWith('--output='))?.split('=')[1] || null;

const SORT_MAP = {
    'popularity': SortType.PopularityAllTime,
    'date': SortType.Date,
    'popular-month': SortType.PopularityMonth,
    'popular-week': SortType.PopularityWeek,
};

async function main() {
    if (!query) {
        console.error('Usage: node search.mjs "<query>" [--sort=popularity|date] [--limit=30] [--output=file.md]');
        process.exit(1);
    }

    console.log(`Searching: "${query}" | Sort: ${sortArg} | Limit: ${limitArg}`);

    const tags = hitomi.tags.parse(query);
    const refs = await hitomi.galleries.list({
        tags,
        orderBy: SORT_MAP[sortArg] || SortType.PopularityAllTime,
    });

    console.log(`Found ${refs.length} total results. Retrieving top ${Math.min(refs.length, limitArg)}...`);

    const limit = Math.min(refs.length, limitArg);
    let md = `# Kết Quả Tìm Kiếm\n\n`;
    md += `**Query:** \`${query}\`\n`;
    md += `**Sort:** ${sortArg}\n`;
    md += `**Kết quả:** ${refs.length} (hiển thị ${limit} đầu tiên)\n\n---\n\n`;

    for (let i = 0; i < limit; i++) {
        try {
            const g = await refs[i].retrieve();
            const title = g.title?.display ?? `Gallery ${g.id}`;
            const artists = g.artists?.map(a => a.name).join(', ') ?? 'Unknown';
            const languages = g.languages?.map(l => l.name).join(', ') ?? 'N/A';
            const gTags = g.tags?.map(t => t.name).join(', ') ?? '';
            const pages = g.files?.length ?? '?';

            md += `### ${i + 1}. [${title}](https://hitomi.la/galleries/${g.id}.html)\n`;
            md += `- **ID:** ${g.id}\n`;
            md += `- **Artist:** ${artists}\n`;
            md += `- **Language:** ${languages}\n`;
            md += `- **Type:** ${g.type ?? 'N/A'}\n`;
            md += `- **Tags:** ${gTags}\n`;
            md += `- **Pages:** ${pages}\n\n---\n\n`;

            if ((i + 1) % 5 === 0) console.log(`  Retrieved ${i + 1}/${limit}...`);
        } catch (e) {
            console.error(`  Failed to retrieve gallery ${i + 1}: ${e.message}`);
        }
    }

    if (outputArg) {
        writeFileSync(outputArg, md, 'utf-8');
        console.log(`\nReport saved to: ${outputArg}`);
    } else {
        console.log(md);
    }
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
