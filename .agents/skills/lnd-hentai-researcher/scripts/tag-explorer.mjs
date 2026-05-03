#!/usr/bin/env node
/**
 * Hitomi.la Tag Explorer
 * Usage: node tag-explorer.mjs <term1> [term2] [term3] ... [--limit=10]
 * 
 * Searches for tag autocomplete results for each term.
 * 
 * Dependencies: node-hitomi@^9.1.1
 */

import hitomi from 'node-hitomi';

const args = process.argv.slice(2);
const terms = args.filter(a => !a.startsWith('--'));
const limitArg = parseInt(args.find(a => a.startsWith('--limit='))?.split('=')[1] || '10');

async function main() {
    if (terms.length === 0) {
        console.error('Usage: node tag-explorer.mjs <term1> [term2] ... [--limit=10]');
        process.exit(1);
    }

    console.log(`Exploring tags for: ${terms.join(', ')}\n`);

    for (const term of terms) {
        try {
            const results = await hitomi.tags.search(term);
            const top = results.slice(0, limitArg);
            
            console.log(`📌 "${term}" (${results.length} matches):`);
            for (const [tag, count] of top) {
                console.log(`   ${tag} — ${count.toLocaleString()} galleries`);
            }
            console.log();
        } catch (e) {
            console.error(`   Error for "${term}": ${e.message}`);
        }
    }
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
