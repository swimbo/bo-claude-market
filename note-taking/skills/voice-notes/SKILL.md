---
name: voice-notes
description: >
  Fetches and imports Monologue voice note transcriptions into Obsidian markdown.
  Use this skill whenever the user mentions transcribing voice memos, processing
  voice notes, importing Monologue notes to Obsidian, or "add my voice notes to
  Obsidian". Uses the official Monologue CLI (monologue-toolkit by EveryInc) to
  fetch notes via the Notes public API, then writes formatted markdown to the
  Obsidian inbox. Triggers for: "import voice notes", "process monologue notes",
  "sync voice notes to obsidian", "transcribe my recordings".
version: 1.0.0
author: Bo / Game Plan Tech
license: MIT
metadata:
  hermes:
    tags: [obsidian, monologue, voice, transcription, notes, every]
    related_skills: [obsidian, handwritten-notes]
compatibility: "Requires monologue CLI (github.com/EveryInc/monologue-toolkit). Run 'monologue onboarding' once to configure API key."
---

# Voice Notes (Monologue) -> Obsidian

Fetches Monologue voice note transcriptions via the official CLI and writes them
to the Obsidian inbox as formatted markdown notes.

## App Details

**App:** Monologue by Every (monologue.to)
**Bundle ID:** com.zeitalabs.jottleai (legacy internal name)
**Transcription:** Local (Parakeet v3 via WhisperKit/argmax)
**API:** Public Notes API at notes.monologue.to -- read-only

## Environment Variables

Set in `~/.zshrc` or `~/.bashrc`:

```bash
export OBSIDIAN_INBOX="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Scratch/000 Inbox/"
```

The default shown above works for standard iCloud-synced Obsidian vaults on macOS.
Override if your vault lives elsewhere.

## Setup (one-time)

```bash
# 1. Install the monologue CLI
curl -fsSL https://raw.githubusercontent.com/EveryInc/monologue-toolkit/main/install.sh | sh
# or with Go:
go install github.com/EveryInc/monologue-toolkit/cli/cmd/monologue@latest
export PATH="$PATH:$(go env GOPATH)/bin"

# 2. Get an API key
# Monologue -> Settings -> Notes -> API -> Create key

# 3. Onboard (paste key when prompted)
monologue onboarding

# 4. Verify
monologue notes list --limit 5
```

## Running

```bash
# All unimported notes
python3 scripts/import_monologue_notes.py

# Specific date only
python3 scripts/import_monologue_notes.py 2026-02-13

# Preview without writing
python3 scripts/import_monologue_notes.py --dry-run
```

## Output Format

One file per note: `YYYYMMDD_{title-slug}_{HHMM}.md`

```markdown
---
date: 2026-02-13
time: 14:22
type: voice-note
source: Monologue
note_id: ebced294-6f70-475d-a9ef-cc2822924192
tags: [voice-note, inbox]
---

# Note Title -- February 13, 2026

## Summary

{summary text}

## Transcript

{full transcript text}
```

## Edge Cases

| Situation | Handling |
|---|---|
| Note already imported | Checked by note_id in frontmatter of existing files; skipped |
| Empty transcription | Skipped with warning |
| Multiple notes same date+time | Appends `_2`, `_3` to filename |
| Auth failure | Re-run `monologue onboarding` with a fresh API key |

## Troubleshooting

| Problem | Fix |
|---|---|
| `monologue: command not found` | Run install command above; check PATH |
| Auth / 401 error | Re-run `monologue onboarding`; get fresh key from Monologue app |
| No notes listed | Check API key is for Notes API (Monologue -> Settings -> Notes -> API) |
| Permission denied on Obsidian path | System Settings -> Privacy & Security -> Files and Folders |

## Related

- Official toolkit: https://github.com/EveryInc/monologue-toolkit
- Note URL format: `https://notes.monologue.to/u/{note-id}`
- The toolkit's own `skills/monologue-notes/` can also be installed directly for agent use
