import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os

# If tesseract is not in PATH (Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

doc = fitz.open("books/WZ2FQlnIXv7NfZW.pdf")

os.makedirs("chunked_books", exist_ok=True)

for i, page in enumerate(doc):
    # render page to image (important: use high DPI)
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # OCR
    text = pytesseract.image_to_string(img, lang="ben")

    with open(f"chunked_books/{i}.txt", "w", encoding="utf-8") as f:
        f.write(text)
