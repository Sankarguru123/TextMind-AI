from fastapi import  FastAPI
from routes import file_upload,text_extraction,nlp_processing
import uvicorn


app = FastAPI(title="TextMind AI")

# Include routers
app.include_router(file_upload.router)
app.include_router(text_extraction.router)
app.include_router(nlp_processing.router)

@app.get("/")
def home():
    return {"message": "Welcome to TextMind AI"}
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)