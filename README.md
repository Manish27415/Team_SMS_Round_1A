# Team_SMS_Round_1A– Structured PDF Outline Extractor

## 🚀 Overview
This project extracts a structured outline from PDF files by detecting the document title and hierarchical headings (H1, H2, H3) with their corresponding page numbers. It is designed to work offline and run inside a Docker container.

## 🧠 Core Features
- Extracts:
  - Document title
  - Headings (H1, H2, H3) using font size heuristics
  - Page numbers for each heading
- Accepts PDFs up to 50 pages
- Generates structured JSON output
- Fully offline, CPU-compatible
- Compliant with Adobe Hackathon Round 1A specs

## 📂 Input/Output
- Input: PDFs placed inside `/app/input`
- Output: JSON files inside `/app/output`, named as `<input-filename>.json`

### ✅ JSON Output Format
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## 🐳 Docker Instructions
### 🏗 Build the image
```bash
docker build --platform linux/amd64 -t outline_extractor:round1a .
```

### ▶ Run the container
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none outline_extractor:round1a
```

## 📦 Dependencies
- Python 3.10
- [PyMuPDF](https://pymupdf.readthedocs.io/) (`pip install pymupdf`)


## ⚠️ Constraints Met
- ✅ No Internet Access
- ✅ CPU-only
- ✅ Max 10s for 50 pages
- ✅ No hardcoding
- ✅ Model-free, <200MB dependencies

---

Made with ❤️ for Adobe India Hackathon 2025
