from fastapi import FastAPI
from app.routes import analyze_image


app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(analyze_image.router)
