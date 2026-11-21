// news-image-20261120 entrypoint: publish the 50-story front page + its 16 illustrations.
//
// The entry is a single 1024x1024 PNG (entry.png) plus the 16 illustration PNGs
// it was composed from (4 heroes, 12 Tier A strips). This script copies them
// into the harness output directory and verifies each one is a real PNG.
import { copyFileSync, statSync, readFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(out, { recursive: true });

// [source in this repo, destination name in the output dir]
const FILES = [
  ['entry.png', 'entry.png'],
  ['hero1-meltdown.png', 'hero1-meltdown.png'],
  ['hero2-gtavi.png', 'hero2-gtavi.png'],
  ['hero3-ukraine.png', 'hero3-ukraine.png'],
  ['hero4-summit.png', 'hero4-summit.png'],
  ['strip01-anthropic.png', 'strip01-anthropic.png'],
  ['strip02-icj.png', 'strip02-icj.png'],
  ['strip03-cop31.png', 'strip03-cop31.png'],
  ['strip04-huang.png', 'strip04-huang.png'],
  ['strip05-microsoft.png', 'strip05-microsoft.png'],
  ['strip06-eucyber.png', 'strip06-eucyber.png'],
  ['strip07-suncatcher.png', 'strip07-suncatcher.png'],
  ['strip08-muse.png', 'strip08-muse.png'],
  ['strip09-blackhole.png', 'strip09-blackhole.png'],
  ['strip10-cyclone.png', 'strip10-cyclone.png'],
  ['strip11-hormuz.png', 'strip11-hormuz.png'],
  ['strip12-rosalia.png', 'strip12-rosalia.png'],
];

// A real PNG starts with the 8-byte PNG signature and stores its width/height
// as big-endian uint32 at bytes 16-23 (IHDR). Reject anything else.
function checkPng(path, wantW, wantH) {
  const buf = readFileSync(path);
  const sig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (buf.length < 24 || !buf.subarray(0, 8).equals(sig)) {
    throw new Error(`not a PNG: ${path}`);
  }
  const w = buf.readUInt32BE(16);
  const h = buf.readUInt32BE(20);
  if (wantW !== undefined && (w !== wantW || h !== wantH)) {
    throw new Error(`bad size ${w}x${h} (want ${wantW}x${wantH}): ${path}`);
  }
  return { w, h, bytes: buf.length };
}

let totalBytes = 0;
for (const [srcName, dstName] of FILES) {
  const src = join(here, srcName);
  const dst = join(out, dstName);
  if (!existsSync(src)) throw new Error(`missing source: ${src}`);
  copyFileSync(src, dst);
  const info = checkPng(dst, srcName === 'entry.png' ? 1024 : undefined, srcName === 'entry.png' ? 1024 : undefined);
  if (srcName === 'entry.png') {
    console.log(`entry.png: ${info.w}x${info.h}, ${info.bytes} bytes`);
  }
  totalBytes += statSync(dst).size;
}
console.log(`published ${FILES.length} files (${totalBytes} bytes) to ${out}`);
