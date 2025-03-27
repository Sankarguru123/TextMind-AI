import docx
from fastapi import APIRouter
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import pandas as pd
import json
import os

router = APIRouter()


@router.get("/extract_text/")
def extract_text(file_path: str):
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".pdf":
        doc = fitz.open(file_path)
        text = " ".join([page.get_text() for page in doc])
    elif file_ext in [".png", ".jpg", ".jpeg"]:
        text = pytesseract.image_to_string(Image.open(file_path))
    elif file_ext == ".csv":
        df = pd.read_csv(file_path)
        text = df.to_string()
    elif file_ext == ".json":
        with open(file_path, "r") as f:
            data = json.load(f)
            text = json.dumps(data, indent=4)
    elif file_ext in ["xlsx", "xls"]:  # Handling Excel files
        df = pd.read_excel(file_path)
        text = df.to_string()
    elif file_ext == "docx":  # Handling Word documents
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

    else:
        return {"error": "Unsupported file format"}

    return {"file_path": file_path, "extracted_text": text}
