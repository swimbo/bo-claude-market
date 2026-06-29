---
name: handwritten-notes
description: >
  Transcribes handwritten notes scanned by ScanSnap into Obsidian markdown.
  Use this skill whenever the user mentions scanning notes, transcribing handwriting,
  processing ScanSnap PDFs, or saving scanned pages to Obsidian. Triggers for:
  "transcribe my notes", "process my scans", "add scans to Obsidian", "read my
  handwritten notes". Rasterizes each PDF page with pdftoppm, reads the handwritten
  date/letter corner label (e.g. "02/13 a", "3/10a") to determine canonical date
  and page order, groups and sorts pages by label, writes one Obsidian note per
  canonical date. Uses a vision model via LM Studio (local only -- no cloud models).
version: 1.0.0
author: Bo / Game Plan Tech
license: MIT
metadata:
  hermes:
    tags: [obsidian, scansnap, handwriting, ocr, notes, local-ai, lm-studio]
    related_skills: [obsidian, voice-notes, ocr-and-documents]
compatibility: "Python: openai, pypdf. System: pdftoppm (brew install poppler). LM Studio running with a vision model loaded."
---

# Handwritten Notes -> Obsidian

Converts ScanSnap handwritten note PDFs into Obsidian markdown notes.

## Key Design Decisions

**Corner label is authoritative.** Each page has a handwritten label like `02/13 a`
or `3/10a` in the corner. This -- not the PDF filename date -- determines the canonical
date and page order. A single scan session can contain pages from multiple dates.

**Local only.** Vision model via LM Studio. No cloud models, no fallback. Stops with
a clear error if LM Studio is not running.

**One API call per page** handles both corner label extraction and body transcription.

**Startup load check + retry on eviction.** Checks model state once before the run;
loads if idle. If evicted mid-run, catches the error, reloads, retries that page.

## Environment Variables

Set these in `~/.zshrc` or `~/.bashrc`:

```bash
export SCANSNAP_DIR="$HOME/Documents/ScanSnap/Processed/"
export OBSIDIAN_INBOX="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Scratch/000 Inbox/"
export LM_STUDIO_BASE="http://127.0.0.1:1234"
export LM_STUDIO_MODEL_ID="gemma-4-31b-it-mlx"   # match what LM Studio shows
export LM_STUDIO_LOAD_TIMEOUT="300"               # seconds, optional
```

Defaults are shown above. Only override what differs on your machine.

## Corner Label Format

Bo writes a label in any corner of each page:
- `02/13 a` -- Feb 13, page a
- `3/10a` -- Mar 10, page a (no leading zero, no space)
- `3/11 b`, `3/11 c` -- Mar 11, pages b and c
- Letter is always lowercase a-z; year inferred (rolls back if >30 days future)

## PDF Discovery

Prefers individual page files (`MMDDYYYY_NNN.pdf`). Falls back to multi-page combined
session files (`MMDDYYYY.pdf`) if no individual pages exist for that scan date.

## Output Format

One file per canonical date: `YYYYMMDD_Handwritten_Notes.md`

```markdown
---
date: 2026-02-13
type: handwritten-note
source: ScanSnap
source_files: [02092026_001.pdf, 02092026_002.pdf]
pages: 2
tags: [handwritten, inbox]
---

# Handwritten Notes -- February 13, 2026

---
*Page A*

{transcribed content page a}

---
*Page B*

{transcribed content page b}
```

## Setup (one-time)

```bash
# Install dependencies
pip install openai pypdf
brew install poppler   # provides pdftoppm

# Set env vars in your shell profile (see above)

# Verify model ID matches what LM Studio shows
curl -s http://127.0.0.1:1234/api/v1/models | python3 -c "
import json,sys; data=json.load(sys.stdin)
[print(m.get('key') or m.get('id','?')) for m in data.get('models', data.get('data',[]))]"
```

## Running

```bash
# All unprocessed scans
python3 scripts/transcribe_handwritten.py

# Specific date only
python3 scripts/transcribe_handwritten.py 2026-02-13
```

## Edge Cases

| Situation | Handling |
|---|---|
| Pages scanned out of order | Sorted by letter (a->b->c) within each date group |
| Same date across multiple scan sessions | Merged into one note |
| Model idle at startup | Loaded once before run begins |
| Model evicted mid-run | Caught, reloaded, page retried once |
| No corner label found | Flagged in output, NOT written to Obsidian |
| Blank page | Detected by model, skipped |
| Date >30 days in future | Year rolled back to previous year |
| Already-processed date in Obsidian | Skipped |

## Troubleshooting

| Problem | Fix |
|---|---|
| `pdftoppm: command not found` | `brew install poppler` |
| LM Studio server not running | LM Studio -> Developer tab -> Start Server |
| Wrong model ID | Run curl command above; update `LM_STUDIO_MODEL_ID` env var |
| Load timeout | Increase `LM_STUDIO_LOAD_TIMEOUT`; check LM Studio memory |
| Label not detected | Check `/tmp/ss_*.png` -- corner may be cropped or very faint |
| Wrong year | Edit `date:` frontmatter in Obsidian |
| Permission denied on Obsidian path | System Settings -> Privacy & Security -> Files and Folders |
