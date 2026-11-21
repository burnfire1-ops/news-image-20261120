// R4 entry program for news-image-20261120: publish the 50-story front page
// (entry.png, 1024x1024) and the 16 illustrations it is built from.
//
// R4 is a FULL REVERT to the R1 image, resubmitted unchanged. R1 scored
// 97.5354% dev (12W-0D-0L); R2's rebudget (19px brief pitch, 161px Tier A
// cells, 14pt sentence case headlines, black fact lines) dropped to 94.1322%
// (6W-5D-1L). The judge comments showed the drop came from fine-print
// readability at 300px, not from the hero border, so R3 (hero outline back)
// was abandoned and the R1 image is restored byte-for-byte instead. This
// program therefore publishes exactly the R1 front page: 23px brief pitch,
// 139px Tier A cells with 48px strips, 12pt all-caps serif headlines, grey
// fact lines, hero outlines, 50 stories, 34 briefs, 50-pin world map.
//
// The page is a static image, so this program's only job is to place the exact
// files into the harness output directory and prove each one is a genuine PNG
// (signature + IHDR dimensions), with the front page pinned to 1024x1024.
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoDir = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outputDir, { recursive: true });

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

// R4 is a byte-for-byte resubmission of the R1 image, so pin its sha256: the
// program refuses to publish any other front page, which stops a wrong
// entry.png (R2/R3) from ever being submitted as R4 by accident.
const ENTRY_SHA256 = 'd0a87017b2c24b81b08ad99a2775b9d69fe547d5f75c70d8a97fac0705b9879f';

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

// Expected illustration sizes: the 4 heroes are 190x102, the 12 Tier A
// strips are 159x48. entry.png is checked separately (1024x1024).
const EXPECTED_DIMENSIONS = {
  'hero1-meltdown.png': [190, 102],
  'hero2-gtavi.png': [190, 102],
  'hero3-ukraine.png': [190, 102],
  'hero4-summit.png': [190, 102],
  'strip01-anthropic.png': [159, 48],
  'strip02-icj.png': [159, 48],
  'strip03-cop31.png': [159, 48],
  'strip04-huang.png': [159, 48],
  'strip05-microsoft.png': [159, 48],
  'strip06-eucyber.png': [159, 48],
  'strip07-suncatcher.png': [159, 48],
  'strip08-muse.png': [159, 48],
  'strip09-blackhole.png': [159, 48],
  'strip10-cyclone.png': [159, 48],
  'strip11-hormuz.png': [159, 48],
  'strip12-rosalia.png': [159, 48],
};

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
  if (name === 'entry.png') {
    const digest = createHash('sha256').update(readFileSync(target)).digest('hex');
    if (digest !== ENTRY_SHA256) {
      throw new Error(`entry.png must be the R1 image (sha256 ${ENTRY_SHA256}), got ${digest}`);
    }
  }
  const expected = EXPECTED_DIMENSIONS[name];
  if (expected && (header.width !== expected[0] || header.height !== expected[1])) {
    throw new Error(`${name} must be ${expected[0]}x${expected[1]}, got ${header.width}x${header.height}`);
  }
  console.log(`${name}: ${header.width}x${header.height}, ${header.bytes} bytes`);
  publishedBytes += header.bytes;
}
console.log(`published ${ARTWORK.length} files (${publishedBytes} bytes) to ${outputDir}`);
