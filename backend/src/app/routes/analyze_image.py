import tempfile
from fastapi import APIRouter, UploadFile, File
from app.services.vision import classify_image

router = APIRouter()

@router.post("/api/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name  # save path before closing
    
    # Now the file is closed, safe to open again
    result = classify_image(tmp_path, top_k=5)
    return {"result": result}