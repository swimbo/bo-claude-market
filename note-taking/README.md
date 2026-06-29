# note-taking

Imports handwritten ScanSnap notes and Monologue voice notes into Obsidian.

## Skills

### handwritten-notes
Transcribes ScanSnap PDFs into Obsidian markdown using a local LM Studio vision model.
- Reads the handwritten corner label (`MM/DD letter`) from each page for canonical date and order
- Groups pages by date, sorts by letter, writes one note per canonical date
- 100% local — no cloud models

### voice-notes
Imports Monologue voice note transcriptions into Obsidian via the official monologue CLI.
- Uses the Monologue Notes public API (read-only)
- Requires the `monologue` CLI installed and onboarded

## Environment Variables

Set in `~/.zshrc` or `~/.bashrc`:

```bash
# Shared
export OBSIDIAN_INBOX="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Scratch/000 Inbox/"

# handwritten-notes only
export SCANSNAP_DIR="$HOME/Documents/ScanSnap/Processed/"
export LM_STUDIO_BASE="http://127.0.0.1:1234"
export LM_STUDIO_MODEL_ID="gemma-4-31b-it-mlx"
```

## Setup

**Handwritten notes:**
```bash
pip install openai pypdf
brew install poppler
# Start LM Studio and load a vision model
```

**Voice notes:**
```bash
curl -fsSL https://raw.githubusercontent.com/EveryInc/monologue-toolkit/main/install.sh | sh
monologue onboarding   # paste API key from Monologue -> Settings -> Notes -> API
```

## Usage

```bash
python3 skills/handwritten-notes/scripts/transcribe_handwritten.py
python3 skills/voice-notes/scripts/import_monologue_notes.py
python3 skills/voice-notes/scripts/import_monologue_notes.py --dry-run
```
