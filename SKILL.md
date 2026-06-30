---
name: book-to-audio
description: >
  Convert PDF or EPUB to audiobook MP3. 3 modes: concise chapters (~30%),
  full chapters (verbatim), single summary MP3. Supports 17 languages.
  Use when user says "convert book to audio", "make audiobook",
  "summarize book as audio", "pdf to audio", "epub to audio".
---

# Book to Audiobook

Convert any PDF or EPUB into an audiobook using edge-tts.

## Prerequisites

Run once to set up the Python venv:

```bash
cd /home/otwos/Projects/Audiobook
bash scripts/setup.sh
```

All subsequent commands run from the Audiobook directory with venv activated:

```bash
source .venv/bin/activate
```

## Modes

| Mode | Description | Output |
|------|-------------|--------|
| **1. Full chapters** | Each chapter at 100% original text. One MP3 per chapter. | `01-chapter.mp3`, `02-chapter.mp3`, ... |
| **2. Full book** | Entire book at 100% original text. One MP3 file. | `full-book.mp3` |
| **3. Single summary** | Entire book summarized to ~30-40%. One MP3 file. | `book-summary.mp3` |

## Workflow

### Step 1: Ask the user

Ask these questions before starting:

1. **File path** — path to the PDF or EPUB file
2. **Mode** — 1 (concise chapters), 2 (full chapters), or 3 (single summary MP3)
3. **Voice preference** — or let the agent auto-detect language and suggest a voice

If user doesn't specify a voice, extract first, detect language, then suggest
the default voice from `scripts/voices.json`.

### Step 2: Extract text

```bash
source .venv/bin/activate
python scripts/extract.py "<file_path>" --output chapters.json
```

This produces `chapters.json` with structure:

```json
{
  "title": "Book Title",
  "author": "Author Name",
  "language": "en",
  "chapters": [
    {"num": 1, "heading": "Chapter 1", "text": "..."},
    {"num": 2, "heading": "Chapter 2", "text": "..."}
  ]
}
```

Report to user: title, author, number of chapters, detected language.

### Step 3: Summarize (Mode 3 only)

The agent summarizes the text using its own LLM. No external API needed.

**Mode 3 — summarize entire book:**

Concatenate all chapter texts. Summarize the combined text to ~30-40%. Write the
summary as a single chapter in `chapters.json`:

```json
{
  "title": "Book Title",
  "author": "Author Name",
  "language": "en",
  "chapters": [
    {"num": 1, "heading": "Book Summary", "text": "...summarized text..."}
  ]
}
```

**Summary guidelines:**
- Target ~30-40% of original word count
- Use clear, spoken-language style (this will be read aloud)
- Avoid bullet points — write in flowing paragraphs suitable for speech
- Preserve the author's voice and key terminology
- Include chapter/section transitions so the audio flows naturally

### Step 4: Convert to audio (Mode 1 and Mode 2 — no summarization needed)

For Mode 1 and Mode 2, skip Step 3 and go directly to conversion.

### Step 4: Convert to audio

```bash
python scripts/tts_convert.py chapters.json --mode <1|2|3> --voice <voice> --output ./output/
```

Mode 1 and 2 use original text. Mode 3 uses summarized text from Step 3.

**Voice selection:**
- Read `scripts/voices.json` for the detected language
- Use the first voice in the list as default (male voice)
- If user prefers female voice, use the second voice
- User can specify any edge-tts voice name directly

**Common voice examples:**
- English (US): `en-US-GuyNeural`, `en-US-JennyNeural`
- English (UK): `en-GB-RyanNeural`, `en-GB-SoniaNeural`
- German: `de-DE-ConradNeural`, `de-DE-KatjaNeural`
- French: `fr-FR-HenriNeural`, `fr-FR-DeniseNeural`
- Spanish: `es-ES-AlvaroNeural`, `es-ES-ElviraNeural`
- Japanese: `ja-JP-KeitaNeural`, `ja-JP-NanamiNeural`
- Full list: run `edge-tts --list-voices`

### Step 5: Report results

Tell the user:
- Output directory path
- Number of MP3 files created
- File names and approximate sizes
- Any chapters that were skipped (empty text)
- If scanned PDF detected (no text layer), suggest OCR tools

## Troubleshooting

**"No text found in PDF"** — PDF is likely scanned image, not text. Needs OCR first.

**"No chapters detected"** — Book has no clear chapter structure. Entire book
treated as one chapter.

**TTS errors** — Usually text too long. Script auto-splits at 5000 chars.
If errors persist, check edge-tts voice name is valid.

**Slow conversion** — edge-tts is network-based. Large books take 10-30 minutes.
Each chapter prints progress to stderr.
