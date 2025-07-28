import re
from collections import defaultdict

def clean_text(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    if not text or len(text) < 3:
        return None
    if re.match(r'^(https?://|www\.)', text.lower()):
        return None
    return text

def extract_title_from_page(doc):
    blocks = doc[0].get_text("dict")["blocks"]
    candidates = []
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span["size"] > 15 and span["text"].strip().isupper():
                    candidates.append(span["text"].strip())
    if candidates:
        return " ".join(candidates).strip()
    return doc.metadata.get("title", "Untitled")

def get_top_font_levels(doc, max_levels=3):
    font_sizes = defaultdict(int)
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    font_sizes[round(span["size"], 1)] += 1

    sorted_sizes = sorted(font_sizes.items(), key=lambda x: -x[0])
    top_sizes = [size for size, _ in sorted_sizes[:max_levels]]
    return {size: f"H{i+1}" for i, size in enumerate(top_sizes)}
