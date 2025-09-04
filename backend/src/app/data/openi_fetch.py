import os, json, requests
from PIL import Image
from io import BytesIO

OPENI_ENDPOINT = "https://openi.nlm.nih.gov/api/search"
BASE_URL = "https://openi.nlm.nih.gov"

def fetch_openi_samples(query="chest xray", n=10, out_dir="data/openi"):
    """
    Fetch N amount of chest xray images and captions from OpenI
    Save as PNGs so I dont have to downlaod the whole database
    """

    os.makedirs(out_dir, exist_ok=True)
    params = {
        "m": 1,
        "n": n,
        "it": "xg",
        "query": query
    }
    r = requests.get(OPENI_ENDPOINT, params=params)
    r.raise_for_status()
    data = r.json()

    saved = []
    for i, item in enumerate(data.get("list", [])):
        raw_url = item.get("imgLarge") or item.get("img") or item.get("imgThumb")

        if not raw_url:
            continue

        # Prepend base url if needed 
        if raw_url.startswith("/"):
            img_url = BASE_URL + raw_url
        else:
            img_url = raw_url

        caption = item.get("caption", "No caption")
        pmcid = item.get("pmcid")

        img_bytes = requests.get(img_url, timeout=30).content
        img = Image.open(BytesIO(img_bytes)).convert("L")
        img_path = os.path.join(out_dir, f"openi_{i}.png")
        img.save(img_path)

        saved.append({
            "image_path": img_path,
            "caption": caption,
            "pmcid": pmcid,
        })

        with open(os.path.join(out_dir, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(saved, f, indent=2)

        return len(saved)
