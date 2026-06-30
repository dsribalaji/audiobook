# Book to Audiobook

Convert any PDF or EPUB into an audiobook using AI text-to-speech. Works with any agentic CLI (opencode, Claude Code, Cursor, etc.).

## Features

- **3 conversion modes** — concise chapters, full chapters, or single summary MP3
- **17 languages** — English, Greek, Russian, German, Japanese, French, Spanish, Portuguese, Chinese, Korean, Italian, Arabic, Hindi, Turkish, Dutch, Polish, Swedish
- **Auto chapter detection** — detects chapters from headings, font sizes, and TOC
- **Auto language detection** — identifies book language and suggests matching voice
- **Full ID3 metadata** — title, author, chapter names, track numbers embedded in MP3
- **No API keys needed** — uses free edge-tts (Microsoft) for voice synthesis
- **Agent-powered summarization** — your LLM summarizes the book, no extra API costs

## Requirements

- Python 3.10+
- `uv` (recommended) or `pip`
- Internet connection (edge-tts is network-based)

## Quick Start

### One-line install (any agent)

```bash
curl -sSL https://raw.githubusercontent.com/dsribalaji/audiobook/main/install.sh | bash
```

This clones the repo to `~/.audiobook-skill`, sets up the venv, and installs the `/audiobook` command for opencode if detected.

### opencode

Type `/audiobook` — it asks for the book file, mode, and voice. Done.

### Claude Code / Copilot / Cursor / Other agents

Copy the install prompt from [install.md](install.md) and paste it into your agent. It will self-install.

### Manual CLI

```bash
git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
cd ~/.audiobook-skill
bash scripts/setup.sh
source .venv/bin/activate

# Extract
python scripts/extract.py "/path/to/book.pdf" --output chapters.json

# Convert
python scripts/tts_convert.py chapters.json --mode 1 --voice en-US-GuyNeural --output ./output/my-book/
```

## Conversion Modes

| Mode | Name | Description | Output |
|------|------|-------------|--------|
| `--mode 1` | **Concise Chapters** | Each chapter summarized to ~30% of original length. One MP3 per chapter. | `01-Chapter-1.mp3`, `02-Chapter-2.mp3`, ... |
| `--mode 2` | **Full Chapters** | Each chapter read verbatim. One MP3 per chapter. | `01-Chapter-1.mp3`, `02-Chapter-2.mp3`, ... |
| `--mode 3` | **Single Summary** | Entire book summarized to ~30%. One MP3 file. | `book-summary.mp3` |

## Usage with Agentic CLI

### Option A: Use as a Skill (Recommended)

Point your agent at the `SKILL.md` file. The agent will:

1. Ask you for the book file, mode, and voice preference
2. Extract text from the PDF/EPUB
3. Summarize chapters (Mode 1) or the full book (Mode 3) using its own LLM
4. Convert to MP3 with metadata
5. Report the output location

**opencode:**
```
Convert this book to audio: /path/to/book.pdf
```

**Claude Code / Cursor:**
```
Read the SKILL.md in /home/otwos/Projects/Audiobook/ and follow the instructions
to convert my book to an audiobook.
```

### Option B: Manual CLI Usage

#### Step 1: Extract Text

```bash
source .venv/bin/activate
python scripts/extract.py "/path/to/book.pdf" --output chapters.json
```

Output:
```
Extracted 12 chapters from 'My Book Title'
Language: en
Output: chapters.json
```

The `chapters.json` file contains:
```json
{
  "title": "My Book Title",
  "author": "John Doe",
  "language": "en",
  "chapters": [
    {"num": 1, "heading": "Chapter 1: The Beginning", "text": "..."},
    {"num": 2, "heading": "Chapter 2: The Journey", "text": "..."}
  ]
}
```

#### Step 2: Summarize (Mode 1 and Mode 3 Only)

For **Mode 1** — edit `chapters.json` and replace each chapter's `text` with a ~30% summary.

For **Mode 3** — merge all chapters into one and summarize to ~30%:
```json
{
  "title": "My Book Title",
  "author": "John Doe",
  "language": "en",
  "chapters": [
    {"num": 1, "heading": "Book Summary", "text": "...summarized text..."}
  ]
}
```

For **Mode 2** — skip this step entirely.

#### Step 3: Convert to Audio

```bash
# Mode 1: Concise chapters
python scripts/tts_convert.py chapters.json --mode 1 --voice en-US-GuyNeural --output ./output/

# Mode 2: Full chapters
python scripts/tts_convert.py chapters.json --mode 2 --voice en-US-GuyNeural --output ./output/

# Mode 3: Single summary
python scripts/tts_convert.py chapters.json --mode 3 --voice en-US-GuyNeural --output ./output/
```

## Supported Languages & Voices

| Language | Code | Male Voice | Female Voice |
|----------|------|------------|--------------|
| English | `en` | `en-US-GuyNeural` | `en-US-JennyNeural` |
| English (UK) | `en` | `en-GB-RyanNeural` | `en-GB-SoniaNeural` |
| Greek | `el` | `el-GR-NestorasNeural` | `el-GR-AthinaNeural` |
| Russian | `ru` | `ru-RU-DmitryNeural` | `ru-RU-SvetlanaNeural` |
| German | `de` | `de-DE-ConradNeural` | `de-DE-KatjaNeural` |
| Japanese | `ja` | `ja-JP-KeitaNeural` | `ja-JP-NanamiNeural` |
| French | `fr` | `fr-FR-HenriNeural` | `fr-FR-DeniseNeural` |
| Spanish | `es` | `es-ES-AlvaroNeural` | `es-ES-ElviraNeural` |
| Portuguese | `pt` | `pt-BR-AntonioNeural` | `pt-BR-FranciscaNeural` |
| Chinese | `zh` | `zh-CN-YunxiNeural` | `zh-CN-XiaoxiaoNeural` |
| Korean | `ko` | `ko-KR-InJoonNeural` | `ko-KR-SunHiNeural` |
| Italian | `it` | `it-IT-DiegoNeural` | `it-IT-ElsaNeural` |
| Arabic | `ar` | `ar-SA-HamedNeural` | `ar-SA-ZariyahNeural` |
| Hindi | `hi` | `hi-IN-MadhurNeural` | `hi-IN-SwaraNeural` |
| Turkish | `tr` | `tr-TR-AhmetNeural` | `tr-TR-EmelNeural` |
| Dutch | `nl` | `nl-NL-MaartenNeural` | `nl-NL-ColetteNeural` |
| Polish | `pl` | `pl-PL-MarekNeural` | `pl-PL-AgnieszkaNeural` |
| Swedish | `sv` | `sv-SE-MattiasNeural` | `sv-SE-SofieNeural` |

List all available voices:
```bash
edge-tts --list-voices
```

## File Structure

```
Audiobook/
├── SKILL.md                  # Agent instructions (works with any CLI)
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── scripts/
│   ├── setup.sh              # One-time setup (creates venv, installs deps)
│   ├── extract.py            # PDF/EPUB → JSON text extraction
│   ├── tts_convert.py        # JSON → MP3 conversion with metadata
│   └── voices.json           # Language → voice mappings
├── output/                   # Generated audiobook files
└── .venv/                    # Python virtual environment (created by setup)
```

## Script Reference

### `scripts/extract.py`

Extracts text from PDF or EPUB into structured JSON.

```bash
python scripts/extract.py <file_path> [--output <json_file>]
```

| Argument | Description |
|----------|-------------|
| `file_path` | Path to PDF or EPUB file |
| `--output`, `-o` | Output JSON file path (default: stdout) |

**Chapter detection heuristics:**
- `Chapter X`, `CHAPTER X`, `Part X`, `Section X` patterns
- `Lesson X`, `Session X`, `Unit X` patterns
- Standalone numbers 1-30 on their own line
- ALL CAPS headings (5-60 chars, no digits, max 8 words)
- Minimum 200 chars accumulated before splitting to new chapter

**Language detection:**
- Character script analysis (Cyrillic, CJK, Arabic, Greek, Devanagari)
- Common word frequency for European languages
- Falls back to English if uncertain

### `scripts/tts_convert.py`

Converts chapter JSON to MP3 audiobook files.

```bash
python scripts/tts_convert.py <json_file> --mode <1|2|3> [--voice <voice>] [--output <dir>]
```

| Argument | Description |
|----------|-------------|
| `json_file` | Path to chapters JSON file |
| `--mode` | `1` = concise chapters, `2` = full chapters, `3` = single summary |
| `--voice` | edge-tts voice name (default: `en-US-GuyNeural`) |
| `--output`, `-o` | Output directory (default: `./output/`) |

**Features:**
- Auto-splits text >5000 chars at sentence boundaries
- Merges split chunks back into single chapter MP3
- Embeds ID3 metadata: title, artist (author), track number
- Progress output to stderr

### `scripts/voices.json`

Maps language codes to recommended voices. First voice in list is male default, second is female.

### `scripts/setup.sh`

One-time setup script. Creates Python venv and installs dependencies.

```bash
bash scripts/setup.sh
```

Uses `uv` if available, falls back to `python3 -m venv`.

## Agent Integration

### How Agents Use This Skill

When you ask an agent to "convert this book to audio", the agent:

1. **Reads `SKILL.md`** — understands the workflow and available modes
2. **Asks you** — file path, mode (1/2/3), voice preference
3. **Runs `extract.py`** — gets structured text from your book
4. **Summarizes** (Mode 1 & 3) — uses its own LLM to condense text to ~30%
5. **Runs `tts_convert.py`** — generates MP3 files with metadata
6. **Reports** — output location, file count, any issues

### Supported Agent CLIs

This skill works with any CLI that can:
- Read markdown instruction files
- Execute shell commands
- Process and generate text (for summarization)

Tested with:
- **opencode** — load via `skills` config or place in `.opencode/skills/`
- **Claude Code** — reference `SKILL.md` directly
- **Cursor** — add as custom instruction
- **Aider** — use `--read` flag with SKILL.md
- **Any agent** — generic markdown instructions, no platform-specific config

### Adding to opencode

```json
// opencode.json
{
  "skills": {
    "paths": ["/home/otwos/Projects/Audiobook"]
  }
}
```

Or place the `Audiobook` folder inside `.opencode/skills/`:
```bash
cp -r /home/otwos/Projects/Audiobook .opencode/skills/book-to-audio
```

## Troubleshooting

### "No text found in PDF"
The PDF is likely a scanned image, not a text-based PDF. You need OCR first:
```bash
# Install tesseract
sudo apt install tesseract-ocr

# OCR the PDF
ocrmypdf input.pdf output.pdf
```
Then use `output.pdf` with extract.py.

### "No chapters detected"
The book doesn't have clear chapter headings. The entire book is treated as one chapter. You can manually edit `chapters.json` to split it.

### "Module not found" errors
Re-run setup:
```bash
bash scripts/setup.sh
```

### TTS errors about text length
The script auto-splits text at 5000 chars. If errors persist:
- Check voice name is valid: `edge-tts --list-voices`
- Check internet connection (edge-tts requires network)

### Slow conversion
edge-tts is network-based. Expectations:
- 10-page chapter: ~30 seconds
- 300-page book (full): ~15-30 minutes
- Summary mode: ~2-5 minutes

Each chapter prints progress to stderr so you can track it.

### Double characters in extracted text
Some PDFs encode text with duplicate characters (e.g., "WWhhaatt" instead of "What"). This is a PDF encoding issue, not a bug in extract.py. Use a different source PDF or preprocess with OCR.

## License

MIT
