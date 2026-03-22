import os
from langchain_core.tools import tool
from ddgs import DDGS
import trafilatura
from config import MAX_TEXT_LENGTH, OUTPUT_DIR

@tool
def web_search(query: str) -> str:
    """Шукає інформацію в інтернеті. Повертає стислий список результатів."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    
    formatted = []
    for r in results:
        formatted.append(
            f"Title: {r.get('title')}\n"
            f"URL: {r.get('href')}\n"
            f"Snippet: {r.get('body')}\n"
        )
    
    return "\n---\n".join(formatted)

@tool
def read_url(url: str) -> str:
    """Отримує повний текстовий контент веб-сторінки за URL."""
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return "Помилка: не вдалося завантажити сторінку."
    
    text = trafilatura.extract(downloaded)
    if not text:
        return "Помилка: не вдалося витягти текст зі сторінки."
    
    text = text.strip()
    return text[:MAX_TEXT_LENGTH]

@tool
def write_report(filename: str, content: str) -> str:
    """Записує контент у файл Markdown. filename має закінчуватися на .md"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"✅ Звіт успішно збережено у файл: {path}"
