#!/usr/bin/env python3
"""Convert chapter JSON to MP3 audiobook using edge-tts."""

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

def split_text(text: str, max_chars: int = 5000) -> list[str]:
    """Split text at sentence boundaries, respecting max_chars limit."""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 > max_chars:
            if current:
                chunks.append(current.strip())
            current = sentence
        else:
            current = (current + " " + sentence).strip() if current else sentence

    if current.strip():
        chunks.append(current.strip())

    return chunks if chunks else [text[:max_chars]]


def set_mp3_metadata(file_path: Path, title: str, artist: str, track: int):
    """Add ID3 tags to MP3 file."""
    try:
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, TIT2, TPE1, TRCK

        audio = MP3(str(file_path))
        if audio.tags is None:
            audio.add_tags()

        audio.tags.add(TIT2(encoding=3, text=[title]))
        audio.tags.add(TPE1(encoding=3, text=[artist]))
        audio.tags.add(TRCK(encoding=3, text=[str(track)]))
        audio.save()
    except Exception as e:
        print(f"  Warning: Could not set metadata: {e}", file=sys.stderr)


async def tts_to_file(text: str, voice: str, output_path: Path):
    """Convert text to MP3 using edge-tts."""
    import edge_tts

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))


async def convert_chapters(chapters: list, voice: str, output_dir: Path, mode: int, author: str = "Unknown"):
    """Convert all chapters to MP3 files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    total = len(chapters)

    for i, chapter in enumerate(chapters):
        num = chapter.get("num", i + 1)
        heading = chapter.get("heading", f"Chapter {num}")
        text = chapter.get("text", "")

        if not text.strip():
            print(f"  Skipping empty chapter: {heading}", file=sys.stderr)
            continue

        # Clean heading for filename
        safe_heading = re.sub(r'[^\w\s-]', '', heading)[:50].strip().replace(' ', '-')
        if not safe_heading:
            safe_heading = f"chapter-{num}"
        filename = f"{num:02d}-{safe_heading}.mp3"
        filepath = output_dir / filename

        print(f"[{num}/{total}] {heading}", file=sys.stderr)

        # Split long text into chunks
        chunks = split_text(text)
        if len(chunks) > 1:
            print(f"  Split into {len(chunks)} parts", file=sys.stderr)

        # Convert each chunk
        temp_files = []
        for j, chunk in enumerate(chunks):
            if len(chunks) > 1:
                temp_path = output_dir / f".tmp_{num}_{j}.mp3"
            else:
                temp_path = filepath

            await tts_to_file(chunk, voice, temp_path)
            if len(chunks) > 1:
                temp_files.append(temp_path)

        # Merge chunks if split
        if temp_files:
            merge_mp3s(temp_files, filepath)
            for f in temp_files:
                f.unlink(missing_ok=True)

        set_mp3_metadata(filepath, heading, author, num)

    print(f"\nDone. Output: {output_dir}", file=sys.stderr)


def merge_mp3s(files: list[Path], output: Path):
    """Merge multiple MP3 files into one."""
    from mutagen.mp3 import MP3

    # Simple binary concat (works for same-bitrate MP3s from same TTS engine)
    with open(output, 'wb') as outf:
        for f in files:
            outf.write(f.read_bytes())


async def convert_single(chapters: list, voice: str, output_dir: Path, author: str = "Unknown"):
    """Convert all chapters into a single MP3 (Mode 3)."""
    output_dir.mkdir(parents=True, exist_ok=True)

    combined_text = ""
    for chapter in chapters:
        heading = chapter.get("heading", "")
        text = chapter.get("text", "")
        if heading:
            combined_text += f"{heading}.\n\n"
        combined_text += text + "\n\n"

    if not combined_text.strip():
        sys.exit("Error: No text to convert.")

    safe_name = "book-summary.mp3"
    filepath = output_dir / safe_name

    print(f"Converting {len(combined_text)} chars to audio...", file=sys.stderr)

    chunks = split_text(combined_text)
    print(f"Split into {len(chunks)} chunks", file=sys.stderr)

    if len(chunks) == 1:
        await tts_to_file(chunks[0], voice, filepath)
    else:
        temp_files = []
        for j, chunk in enumerate(chunks):
            temp_path = output_dir / f".tmp_summary_{j}.mp3"
            print(f"  Chunk {j+1}/{len(chunks)}...", file=sys.stderr)
            await tts_to_file(chunk, voice, temp_path)
            temp_files.append(temp_path)

        merge_mp3s(temp_files, filepath)
        for f in temp_files:
            f.unlink(missing_ok=True)

    set_mp3_metadata(filepath, "Book Summary", author, 1)
    print(f"\nDone. Output: {filepath}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Convert chapter JSON to MP3 audiobook")
    parser.add_argument("json_file", help="Path to chapters JSON file")
    parser.add_argument("--mode", type=int, required=True, choices=[1, 2, 3],
                        help="1=concise chapters, 2=full chapters, 3=single summary")
    parser.add_argument("--voice", default="en-US-GuyNeural",
                        help="edge-tts voice name (default: en-US-GuyNeural)")
    parser.add_argument("--output", "-o", default="./output",
                        help="Output directory (default: ./output)")
    args = parser.parse_args()

    json_path = Path(args.json_file)
    if not json_path.exists():
        sys.exit(f"Error: JSON file not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chapters = data.get("chapters", [])
    if not chapters:
        sys.exit("Error: No chapters found in JSON.")

    output_dir = Path(args.output)
    voice = args.voice
    author = data.get("author", "Unknown")

    print(f"Mode: {args.mode}", file=sys.stderr)
    print(f"Voice: {voice}", file=sys.stderr)
    print(f"Chapters: {len(chapters)}", file=sys.stderr)
    print(f"Author: {author}", file=sys.stderr)
    print(f"Output: {output_dir}", file=sys.stderr)
    print("", file=sys.stderr)

    if args.mode == 3:
        asyncio.run(convert_single(chapters, voice, output_dir, author))
    else:
        asyncio.run(convert_chapters(chapters, voice, output_dir, args.mode, author))


if __name__ == "__main__":
    main()
