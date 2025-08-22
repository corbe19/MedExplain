from fastapi import APIRouter, UploadFile
from app.services.vision import classify_image

router = APIRouter(prefix="/analyze", tags=["analyze"])

@router.post("/image")
async def analyze_image(file: UploadFile):
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
    result = classify_image(file.filename)
    return {"labels": result}
