---
description: Convert PDF or EPUB to audiobook MP3. 3 modes: concise, full, single summary.
---

# /audiobook

You are converting a book (PDF or EPUB) into an audiobook. Follow these steps exactly.

## Step 0: Auto-setup

Check if the venv exists at `/home/otwos/Projects/Audiobook/.venv/`. If not, run:

```bash
cd /home/otwos/Projects/Audiobook && bash scripts/setup.sh
```

If setup.sh fails (no uv, no python3-venv), try:
```bash
cd /home/otwos/Projects/Audiobook
python3 -m venv --without-pip .venv
source .venv/bin/activate
curl -sS https://bootstrap.pypa.io/get-pip.py | python
pip install -r requirements.txt
```

## Step 1: Ask user

Ask the user these questions (use the question tool):

1. **File path** — path to their PDF or EPUB file. Use `$ARGUMENTS` if provided.
2. **Mode**:
   - `1` — Full chapters (100% original, one MP3 per chapter)
   - `2` — Full book (100% original, single MP3 with all chapters)
   - `3` — Single summary (entire book summarized to ~30-40%, one MP3)
3. **Voice** — Male or Female?

## Step 2: Extract text

```bash
source /home/otwos/Projects/Audiobook/.venv/bin/activate
python /home/otwos/Projects/Audiobook/scripts/extract.py "<file_path>" --output /tmp/audiobook_chapters.json
```

Read the output. Report: title, author, chapter count, detected language.

## Step 3: Pick voice

Read `/home/otwos/Projects/Audiobook/scripts/voices.json`. Match the detected language code. Pick first voice for male, second for female.

## Step 4: Summarize (Mode 1 and 3 only)

Read `/tmp/audiobook_chapters.json`.

**Mode 1:** For each chapter, summarize the text to ~30% of original. Preserve key concepts, principles, examples, and takeaways. Write in flowing paragraphs (no bullet points) suitable for spoken audio. Write summarized text back into the JSON.

**Mode 3:** Concatenate all chapter text. Summarize to ~30%. Write as a single chapter with heading "Book Summary".

Write the final JSON to `/tmp/audiobook_chapters.json`.

## Step 5: Create output folder

```bash
mkdir -p /home/otwos/Projects/Audiobook/output/<book-slug>
```

Where `<book-slug>` is the book title, lowercase, hyphens for spaces (e.g., `rich-dad-poor-dad`).

## Step 6: Convert to audio

```bash
source /home/otwos/Projects/Audiobook/.venv/bin/activate
python /home/otwos/Projects/Audiobook/scripts/tts_convert.py /tmp/audiobook_chapters.json --mode <1|2|3> --voice <voice> --output /home/otwos/Projects/Audiobook/output/<book-slug>/
```

## Step 7: Report

Tell the user:
- Output folder path
- Number of MP3 files created
- List of files with sizes
- Any chapters skipped
- Clean up: `rm /tmp/audiobook_chapters.json`

If any step fails, report the error clearly and suggest fixes.
