from fastapi import APIRouter, UploadFile
from app.services.vision import classify_image

router = APIRouter()

@router.post("/analyze/image")
async def analyze_image(file: UploadFile):
    # save upload temporarily
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
    result = classify_image(file.filename)
    return {"labels": result}