import pdfplumber

def extract_text_from_pdf(content: bytes):
    import io
    text = ""
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text[:12000]