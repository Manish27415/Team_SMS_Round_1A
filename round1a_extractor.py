import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from collections import defaultdict

class PDFOutlineExtractor:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def extract_outline(self, pdf_path: str) -> dict:
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            title = metadata.get("title") or os.path.splitext(os.path.basename(pdf_path))[0]
            outline = self._extract_headings(doc)
            return {
                "title": title.strip(),
                "outline": outline
            }
        except Exception as e:
            print(f"Error while processing '{pdf_path}': {e}")
            return {
                "title": "Unknown",
                "outline": []
            }

    def _extract_headings(self, doc) -> list:
        headings = []
        for page_number in range(len(doc)):
            page = doc[page_number]
            blocks = page.get_text("dict").get("blocks", [])
            for block in blocks:
                for line in block.get("lines", []):
                    spans = line.get("spans", [])
                    texts = [span["text"].strip() for span in spans if "text" in span]
                    sizes = [span["size"] for span in spans if "size" in span]
                    if not texts or not sizes:
                        continue

                    combined_text = " ".join(texts).strip()
                    font_size = max(sizes)
                    heading_level = self._infer_heading_level(font_size)

                    if heading_level and 3 <= len(combined_text) <= 100:
                        headings.append({
                            "level": heading_level,
                            "text": combined_text,
                            "page": page_number + 1
                        })
        return headings

    def _infer_heading_level(self, size: float) -> str:
        if size >= 18:
            return "H1"
        elif 14 <= size < 18:
            return "H2"
        elif 11 <= size < 14:
            return "H3"
        return None

    def process_all_pdfs(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        for filename in os.listdir(self.input_dir):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(self.input_dir, filename)
                output = self.extract_outline(full_path)
                json_file = os.path.join(self.output_dir, filename.replace(".pdf", ".json"))
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(output, f, indent=4, ensure_ascii=False)
                print(f"Processed: {filename}")

if __name__ == "__main__":
    start_time = datetime.now()

    input_dir = "/app/input"
    output_dir = "/app/output"
    processor = PDFOutlineExtractor(input_dir, output_dir)
    processor.process_all_pdfs()

    end_time = datetime.now()
    print(f"⏱ Completed in {(end_time - start_time).total_seconds():.2f} seconds")
