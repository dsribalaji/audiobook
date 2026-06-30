#!/usr/bin/env python3
"""Extract text from PDF or EPUB into structured JSON by chapter."""

import argparse
import json
import re
import sys
from pathlib import Path

def extract_pdf(file_path: str) -> dict:
    """Extract chapters from PDF using pdfplumber."""
    import pdfplumber

    chapters = []
    current_chapter = {"num": 0, "heading": "Front Matter", "text": ""}

    with pdfplumber.open(file_path) as pdf:
        title = pdf.metadata.get("Title", "") if pdf.metadata else ""
        author = pdf.metadata.get("Author", "") if pdf.metadata else ""

        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if not text.strip():
                continue

            lines = text.split("\n")
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue

                is_chapter = False

                # Pattern: "Chapter X", "CHAPTER X", "Part X", "PART X"
                if re.match(r'^(?:chapter|part|section|book)\s+[\dIVXLC]+', stripped, re.IGNORECASE):
                    is_chapter = True
                # Pattern: "Lesson X", "Session X"
                elif re.match(r'^(?:lesson|session|unit)\s+\d+', stripped, re.IGNORECASE):
                    is_chapter = True
                # Pattern: Standalone number that looks like chapter number (1-30)
                elif re.match(r'^(\d{1,2})$', stripped):
                    num = int(stripped)
                    if 1 <= num <= 30:
                        # Only treat as chapter if there's minimal accumulated text
                        # (avoids picking up page numbers mid-content)
                        if len(current_chapter["text"].strip()) < 100:
                            is_chapter = True
                # Pattern: ALL CAPS line that looks like a heading
                # Must be: 5-60 chars, no digits (avoids prices/ISBNs), not a sentence
                elif (stripped.isupper()
                      and 5 < len(stripped) < 60
                      and not stripped.endswith('.')
                      and not any(c.isdigit() for c in stripped)
                      and len(stripped.split()) <= 8):
                    is_chapter = True

                if is_chapter:
                    # Only start new chapter if current has meaningful content
                    if current_chapter["text"].strip() and len(current_chapter["text"].strip()) > 200:
                        chapters.append(current_chapter)
                        current_chapter = {
                            "num": len(chapters) + 1,
                            "heading": stripped,
                            "text": ""
                        }
                    elif not current_chapter["text"].strip():
                        # First chapter heading found
                        current_chapter["heading"] = stripped
                else:
                    current_chapter["text"] += line + "\n"

            current_chapter["text"] += "\n"

    # Add last chapter
    if current_chapter["text"].strip():
        chapters.append(current_chapter)

    # If no chapters detected, treat entire book as one chapter
    if not chapters:
        all_text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                all_text += t + "\n"
        chapters = [{"num": 1, "heading": "Full Text", "text": all_text}]

    # Detect language (simple heuristic)
    language = detect_language(chapters[0]["text"][:2000] if chapters else "")

    return {
        "title": title or Path(file_path).stem,
        "author": author or "Unknown",
        "language": language,
        "chapters": chapters
    }


def extract_epub(file_path: str) -> dict:
    """Extract chapters from EPUB using ebooklib."""
    from ebooklib import epub
    from html.parser import HTMLParser

    class HTMLTextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []
            self._skip = False

        def handle_starttag(self, tag, attrs):
            if tag in ('script', 'style'):
                self._skip = True

        def handle_endtag(self, tag):
            if tag in ('script', 'style'):
                self._skip = False
            if tag in ('p', 'div', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                self.text.append('\n')

        def handle_data(self, data):
            if not self._skip:
                self.text.append(data)

        def get_text(self):
            return ''.join(self.text)

    book = epub.read_epub(file_path, options={"ignore_ncx": False})

    title = ""
    author = ""
    for item in book.get_metadata('DC', 'title'):
        title = item[0]
    for item in book.get_metadata('DC', 'creator'):
        author = item[0]

    chapters = []
    # Try to get TOC for chapter names
    toc_titles = {}
    for item in book.toc:
        if hasattr(item, 'title'):
            toc_titles[item.title] = True

    for item in book.get_items_of_type(9):  # ITEM_DOCUMENT
        content = item.get_content().decode('utf-8', errors='replace')
        extractor = HTMLTextExtractor()
        extractor.feed(content)
        text = extractor.get_text().strip()

        if not text or len(text) < 50:  # Skip near-empty pages
            continue

        # Try to extract heading from first line
        lines = text.split('\n')
        heading = lines[0].strip() if lines else f"Chapter {len(chapters) + 1}"

        # Check if heading matches a TOC entry
        for toc_title in toc_titles:
            if toc_title.lower() in heading.lower() or heading.lower() in toc_title.lower():
                heading = toc_title
                break

        chapters.append({
            "num": len(chapters) + 1,
            "heading": heading[:100],  # Cap heading length
            "text": text
        })

    if not chapters:
        sys.exit("Error: No text content found in EPUB.")

    language = detect_language(chapters[0]["text"][:2000])

    return {
        "title": title or Path(file_path).stem,
        "author": author or "Unknown",
        "language": language,
        "chapters": chapters
    }


def detect_language(sample: str) -> str:
    """Simple language detection based on character ranges."""
    if not sample:
        return "en"

    # Count characters by script
    cyrillic = len(re.findall(r'[\u0400-\u04FF]', sample))
    cjk = len(re.findall(r'[\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF]', sample))
    arabic = len(re.findall(r'[\u0600-\u06FF]', sample))
    greek = len(re.findall(r'[\u0370-\u03FF]', sample))
    devanagari = len(re.findall(r'[\u0900-\u097F]', sample))

    total = len(sample)
    if total == 0:
        return "en"

    if cyrillic / total > 0.1:
        return "ru"
    if cjk / total > 0.1:
        # Distinguish Chinese vs Japanese (hiragana/katakana)
        japanese = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF]', sample))
        return "ja" if japanese / total > 0.01 else "zh"
    if arabic / total > 0.1:
        return "ar"
    if greek / total > 0.1:
        return "el"
    if devanagari / total > 0.1:
        return "hi"

    # European language heuristics
    lower = sample.lower()
    if any(w in lower for w in ['der', 'die', 'das', 'und', 'ist', 'ein']):
        return "de"
    if any(w in lower for w in ['les', 'des', 'une', 'est', 'dans', 'pour']):
        return "fr"
    if any(w in lower for w in ['los', 'las', 'una', 'que', 'por', 'con']):
        return "es"
    if any(w in lower for w in ['os', 'das', 'uma', 'que', 'não', 'para']):
        return "pt"
    if any(w in lower for w in ['och', 'det', 'att', 'för', 'som', 'med']):
        return "sv"
    if any(w in lower for w in ['de', 'het', 'een', 'van', 'dat', 'niet']):
        return "nl"
    if any(w in lower for w in ['nie', 'jest', 'się', 'na', 'do', 'jak']):
        return "pl"
    if any(w in lower for w in ['il', 'la', 'che', 'non', 'per', 'sono']):
        return "it"
    if any(w in lower for w in ['bir', 've', 'bu', 'için', 'ile', 'olan']):
        return "tr"
    if any(w in lower for w in ['です', 'ます', 'した', 'して', 'ある', 'いない']):
        return "ja"
    if any(w in lower for w in ['은', '는', '이', '가', '을', '를', '에', '에서']):
        return "ko"

    return "en"


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF or EPUB")
    parser.add_argument("file", help="Path to PDF or EPUB file")
    parser.add_argument("--output", "-o", help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        sys.exit(f"Error: File not found: {file_path}")

    ext = file_path.suffix.lower()
    if ext == ".pdf":
        result = extract_pdf(str(file_path))
    elif ext == ".epub":
        result = extract_epub(str(file_path))
    else:
        sys.exit(f"Error: Unsupported format '{ext}'. Use .pdf or .epub")

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Extracted {len(result['chapters'])} chapters from '{result['title']}'", file=sys.stderr)
        print(f"Language: {result['language']}", file=sys.stderr)
        print(f"Output: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
