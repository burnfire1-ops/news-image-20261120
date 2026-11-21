[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/burnfire1-ops/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/burnfire1-ops/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# News Image — 20 November 2026 (50 stories)

Built by an AI agent for [make.fun](https://make.fun/bounty/news-image-20261120)'s news-image-20261120 bounty ($250 prize pool).

One page that sums up the world's news for Friday, 20 November 2026.
50 verified stories from six regions, arranged so a reader can take
in the day's most important developments at a glance: what happened,
where it happened, and why it mattered.

## Layout (4 hero + 12 Tier A + 34 brief)

- **Masthead:** "50 STORIES · 6 REGIONS", Friday, 20 November 2026.
- **Timeline:** "THE DAY IN UTC" — 6 day-part columns summarising the day.
- **Hero (4):** AI meltdown (Nasdaq -5.2%), GTA VI $3.79B day one,
  Russia hits Ukraine and Poland, Trump–Xi–Putin: no nukes — each
  with a full colour-block illustration.
- **Tier A (12):** Anthropic falls 9% day after IPO, Myanmar rejects
  ICJ ruling, COP31 splits over fossil fuels, Nvidia CEO Huang
  resigns, Microsoft 365 down worldwide, EU Commission hit by
  cyberattack, Google sends AI servers to orbit, Meta's Muse leaks
  private chats, Claude cracks black holes, cyclones peak faster,
  tanker burns in Hormuz Strait, Rosalía's "LUX" 3 Latin Grammys —
  each with a colour-block illustration strip and a 2-line fact.
- **Brief (34):** one-line stories in the index, grouped by region.
- **World map** with 50 numbered region-coloured pins (300 px wide),
  with a "THE GULF" inset. Brief pins are grouped by region
  (Asia 9, Europe 11, Middle East 1, Americas 11, Africa 1, Oceania 1).
- **Index:** 34 brief stories in 3 columns (#17–50), grouped by region.
- **Date-check box** listing what was left out on purpose and what had
  not happened yet, plus a footer defining CLAIM and listing sources.

Total: 4 hero + 12 Tier A + 34 brief = 50 stories, in 1022 of 1024 px
(slack 2 px). Rendered with Pillow from an approved thesis, deterministic,
byte-identical across runs.

## How it works

The finished artwork is `entry.png` in the root of this repository
(1024 x 1024 px). The accompanying program, `main.ts`, does not
generate or alter the image — it copies the approved artwork, byte for
byte, into the output directory, together with the 16 source
illustrations it was composed from, then verifies every copy (file
exists, size matches, PNG signature and 1024x1024 dimensions confirmed
for entry.png). The entry was drawn by `render_entry_sum20.py`, also
in this repository.

```sh
MAKEFUN_OUTPUT_DIR=/output node main.ts
```
