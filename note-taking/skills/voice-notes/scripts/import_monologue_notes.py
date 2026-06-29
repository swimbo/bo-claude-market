#!/usr/bin/env python3
"""
import_monologue_notes.py
Monologue voice notes -> Obsidian markdown notes.

Uses the official monologue CLI (github.com/EveryInc/monologue-toolkit)
to fetch notes via the Notes public API, then writes formatted markdown
to the Obsidian inbox.

Prerequisites:
  - monologue CLI installed (see SKILL.md for install steps)
  - Run 'monologue onboarding' once to configure your API key
  - API key from: Monologue -> Settings -> Notes -> API

Environment variables (set in ~/.zshrc or ~/.bashrc):
  OBSIDIAN_INBOX   Path to Obsidian inbox folder

Usage:
    python3 import_monologue_notes.py                  # all unimported notes
    python3 import_monologue_notes.py 2026-02-13       # specific date only
    python3 import_monologue_notes.py --dry-run        # preview without writing
"""
import os, sys, json, re, subprocess, glob
from datetime import datetime

# ── Configuration ─────────────────────────────────────────────────────────────

OBSIDIAN_INBOX = os.environ.get("OBSIDIAN_INBOX",
                    os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Scratch/000 Inbox/"))

# ── CLI helpers ───────────────────────────────────────────────────────────────

def check_cli():
    result = subprocess.run(["which", "monologue"], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: monologue CLI is not installed.")
        print()
        print("Install:")
        print("  curl -fsSL https://raw.githubusercontent.com/EveryInc/monologue-toolkit/main/install.sh | sh")
        print("  # or with Go:")
        print("  go install github.com/EveryInc/monologue-toolkit/cli/cmd/monologue@latest")
        print()
        print("Then onboard:")
        print("  monologue onboarding")
        sys.exit(1)


def list_notes():
    result = subprocess.run(
        ["monologue", "notes", "list", "--json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        result = subprocess.run(["monologue", "notes", "list"], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"monologue notes list failed: {result.stderr.strip() or result.stdout.strip()}")
        return parse_plain_list(result.stdout)
    try:
        data = json.loads(result.stdout)
        # handle both {items: [...]} and plain list
        if isinstance(data, list):
            return data
        return data.get("items", data.get("notes", []))
    except json.JSONDecodeError:
        return parse_plain_list(result.stdout)


def get_note(note_id):
    result = subprocess.run(
        ["monologue", "notes", "get", note_id, "--json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        result = subprocess.run(
            ["monologue", "notes", "get", note_id],
            capture_output=True, text=True
        )
    if result.returncode != 0:
        raise RuntimeError(f"monologue notes get {note_id} failed: {result.stderr.strip()}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout.strip()}


def parse_plain_list(text):
    notes = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        uuid_match = re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', line)
        if uuid_match:
            notes.append({"note_id": uuid_match.group(), "raw": line})
    return notes

# ── Obsidian helpers ──────────────────────────────────────────────────────────

def already_imported(note_id):
    for md_file in glob.glob(os.path.join(OBSIDIAN_INBOX, "*_voice_note_*.md")):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                if note_id in f.read():
                    return True
        except Exception:
            pass
    return False


def get_output_path(dt, title_slug="voice_note"):
    base = f"{dt.strftime('%Y%m%d')}_{title_slug}_{dt.strftime('%H%M')}"
    path = os.path.join(OBSIDIAN_INBOX, f"{base}.md")
    if not os.path.exists(path):
        return path
    n = 2
    while True:
        path = os.path.join(OBSIDIAN_INBOX, f"{base}_{n}.md")
        if not os.path.exists(path):
            return path
        n += 1


def slugify(text, max_len=30):
    slug = re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')
    return slug[:max_len] if slug else "voice_note"


def extract_datetime(note):
    for field in ["created_at", "date", "createdAt", "timestamp", "datetime"]:
        val = note.get(field)
        if val:
            for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ",
                        "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                try:
                    return datetime.strptime(val[:26].rstrip("Z"), fmt.rstrip("Z"))
                except ValueError:
                    continue
    return None


def format_note(note, dt):
    note_id      = note.get("note_id", note.get("id", "unknown"))
    title        = note.get("title", "Voice Note")
    summary      = (note.get("summary") or "").strip()
    transcript   = (note.get("transcript") or note.get("text") or note.get("raw", "")).strip()
    duration     = note.get("duration", "")
    participants = note.get("participants", "")

    date_str     = dt.strftime("%Y-%m-%d")
    time_str     = dt.strftime("%H:%M")
    date_display = dt.strftime("%B %d, %Y")
    time_display = dt.strftime("%-I:%M %p")

    fm_lines = ["---", f"date: {date_str}", f"time: {time_str}",
                "type: voice-note", "source: Monologue", f"note_id: {note_id}"]
    if duration:
        fm_lines.append(f"duration: {duration}")
    if participants:
        fm_lines.append(f"participants: {participants}")
    fm_lines += ["tags: [voice-note, inbox]", "---"]

    sections = ["\n".join(fm_lines), "", f"# {title} -- {date_display}"]

    if summary:
        sections += ["", "## Summary", "", summary]
    if transcript:
        sections += ["", "## Transcript", "", transcript]
    elif not summary:
        sections += ["", "*(No transcript available)*"]

    return "\n".join(sections) + "\n"

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    target_date = next((a for a in args if re.match(r'\d{4}-\d{2}-\d{2}', a)), None)

    print(f"OBSIDIAN_INBOX: {OBSIDIAN_INBOX}\n")

    if dry_run:
        print("DRY RUN -- no files will be written.\n")

    check_cli()

    print("Fetching note list from Monologue API...")
    try:
        notes = list_notes()
    except RuntimeError as e:
        print(f"ERROR: {e}")
        print("\nIf you see an auth error, re-run: monologue onboarding")
        sys.exit(1)

    if not notes:
        print("No notes found. Check that Monologue has notes and the API key is valid.")
        return

    print(f"Found {len(notes)} note(s).\n")

    imported, skipped, errors = 0, 0, 0

    for note_stub in notes:
        note_id = note_stub.get("note_id") or note_stub.get("id")
        if not note_id:
            print(f"  Note missing ID -- skipping.")
            errors += 1
            continue

        if already_imported(note_id):
            skipped += 1
            continue

        try:
            note = get_note(note_id)
        except RuntimeError as e:
            print(f"  {note_id}: {e}")
            errors += 1
            continue

        dt = extract_datetime(note) or extract_datetime(note_stub)
        if not dt:
            print(f"  {note_id}: no parseable date -- skipping.")
            errors += 1
            continue

        if target_date and dt.strftime("%Y-%m-%d") != target_date:
            continue

        title = note.get("title", "Voice Note")
        print(f"  {dt.strftime('%Y-%m-%d %H:%M')}  {title[:60]}")

        if not dry_run:
            content = format_note(note, dt)
            slug = slugify(title)
            out_path = get_output_path(dt, title_slug=slug)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"    -> {os.path.basename(out_path)}")

        imported += 1

    print(f"\nDone. {imported} imported, {skipped} already in Obsidian, {errors} skipped.")
    if dry_run and imported > 0:
        print("(Dry run -- run without --dry-run to write files.)")


if __name__ == "__main__":
    main()
