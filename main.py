import os
import json
import fitz  # PyMuPDF
from utils import clean_text, extract_title_from_page, get_top_font_levels

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    size_to_level = get_top_font_levels(doc)
    outline = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = round(span["size"], 1)
                    text = clean_text(span["text"])
                    if text and size in size_to_level:
                        outline.append({
                            "level": size_to_level[size],
                            "text": text,
                            "page": page_num
                        })

    return {
        "title": extract_title_from_page(doc),
        "outline": outline
    }

def main():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            result = extract_headings(pdf_path)
            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"✅ Processed: {filename}")

if __name__ == "__main__":
    main()
