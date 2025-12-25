# Epstein-Files-Unredactor
A Python tool that reveals text hidden by fake PDF redactions by removing black overlay rectangles while preserving all underlying text. Works on multi-page PDFs across macOS and Windows.

# PDF Overlay Revealer (Fake Redaction Remover)

## 🚨 Overview

Many PDFs use **fake redaction**.

Instead of deleting sensitive text, they place **black rectangles on top of the text**.
Visually it looks hidden — but the text is still there.

That’s why:
- Copy-pasting from PDFs reveals “hidden” text
- Text extraction tools can still read censored content

This tool removes those **black overlay rectangles** while keeping the **original text intact**.

---

## ✅ What This Tool Does

- Scans **all pages** of a PDF
- Detects **black vector overlay rectangles**
- Removes **only the black boxes**
- Preserves **all underlying text**
- Works on **large PDFs** (hundreds of pages)

---

## ❌ What This Tool Does NOT Do

- ❌ Does NOT recover text that was actually deleted
- ❌ Does NOT work on scanned/image-only PDFs
- ❌ Does NOT bypass real redaction

If text exists under the black box → it will be revealed  
If it doesn’t exist → nothing can recover it

---

## 🖥️ Requirements

- Python **3.8 or newer**
- Works on **macOS** and **Windows**

---

## 📦 Installation

pip install pymupdf

Usage:

python epstein.py input.pdf output.pdf

📊 Example Output
Done. Removed black rectangle overlays: 1342
Output: revealed.pdf

🧠 How It Works (Simple)
Fake redactions are usually rectangles drawn over text
This tool removes only those rectangle drawing commands
Text commands are never modified
No OCR. No repainting. No guessing.

⚠️ Limitations
Black boxes baked into images cannot be removed
Truly deleted text cannot be recovered
Works only on vector-based overlays


