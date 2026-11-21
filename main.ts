// news-image-20261120 — 50 stories in one image.
// Node 22, standard library only. The finished artwork is entry.png
// in this same directory; this program places it into the output
// directory (/output, or MAKEFUN_OUTPUT_DIR when set), along with the
// 16 source illustrations the entry was composed from.
// 50 stories = 4 hero + 12 Tier A + 34 brief.
// Hero: AI meltdown (Nasdaq -5.2%), GTA VI $3.79B day one,
// Russia hits Ukraine and Poland, Trump-Xi-Putin no nukes.
// Tier A (12): Anthropic falls 9%, Myanmar rejects ICJ ruling,
// COP31 splits over fossil fuels, Nvidia CEO Huang resigns,
// Microsoft 365 down worldwide, EU Commission hit by cyberattack,
// Google sends AI servers to orbit, Meta's Muse leaks private chats,
// Claude cracks black holes, cyclones peak faster, tanker burns in
// Hormuz Strait, Rosalía's LUX wins 3 Latin Grammys.
// World map with 50 numbered pins; 34-brief index in 3 columns;
// UTC timeline; date-check box. Total 1022/1024.
// The gate takes a whole PNG or JPEG of at most 1 MiB, 1024x1024 px.

import { copyFileSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const artwork = new URL("./entry.png", import.meta.url);
const dest = join(outDir, "entry.png");

const illustrations = [
  "hero1-meltdown.png",
  "hero2-gtavi.png",
  "hero3-ukraine.png",
  "hero4-summit.png",
  "strip01-anthropic.png",
  "strip02-icj.png",
  "strip03-cop31.png",
  "strip04-huang.png",
  "strip05-microsoft.png",
  "strip06-eucyber.png",
  "strip07-suncatcher.png",
  "strip08-muse.png",
  "strip09-blackhole.png",
  "strip10-cyclone.png",
  "strip11-hormuz.png",
  "strip12-rosalia.png",
];

for (const name of illustrations) {
  const src = new URL(`./${name}`, import.meta.url);
  const dst = join(outDir, name);
  copyFileSync(src, dst);
  const s = statSync(src).size;
  const d = statSync(dst).size;
  if (d !== s) {
    throw new Error(`${name} copy size mismatch: ${d} != ${s}`);
  }
}

copyFileSync(artwork, dest);

const srcSize = statSync(artwork).size;
const dstSize = statSync(dest).size;
if (dstSize !== srcSize) {
  throw new Error(`entry.png copy size mismatch: ${dstSize} != ${srcSize}`);
}

// Verify the bytes are a 1024x1024 PNG: check the 8-byte PNG
// signature, then width/height from the IHDR chunk (bytes 16-23).
const bytes = readFileSync(dest);
const pngSig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(pngSig)) {
  throw new Error("entry.png is not a PNG (bad signature)");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png dimensions ${width}x${height}, expected 1024x1024`);
}
console.log(`entry.png copied OK (${dstSize} bytes, ${width}x${height}) -> ${dest}`);
console.log(`illustrations copied OK (${illustrations.length} files) -> ${outDir}`);
console.log(`total files written: ${illustrations.length + 1} (entry.png + ${illustrations.length} illustrations)`);
