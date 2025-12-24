import json
import os
from typing import List

from config.settings import (
    PAGES_PATH,
    CHUNKS_PATH,
    NARRATIVE_CHUNK_SIZE,
    NARRATIVE_OVERLAP
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


# -------- Poem / Song Detection --------
def is_poem(text: str) -> bool:
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) < 4:
        return False

    avg_line_len = sum(len(l) for l in lines) / len(lines)
    return avg_line_len < 50


# -------- Narrative Chunking --------
def sliding_window(words: List[str]) -> List[str]:
    chunks = []
    start = 0

    while start < len(words):
        end = start + NARRATIVE_CHUNK_SIZE
        chunks.append(" ".join(words[start:end]))
        start = end - NARRATIVE_OVERLAP

    return chunks


def run():
    if not os.path.exists(PAGES_PATH):
        raise FileNotFoundError("pages.json not found. Run pdf_loader first.")

    with open(PAGES_PATH, "r", encoding="utf-8") as f:
        pages = json.load(f)

    chunks = []
    chunk_id = 0

    current_book = None
    current_chapter = None
    chapter_id = -1

    buffer_text = []
    buffer_page_nos = []

    def flush_buffer():
        nonlocal chunk_id
        if not buffer_text:
            return

        text = "\n".join(buffer_text)
        words = text.split()

        for chunk in sliding_window(words):
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk,
                "book": current_book,
                "chapter": current_chapter,
                "chapter_id": chapter_id,
                "page_no": buffer_page_nos[0]
            })
            chunk_id += 1

        buffer_text.clear()
        buffer_page_nos.clear()

    for page in pages:
        book = page["book"]
        chapter = page["chapter"]
        text = page["text"]

        # -------- Book Change --------
        if book != current_book:
            flush_buffer()
            current_book = book
            current_chapter = None
            chapter_id = -1
            logger.info(f"Chunking new book: {current_book}")

        # -------- Chapter Change --------
        if chapter != current_chapter:
            flush_buffer()
            current_chapter = chapter
            chapter_id += 1
            logger.info(
                f"Chunking chapter {chapter_id}: {current_chapter}"
            )

        # -------- Poem Handling (NO windowing) --------
        if is_poem(text):
            flush_buffer()
            chunks.append({
                "chunk_id": chunk_id,
                "text": text,
                "book": current_book,
                "chapter": current_chapter,
                "chapter_id": chapter_id,
                "page_no": page["page_no"]
            })
            chunk_id += 1
            continue

        # -------- Narrative Buffer --------
        buffer_text.append(text)
        buffer_page_nos.append(page["page_no"])

    flush_buffer()

    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    logger.info(f"Chunking completed: {len(chunks)} chunks created")


if __name__ == "__main__":
    run()


