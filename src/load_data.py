"""Optional local knowledge-base helper.

The deployed API does not need this script because it reads banking_faq.txt
directly. It is kept for the original college project structure.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "banking_faq.txt"

if __name__ == "__main__":
    if DATA_FILE.exists():
        text = DATA_FILE.read_text(encoding="utf-8")
        print(f"Banking knowledge file found: {DATA_FILE}")
        print(f"Characters: {len(text)}")
    else:
        raise FileNotFoundError(f"Missing banking FAQ: {DATA_FILE}")
