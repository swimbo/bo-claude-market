#!/usr/bin/env python3
"""
transcribe_handwritten.py
ScanSnap PDFs → Obsidian markdown notes.

Reads handwritten corner label (MM/DD letter) from each page to determine
canonical date and sort order. Groups pages by date, sorts by letter, writes
one Obsidian note per canonical date.

Uses a vision model via LM Studio (local only). No cloud fallback.

Environment variables (set in ~/.zshrc or ~/.bashrc):
  SCANSNAP_DIR            Path to ScanSnap processed PDFs folder
  OBSIDIAN_INBOX          Path to Obsidian inbox folder
  LM_STUDIO_BASE          LM Studio server URL (default: http://127.0.0.1:1234)
  LM_STUDIO_MODEL_ID      Model identifier shown in LM Studio server tab
  LM_STUDIO_LOAD_TIMEOUT  Seconds to wait for model load (default: 300)

Usage:
    python3 transcribe_handwritten.py             # all unprocessed scans
    python3 transcribe_handwritten.py 2026-02-13  # specific date only
"""
import os, re, glob, subprocess, base64, json, sys, time, urllib.request
from datetime import date, datetime, timedelta
from collections import defaultdict
from pypdf import PdfReader

# ── Configuration (env vars with defaults) ────────────────────────────────────

SCANSNAP_DIR   = os.environ.get("SCANSNAP_DIR",
                    os.path.expanduser("~/Documents/ScanSnap/Processed/"))
OBSIDIAN_INBOX = os.environ.get("OBSIDIAN_INBOX",
                    os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Scratch/000 Inbox/"))
LM_STUDIO_BASE     = os.environ.get("LM_STUDIO_BASE", "http://127.0.0.1:1234")
LM_STUDIO_MODEL_ID = os.environ.get("LM_STUDIO_MODEL_ID", "gemma-4-31b-it-mlx")
LOAD_TIMEOUT       = int(os.environ.get("LM_STUDIO_LOAD_TIMEOUT", "300"))

EXTRACT_PROMPT = """This is a scanned handwritten note page.

TASK 1 - CORNER LABEL:
Look for a short handwritten label in any corner of the page.
Pattern: MM/DD letter  (e.g. "02/13 a", "3/10a", "3/11 b")
Month and day separated by a slash, then a lowercase letter. Space optional.

TASK 2 - TRANSCRIPTION:
Transcribe ALL handwritten text from the page body (not the corner label itself).
- Unclear but guessable: best guess + [unclear]
- Truly illegible: [illegible]
- Diagrams/drawings: [diagram: brief description]
- Blank/near-blank page: write exactly BLANK_PAGE
- Markdown formatting: # headings, - bullets, - [ ] checkboxes
- No interpretation or commentary -- raw transcription only

Return ONLY valid JSON, no markdown fences, no preamble:
{
  "label": {"month": 2, "day": 13, "letter": "a"},
  "transcription": "full transcribed text here..."
}
If label not found: set month/day/letter all to null."""

# ── LM Studio model management ────────────────────────────────────────────────

def lm_studio_reachable():
    try:
        urllib.request.urlopen(f"{LM_STUDIO_BASE}/api/v1/models", timeout=3)
        return True
    except Exception:
        return False


def get_model_info(model_id):
    req = urllib.request.urlopen(f"{LM_STUDIO_BASE}/api/v1/models", timeout=5)
    data = json.loads(req.read())
    models = data.get("models", data.get("data", []))
    for m in models:
        mid = m.get("key") or m.get("id") or ""
        if model_id.lower() in mid.lower() or mid.lower() in model_id.lower():
            return True, len(m.get("loaded_instances", [])) > 0
    return False, False


def load_model(model_id):
    print(f"  Loading {model_id} (~30-60s)...")
    payload = json.dumps({"model": model_id}).encode()
    req = urllib.request.Request(
        f"{LM_STUDIO_BASE}/api/v1/models/load",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    start = time.time()
    with urllib.request.urlopen(req, timeout=LOAD_TIMEOUT) as resp:
        result = json.loads(resp.read())
    print(f"  Loaded in {time.time() - start:.0f}s")
    return result.get("status") == "loaded"


def startup_check(model_id):
    print("Checking LM Studio model state...")
    found, is_loaded = get_model_info(model_id)
    if not found:
        req = urllib.request.urlopen(f"{LM_STUDIO_BASE}/api/v1/models", timeout=5)
        data = json.loads(req.read())
        models = data.get("models", data.get("data", []))
        ids = [m.get("key") or m.get("id", "?") for m in models]
        print(f"\nERROR: Model '{model_id}' not found. Available:")
        for i in ids:
            print(f"  {i}")
        print(f"\nFix: export LM_STUDIO_MODEL_ID='{ids[0] if ids else 'your-model-id'}'")
        sys.exit(1)
    if not is_loaded:
        print("  Model idle -- loading before run...")
        if not load_model(model_id):
            print("ERROR: Model failed to load.")
            sys.exit(1)
    else:
        print(f"  Model already loaded.")

# ── Vision API ────────────────────────────────────────────────────────────────

def is_eviction_error(e):
    msg = str(e).lower()
    return any(x in msg for x in ["model not loaded", "no model loaded", "not loaded",
                                    "evicted", "503", "500"])


def call_lm_studio(client, img_b64):
    response = client.chat.completions.create(
        model=LM_STUDIO_MODEL_ID,
        max_tokens=4096,
        messages=[{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
            {"type": "text", "text": EXTRACT_PROMPT}
        ]}]
    )
    return response.choices[0].message.content.strip()


def extract_and_transcribe(image_path, client):
    with open(image_path, "rb") as f:
        img_b64 = base64.standard_b64encode(f.read()).decode("utf-8")
    try:
        raw = call_lm_studio(client, img_b64)
    except Exception as e:
        if is_eviction_error(e):
            print("  Model evicted mid-run -- reloading and retrying...")
            load_model(LM_STUDIO_MODEL_ID)
            raw = call_lm_studio(client, img_b64)
        else:
            raise
    raw = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw, flags=re.MULTILINE).strip()
    return json.loads(raw)

# ── PDF helpers ───────────────────────────────────────────────────────────────

def rasterize_page(pdf_path, page_num, pid):
    prefix = f"/tmp/ss_{pid}_{os.path.basename(pdf_path).replace(' ','_')}_{page_num}"
    for f in glob.glob(f"{prefix}-*.png"):
        os.remove(f)
    subprocess.run(
        ["pdftoppm", "-png", "-r", "200",
         "-f", str(page_num), "-l", str(page_num), pdf_path, prefix],
        check=True, capture_output=True
    )
    results = sorted(glob.glob(f"{prefix}-*.png"))
    if not results:
        raise FileNotFoundError(f"No rasterized output for page {page_num} of {pdf_path}")
    return results[0]


def collect_page_pdfs():
    all_pdfs = sorted(glob.glob(os.path.join(SCANSNAP_DIR, "*.pdf")))
    items = []
    seen_scan_dates = set()
    for pdf in all_pdfs:
        base = os.path.basename(pdf)
        if re.match(r'^\d{8}_\d{3}\.pdf$', base):
            items.append((pdf, 1))
            seen_scan_dates.add(base[:8])
    for pdf in all_pdfs:
        base = os.path.basename(pdf)
        if re.match(r'^\d{8}\.pdf$', base) and base[:8] not in seen_scan_dates:
            n = len(PdfReader(pdf).pages)
            for pg in range(1, n + 1):
                items.append((pdf, pg))
    return items

# ── Date helpers ──────────────────────────────────────────────────────────────

def resolve_date_str(month, day):
    today = date.today()
    candidate = date(today.year, month, day)
    year = today.year - 1 if candidate > today + timedelta(days=30) else today.year
    return f"{year}-{month:02d}-{day:02d}"

# ── Obsidian output ───────────────────────────────────────────────────────────

def already_processed(date_compact):
    return bool(glob.glob(os.path.join(OBSIDIAN_INBOX, f"{date_compact}_Handwritten_Notes*.md")))


def get_output_path(date_compact):
    base = f"{date_compact}_Handwritten_Notes"
    path = os.path.join(OBSIDIAN_INBOX, f"{base}.md")
    if not os.path.exists(path):
        return path
    n = 2
    while True:
        path = os.path.join(OBSIDIAN_INBOX, f"{base}_{n}.md")
        if not os.path.exists(path):
            return path
        n += 1


def format_note(date_str, sorted_pages):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    source_files = sorted(set(os.path.basename(p["pdf_path"]) for p in sorted_pages))
    fm = (f"---\ndate: {date_str}\ntype: handwritten-note\nsource: ScanSnap\n"
          f"source_files: [{', '.join(source_files)}]\n"
          f"pages: {len(sorted_pages)}\ntags: [handwritten, inbox]\n---")
    title = f"# Handwritten Notes -- {dt.strftime('%B %d, %Y')}"
    if len(sorted_pages) == 1:
        body = sorted_pages[0]["transcription"]
    else:
        sections = [f"---\n*Page {p['label']['letter'].upper()}*\n\n{p['transcription']}"
                    for p in sorted_pages]
        body = "\n\n".join(sections)
    return f"{fm}\n\n{title}\n\n{body}\n"

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    target_filter = sys.argv[1] if len(sys.argv) > 1 else None
    pid = os.getpid()

    print(f"SCANSNAP_DIR:   {SCANSNAP_DIR}")
    print(f"OBSIDIAN_INBOX: {OBSIDIAN_INBOX}")
    print(f"LM_STUDIO_BASE: {LM_STUDIO_BASE}")
    print(f"MODEL:          {LM_STUDIO_MODEL_ID}\n")

    if not lm_studio_reachable():
        print("ERROR: LM Studio server is not running.")
        print(f"  Open LM Studio -> Developer tab -> Start Server")
        print(f"  Or set LM_STUDIO_BASE if using a different address.")
        sys.exit(1)

    from openai import OpenAI
    client = OpenAI(base_url=f"{LM_STUDIO_BASE}/v1", api_key="lm-studio")
    startup_check(LM_STUDIO_MODEL_ID)

    all_items = collect_page_pdfs()
    if not all_items:
        print(f"No PDFs found in: {SCANSNAP_DIR}")
        print("Set SCANSNAP_DIR env var to your ScanSnap processed folder.")
        return

    print(f"\nFound {len(all_items)} page(s) to process.\n")

    page_results, unlabeled = [], []

    for i, (pdf_path, page_num) in enumerate(all_items, 1):
        basename = os.path.basename(pdf_path)
        print(f"[{i}/{len(all_items)}] {basename} p{page_num} -- rasterizing...")
        try:
            img_path = rasterize_page(pdf_path, page_num, pid)
        except Exception as e:
            print(f"  ERROR: {e}")
            unlabeled.append({"pdf_path": pdf_path, "page_num": page_num, "error": f"rasterize: {e}"})
            continue

        print(f"[{i}/{len(all_items)}] {basename} p{page_num} -- transcribing...")
        try:
            result = extract_and_transcribe(img_path, client)
        except Exception as e:
            print(f"  WARNING: {e}")
            unlabeled.append({"pdf_path": pdf_path, "page_num": page_num, "error": str(e)})
            os.remove(img_path)
            continue

        os.remove(img_path)
        lbl = result.get("label", {})
        transcription = result.get("transcription", "").strip()

        if transcription == "BLANK_PAGE":
            print("  Blank -- skipping.")
            continue
        if lbl.get("month") is None:
            print("  No corner label detected.")
            unlabeled.append({"pdf_path": pdf_path, "page_num": page_num,
                               "transcription": transcription, "error": "label not found"})
        else:
            print(f"  Label: {lbl['month']:02d}/{lbl['day']:02d} {lbl['letter']}")
            page_results.append({"pdf_path": pdf_path, "page_num": page_num,
                                  "label": lbl, "transcription": transcription})

    if not page_results and not unlabeled:
        print("\nAll pages were blank. Nothing to write.")
        return

    by_date = defaultdict(list)
    for p in page_results:
        lbl = p["label"]
        by_date[resolve_date_str(lbl["month"], lbl["day"])].append(p)
    for d in by_date:
        by_date[d].sort(key=lambda p: ord(p["label"]["letter"].lower()) - ord('a'))

    if target_filter:
        by_date = {k: v for k, v in by_date.items() if target_filter in k}

    print(f"\nAssembling {len(by_date)} note(s)...\n")
    for date_str, pages in sorted(by_date.items()):
        date_compact = date_str.replace("-", "")
        if already_processed(date_compact):
            print(f"  {date_str} -- already in Obsidian, skipping.")
            continue
        letters = [p["label"]["letter"].upper() for p in pages]
        print(f"  {date_str}: {len(pages)} page(s) [{', '.join(letters)}]")
        note = format_note(date_str, pages)
        out_path = get_output_path(date_compact)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(note)
        print(f"  -> {os.path.basename(out_path)}")

    if unlabeled:
        print(f"\n  {len(unlabeled)} page(s) could not be processed:")
        for u in unlabeled:
            print(f"  {os.path.basename(u['pdf_path'])} p{u['page_num']}: {u.get('error')}")
        print("  These were NOT written to Obsidian -- review manually.")

    print("\nDone.")


if __name__ == "__main__":
    main()
