from pathlib import Path


def load_stylesheet(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


STYLES_DIR = Path(__file__).resolve().parent.parent / "gui" / "styles"
