from transformers import pipeline

classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

def classify_image(path: str):
    return classifier(path)

