
from typing import List, Tuple
from pathlib import Path

def parse_lines(text: str) -> List[Tuple[str, str]]:
    """
    Parse lines in format: 'question -> answer' OR 'question\tanswer'.
    Lines starting with # are ignored.
    """
    pairs = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if '\t' in line:
            q, a = [part.strip() for part in line.split('\t', 1)]
        elif '->' in line:
            q, a = [part.strip() for part in line.split('->', 1)]
        else:
            # If no delimiter, skip line as invalid
            continue
        if q and a:
            pairs.append((q, a))
    return pairs

def read_cards(file_path: Path) -> List[Tuple[str, str]]:
    if not file_path.exists():
        return []
    text = file_path.read_text(encoding='utf-8')
    return parse_lines(text)

def append_card(file_path: Path, question: str, answer: str) -> None:
    line = f"{question.strip()} -> {answer.strip()}\n"
    with file_path.open('a', encoding='utf-8') as f:
        f.write(line)

def overwrite_cards(file_path: Path, pairs: List[Tuple[str, str]]) -> None:
    text = ''.join(f"{q} -> {a}\n" for q, a in pairs)
    file_path.write_text(text, encoding='utf-8')
