# utils/pdf_reader.py
from io import BytesIO
from typing import Tuple, List
import pdfplumber

# OCR optionnels
try:
    from pdf2image import convert_from_bytes
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False


def read_pdf_all_text(file_bytes: bytes, ocr_on_empty: bool = True, dpi: int = 300) -> Tuple[str, List[str], bool]:
    """
    Tente d'abord l'extraction texte avec pdfplumber (meilleur pour Digiforma).
    Si le texte est (quasi) vide et que OCR est dispo, applique un OCR page par page.
    Retourne: texte_concat, liste_textes_par_page, used_ocr
    """
    used_ocr = False
    text_pages: List[str] = []

    # 1) Texte brut via pdfplumber
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text(x_tolerance=2, y_tolerance=1, layout=True) or ""
            text_pages.append(txt)

    full_text = "\n".join(text_pages).strip()

    # 2) Fallback OCR si quasi vide
    if ocr_on_empty and len(full_text) < 30 and OCR_AVAILABLE:
        used_ocr = True
        images = convert_from_bytes(file_bytes, dpi=dpi)
        text_pages = []
        for im in images:
            txt = pytesseract.image_to_string(im, lang="fra")
            text_pages.append(txt or "")
        full_text = "\n".join(text_pages).strip()

    return full_text, text_pages, used_ocr