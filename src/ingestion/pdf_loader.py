import json
import os
import re
import pdfplumber
from typing import List, Dict

from config.settings import (
    PDF_PATH,
    PAGES_PATH,
    BOOK_SEQUENCE
)
from src.utils.logger import get_logger

logger = get_logger(__name__)

# ---------- Regex ----------
CHAPTER_PATTERN = re.compile(r"^CHAPTER\s+\w+", re.IGNORECASE)
CHAPTER_ONE_PATTERN = re.compile(r"^CHAPTER\s+ONE$", re.IGNORECASE)


def validate_output_file():
    if os.path.exists(PAGES_PATH):
        try:
            with open(PAGES_PATH, "r", encoding="utf-8") as f:
                json.load(f)
            raise RuntimeError(
                "pages.json already exists and is valid. "
                "Delete it manually to regenerate."
            )
        except json.JSONDecodeError:
            raise RuntimeError(
                "pages.json exists but is corrupted. "
                "Delete it before re-running ingestion."
            )


def load_pdf_pages() -> List[Dict]:
    pages = []

    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    validate_output_file()

    current_book = None
    current_chapter = None
    book_index = -1

    logger.info(f"Loading PDF: {PDF_PATH}")

    try:
        with pdfplumber.open(PDF_PATH) as pdf:
            for idx, page in enumerate(pdf.pages):
                page_no = idx + 1

                try:
                    text = page.extract_text()
                except Exception as e:
                    logger.warning(f"Page {page_no}: extraction failed ({e})")
                    continue

                if not text or not text.strip():
                    # Image-only page → ignore here
                    continue

                text = text.strip()
                lines = [l.strip() for l in text.splitlines() if l.strip()]

                # ---------- Chapter Detection ----------
                if lines and CHAPTER_PATTERN.match(lines[0]):
                    chapter_header = lines[0]

                    # ✅ BOOK CHANGE LOGIC (CORRECT)
                    if CHAPTER_ONE_PATTERN.match(chapter_header):
                        book_index += 1
                        if book_index >= len(BOOK_SEQUENCE):
                            logger.warning(
                                f"Extra CHAPTER ONE detected at page {page_no}"
                            )
                        else:
                            current_book = BOOK_SEQUENCE[book_index]
                            logger.info(
                                f"New book detected: {current_book} (page {page_no})"
                            )

                    # Chapter title may span two lines
                    current_chapter = (
                        f"{chapter_header}: {lines[1]}"
                        if len(lines) > 1 else chapter_header
                    )

                    logger.info(
                        f"Chapter detected: {current_chapter} (page {page_no})"
                    )

                pages.append({
                    "page_no": page_no,
                    "book": current_book,
                    "chapter": current_chapter,
                    "text": text
                })

        if not pages:
            raise RuntimeError("No text pages extracted.")

        logger.info(f"Successfully extracted {len(pages)} pages")
        return pages

    except Exception:
        logger.exception("PDF ingestion failed")
        raise


def save_pages(pages: List[Dict]):
    try:
        temp_path = PAGES_PATH + ".tmp"

        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(pages, f, indent=2, ensure_ascii=False)

        os.replace(temp_path, PAGES_PATH)
        logger.info(f"pages.json written to {PAGES_PATH}")

    except Exception:
        logger.exception("Failed to write pages.json")
        raise


if __name__ == "__main__":
    logger.info("Running pdf_loader")

    pages = load_pdf_pages()
    save_pages(pages)

    logger.info("PDF loading completed")
