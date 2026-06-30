# Book to Audiobook — Universal Installer

Copy the prompt below and paste it into your AI coding agent. It will auto-install the skill in the correct location.

---

## For opencode

Paste this into opencode:

```
Install the book-to-audio skill from https://github.com/dsribalaji/audiobook

Steps:
1. Clone the repo to /tmp/audiobook-skill: git clone https://github.com/dsribalaji/audiobook.git /tmp/audiobook-skill
2. Create the command directory: mkdir -p ~/.config/opencode/command
3. Copy the command file: cp /tmp/audiobook-skill/command/audiobook.md ~/.config/opencode/command/audiobook.md
4. Copy the scripts folder: cp -r /tmp/audiobook-skill/scripts ~/.config/opencode/skills/book-to-audio-scripts
5. Update the command file paths if needed to point to the scripts location
6. Run setup: cd /tmp/audiobook-skill && bash scripts/setup.sh
7. Clean up: rm -rf /tmp/audiobook-skill
8. Tell me the skill is ready. I can use it by typing /audiobook
```

---

## For Claude Code

Paste this into Claude Code:

```
Install the book-to-audio skill from https://github.com/dsribalaji/audiobook

Steps:
1. git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
2. Create a CLAUDE.md entry or add to your project instructions referencing ~/.audiobook-skill/SKILL.md
3. Run: cd ~/.audiobook-skill && bash scripts/setup.sh
4. When I ask to convert a book, read ~/.audiobook-skill/SKILL.md and follow the workflow there
5. Tell me the skill is ready
```

---

## For GitHub Copilot

Paste this into Copilot Chat:

```
Install the book-to-audio skill from https://github.com/dsribalaji/audiobook

Steps:
1. git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
2. Run: cd ~/.audiobook-skill && bash scripts/setup.sh
3. When I ask to convert a book to audio, read the SKILL.md at ~/.audiobook-skill/SKILL.md and follow the instructions
4. Tell me the skill is ready
```

---

## For Cursor

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

---

## For Aider

```
/git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
!cd ~/.audiobook-skill && bash scripts/setup.sh
/read ~/.audiobook-skill/SKILL.md
```

---

## For Windsurf / Codeium

Paste this into the AI chat:

```
Install the book-to-audio skill from https://github.com/dsribalaji/audiobook

Steps:
1. git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
2. Run: cd ~/.audiobook-skill && bash scripts/setup.sh
3. Reference ~/.audiobook-skill/SKILL.md when I ask to convert books to audio
4. Tell me the skill is ready
```

---

## For any agent (generic)

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

## Manual Install

If you prefer to install manually:

```bash
# 1. Clone
git clone https://github.com/dsribalaji/audiobook.git ~/.audiobook-skill
cd ~/.audiobook-skill

# 2. Setup
bash scripts/setup.sh

# 3. Test
source .venv/bin/activate
python scripts/extract.py --help
python scripts/tts_convert.py --help
```

## Usage (Manual CLI)

```bash
cd ~/.audiobook-skill
source .venv/bin/activate

# Extract
python scripts/extract.py "/path/to/book.pdf" --output chapters.json

# Convert (mode 1=concise, 2=full, 3=single summary)
python scripts/tts_convert.py chapters.json --mode 1 --voice en-US-GuyNeural --output ./output/my-book/
```
