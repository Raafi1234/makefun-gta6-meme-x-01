// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry itself is a public post on X: a GTA 6 meme whose picture carries
// make.fun's ghost mascot, posted with make.fun and the entrant's play code in
// its text. This program's whole job is to hand the post's address to the
// grader: it copies POST.json from the repository root (MAKEFUN_BOT_DIR,
// /bot inside the grader) into the output directory (MAKEFUN_OUTPUT_DIR,
// /output inside the grader), where the entry_link check reads it.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

try {
  copyFileSync(source, target);
} catch (err) {
  console.error(`could not copy POST.json from ${source}: ${(err as Error).message}`);
  process.exit(1);
}

console.log(`POST.json handed in from ${source}`);
