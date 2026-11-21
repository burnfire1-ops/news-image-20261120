// R2 entry program for news-image-20261120: publish the rebudgeted 50-story
// front page (entry.png, 1024x1024) and the 16 illustrations it is built from.
//
// The page is a static image, so this program's only job is to place the exact
// files into the harness output directory and prove each one is a genuine PNG
// (signature + IHDR dimensions), with the front page pinned to 1024x1024.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoDir = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outputDir, { recursive: true });

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

// Every file shipped with the entry, in publish order: front page first,
// then the 4 hero illustrations, then the 12 Tier A strips.
const ARTWORK = [
  'entry.png',
  'hero1-meltdown.png',
  'hero2-gtavi.png',
  'hero3-ukraine.png',
  'hero4-summit.png',
  'strip01-anthropic.png',
  'strip02-icj.png',
  'strip03-cop31.png',
  'strip04-huang.png',
  'strip05-microsoft.png',
  'strip06-eucyber.png',
  'strip07-suncatcher.png',
  'strip08-muse.png',
  'strip09-blackhole.png',
  'strip10-cyclone.png',
  'strip11-hormuz.png',
  'strip12-rosalia.png',
];

// Read a file's PNG header: the signature must match, and width/height come
// from the IHDR chunk as big-endian uint32 at offsets 16 and 20.
function readPngHeader(filePath) {
  const data = readFileSync(filePath);
  if (data.length < 24 || !data.subarray(0, 8).equals(PNG_SIGNATURE)) {
    throw new Error(`not a PNG: ${filePath}`);
  }
  return { width: data.readUInt32BE(16), height: data.readUInt32BE(20), bytes: data.length };
}

let publishedBytes = 0;
for (const name of ARTWORK) {
  const source = join(repoDir, name);
  const target = join(outputDir, name);
  if (!existsSync(source)) {
    throw new Error(`missing artwork file: ${source}`);
  }
  copyFileSync(source, target);
  const header = readPngHeader(target);
  if (name === 'entry.png' && (header.width !== 1024 || header.height !== 1024)) {
    throw new Error(`entry.png must be 1024x1024, got ${header.width}x${header.height}`);
  }
  console.log(`${name}: ${header.width}x${header.height}, ${header.bytes} bytes`);
  publishedBytes += header.bytes;
}
console.log(`published ${ARTWORK.length} files (${publishedBytes} bytes) to ${outputDir}`);
