from fastapi import  APIRouter,File,UploadFile
import shutil
import os


router = APIRouter()

upload_dir = 'data/'
os.makedirs(upload_dir, exist_ok=True)


@router.post("/upload/")

async def upload_file(file:UploadFile = File(...)):
    file_path = os.path.join(upload_dir,file.filename)
    with open(file_path,'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename":file.filename, "file_path":file_path}
