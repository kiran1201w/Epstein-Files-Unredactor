#!/usr/bin/env python3
"""
reveal_keep_text_v4.py

Removes black censor overlays that are filled rectangles in the PDF content stream,
while keeping underlying text intact.

Fix vs earlier versions:
- Many PDFs never call 'rg'/'g' to set black; they rely on the default fill color (black).
  So we start with fill_is_black=True and update it if we see color-setting operators.

Usage:
  python reveal_keep_text_v4.py input.pdf output.pdf
"""

import sys
import fitz  # pip install pymupdf

FILL_OPS = {"f", "f*", "B", "B*", "b", "b*"}
TOL = 1e-8

def is_zero(x: float) -> bool:
    return abs(x) <= TOL

def tf(tok: str):
    try:
        return float(tok)
    except Exception:
        return None

def strip_black_rectangles(stream: str):
    toks = stream.split()
    out = []
    removed = 0

    # PDF default nonstroking fill color is black (DeviceGray 0)
    fill_is_black = True

    i = 0
    n = len(toks)

    while i < n:
        t = toks[i]

        # Track nonstroking fill color if explicitly set
        if t == "rg" and len(out) >= 3:
            r = tf(out[-3]); g = tf(out[-2]); b = tf(out[-1])
            if None not in (r, g, b):
                fill_is_black = is_zero(r) and is_zero(g) and is_zero(b)
            out.append(t); i += 1; continue

        if t == "g" and len(out) >= 1:
            gval = tf(out[-1])
            if gval is not None:
                fill_is_black = is_zero(gval)
            out.append(t); i += 1; continue

        if t == "k" and len(out) >= 4:
            c = tf(out[-4]); m = tf(out[-3]); y = tf(out[-2]); k = tf(out[-1])
            if None not in (c, m, y, k):
                # "black" commonly 0 0 0 1 k
                fill_is_black = is_zero(c) and is_zero(m) and is_zero(y) and abs(k - 1.0) <= 1e-4
            out.append(t); i += 1; continue

        # Remove filled rectangles when fill is black:
        #   x y w h re [h] f/f*/B/b...
        if t == "re" and fill_is_black and len(out) >= 4:
            x = tf(out[-4]); y = tf(out[-3]); w = tf(out[-2]); h = tf(out[-1])
            if None not in (x, y, w, h):
                j = i + 1
                if j < n and toks[j] == "h":
                    j += 1
                if j < n and toks[j] in FILL_OPS:
                    # drop the 4 numbers already added, and skip 're' + optional 'h' + fill op
                    out = out[:-4]
                    removed += 1
                    i = j + 1
                    continue

        out.append(t)
        i += 1

    return " ".join(out), removed


def process_pdf(input_pdf: str, output_pdf: str):
    doc = fitz.open(input_pdf)
    removed_total = 0

    for page in doc:
        contents = page.get_contents()
        if not contents:
            continue
        if isinstance(contents, int):
            contents = [contents]

        for xref in contents:
            raw = doc.xref_stream(xref)
            text = raw.decode("latin-1", errors="ignore")

            new_text, removed = strip_black_rectangles(text)
            if removed:
                doc.update_stream(xref, new_text.encode("latin-1"))
                removed_total += removed

    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()
    print(f"Done. Removed black rectangle overlays: {removed_total}")
    print(f"Output: {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reveal_keep_text_v4.py input.pdf output.pdf")
        sys.exit(1)
    process_pdf(sys.argv[1], sys.argv[2])
