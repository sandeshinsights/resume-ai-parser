from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from parser import parse_cv_with_gemini
from utils import extract_text_from_pdf
from validator import clean_data

app = FastAPI(title="ResumeAI")

@app.get("/", response_class=HTMLResponse)
async def home():
    try:
        return open("templates/index.html", "r", encoding="utf-8").read()
    except Exception as e:
        return f"<h1>Error: {e}</h1>"

@app.post("/api/parse-cv")
async def parse_cv(file: UploadFile = File(...)):
    try:
        content = await file.read()
        if len(content) == 0:
            return JSONResponse(status_code=400, content={"error": "Empty file"})
        text = extract_text_from_pdf(content)
        if not text or len(text.strip()) < 20:
            return JSONResponse(status_code=422, content={"error": "Could not extract text from PDF"})
        parsed = parse_cv_with_gemini(text)
        cleaned = clean_data(parsed)
        return cleaned
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})