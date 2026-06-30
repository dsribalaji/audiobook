# Book to Audiobook

Convert any PDF or EPUB into an audiobook using AI text-to-speech. Works with any agentic CLI — opencode, Claude Code, Copilot, Cursor, Aider, Windsurf, or plain terminal.

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

---

## Installation

### One-line install

```bash
curl -sSL https://raw.githubusercontent.com/dsribalaji/audiobook/main/install.sh | bash
```

Clones to `~/.audiobook-skill`, sets up venv, installs `/audiobook` command for opencode if detected.

### opencode

Type `/audiobook` — asks for book file, mode, voice. Done.

### Claude Code

Paste this into Claude Code:

```
Install the book-to-audio skill from https://github.com/dsribalaji/audiobook

Steps:
1. git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
2. Run: cd ~/.audiobook-skill && bash scripts/setup.sh
3. When I ask to convert a book, read ~/.audiobook-skill/SKILL.md and follow the workflow
4. Tell me the skill is ready
```

### GitHub Copilot

Paste this into Copilot Chat:

```
Install the book-to-audio skill from https://github.com/dsribalaji/audiobook

Steps:
1. git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
2. Run: cd ~/.audiobook-skill && bash scripts/setup.sh
3. When I ask to convert a book to audio, read ~/.audiobook-skill/SKILL.md and follow it
4. Tell me the skill is ready
```

### Cursor

Paste this into Cursor Chat:

```
Install the book-to-audio skill from https://github.com/dsribalaji/audiobook

Steps:
1. git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
2. Run: cd ~/.audiobook-skill && bash scripts/setup.sh
3. Add ~/.audiobook-skill/SKILL.md to your Cursor rules or reference it as context
4. When I ask to convert a book, follow the SKILL.md workflow
5. Tell me the skill is ready
```

### Aider

```
/git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
!cd ~/.audiobook-skill && bash scripts/setup.sh
/read ~/.audiobook-skill/SKILL.md
```

### Windsurf / Codeium

```
Install the book-to-audio skill from https://github.com/dsribalaji/audiobook

Steps:
1. git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
2. Run: cd ~/.audiobook-skill && bash scripts/setup.sh
3. Reference ~/.audiobook-skill/SKILL.md when I ask to convert books to audio
4. Tell me the skill is ready
```

### Any agent (generic)

If your agent is not listed above, paste this:

```
I want to install the book-to-audio skill from https://github.com/dsribalaji/audiobook

1. Clone the repo: git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
2. Run setup: cd ~/.audiobook-skill && bash scripts/setup.sh
3. Read the SKILL.md file at ~/.audiobook-skill/SKILL.md
4. When I ask to convert a PDF or EPUB to audiobook, follow the workflow in SKILL.md
5. Output generated audio files to ~/.audiobook-skill/output/<book-name>/

Tell me when it's ready.
```

---

## Conversion Modes

| Mode | Name | Description | Output |
|------|------|-------------|--------|
| `--mode 1` | **Concise Chapters** | Each chapter summarized to ~30% of original length. One MP3 per chapter. | `01-Chapter-1.mp3`, `02-Chapter-2.mp3`, ... |
| `--mode 2` | **Full Chapters** | Each chapter read verbatim. One MP3 per chapter. | `01-Chapter-1.mp3`, `02-Chapter-2.mp3`, ... |
| `--mode 3` | **Single Summary** | Entire book summarized to ~30%. One MP3 file. | `book-summary.mp3` |

---

## Manual CLI Usage

```bash
git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
cd ~/.audiobook-skill
bash scripts/setup.sh
source .venv/bin/activate

# Step 1: Extract text
python scripts/extract.py "/path/to/book.pdf" --output chapters.json

# Step 2: Convert to audio (mode 1=concise, 2=full, 3=single summary)
python scripts/tts_convert.py chapters.json --mode 1 --voice en-US-GuyNeural --output ./output/my-book/
```

The `chapters.json` structure:
```json
{
  "title": "My Book Title",
  "author": "John Doe",
  "language": "en",
  "chapters": [
    {"num": 1, "heading": "Chapter 1", "text": "..."},
    {"num": 2, "heading": "Chapter 2", "text": "..."}
  ]
}
```

For Mode 1/3, edit `chapters.json` to replace text with summaries before converting. For Mode 2, skip summarization.

---

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

---

## File Structure

```
audiobook/
├── SKILL.md                  # Agent instructions (works with any CLI)
├── README.md                 # This file
├── install.sh                # One-line installer script
├── requirements.txt          # Python dependencies
├── command/
│   └── audiobook.md          # /audiobook slash command (opencode)
├── scripts/
│   ├── setup.sh              # Creates venv, installs deps
│   ├── extract.py            # PDF/EPUB → JSON text extraction
│   ├── tts_convert.py        # JSON → MP3 conversion with metadata
│   └── voices.json           # Language → voice mappings
└── output/                   # Generated audiobook files
```

---

## Script Reference

### `scripts/extract.py`

```bash
python scripts/extract.py <file_path> [--output <json_file>]
```

| Argument | Description |
|----------|-------------|
| `file_path` | Path to PDF or EPUB file |
| `--output`, `-o` | Output JSON file path (default: stdout) |

**Chapter detection:** `Chapter X`, `Part X`, `Section X`, `Lesson X`, standalone numbers 1-30, ALL CAPS headings (5-60 chars, no digits). Minimum 200 chars before splitting.

**Language detection:** Cyrillic, CJK, Arabic, Greek, Devanagari script analysis + European word frequency. Falls back to English.

### `scripts/tts_convert.py`

```bash
python scripts/tts_convert.py <json_file> --mode <1|2|3> [--voice <voice>] [--output <dir>]
```

| Argument | Description |
|----------|-------------|
| `json_file` | Path to chapters JSON file |
| `--mode` | `1` = concise, `2` = full, `3` = single summary |
| `--voice` | edge-tts voice name (default: `en-US-GuyNeural`) |
| `--output`, `-o` | Output directory (default: `./output/`) |

Auto-splits text >5000 chars at sentence boundaries. Embeds ID3 metadata (title, artist, track number).

### `scripts/voices.json`

Maps language codes to voices. First = male default, second = female.

### `scripts/setup.sh`

Creates venv and installs deps. Uses `uv` if available, falls back to `python3 -m venv`.

---

## Troubleshooting

**"No text found in PDF"** — Scanned image PDF. Needs OCR first:
```bash
sudo apt install tesseract-ocr
ocrmypdf input.pdf output.pdf
```

**"No chapters detected"** — No clear chapter headings. Entire book treated as one chapter. Edit `chapters.json` manually to split.

**"Module not found"** — Re-run `bash scripts/setup.sh`.

**TTS errors** — Script auto-splits at 5000 chars. Check voice name with `edge-tts --list-voices`. Check internet connection.

**Slow conversion** — edge-tts is network-based. ~30s per 10-page chapter. ~15-30 min for full 300-page book. ~2-5 min for summary mode. Progress prints to stderr.

**Double characters** — Some PDFs encode with duplicate chars ("WWhhaatt" instead of "What"). PDF encoding issue, not a bug. Use a different source or OCR.

## License

MIT
