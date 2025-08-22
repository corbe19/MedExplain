from transformers import pipeline

_classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

def classify_image(path: str, top_k: int = 5):
    preds = _classifier(path, top_k=top_k)
    # normalize to {label, score}
    return [{"label": p["label"], "score": float(p["score"])} for p in preds]
