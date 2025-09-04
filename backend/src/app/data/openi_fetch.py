import os, json, requests
import time
from PIL import Image
from io import BytesIO

OPENI_ENDPOINT = "https://openi.nlm.nih.gov/api/search"
BASE_URL = "https://openi.nlm.nih.gov"

def fetch_openi_samples(query="chest xray",
                        want=15,
                        per_page=50,
                        n=10,
                        out_dir="data/openi",
                        image_type="x"):
    """
    Fetch N amount of chest xray images and captions from OpenI
    Save as PNGs so I dont have to downlaod the whole database
    """

    os.makedirs(out_dir, exist_ok=True)
    saved_meta = []
    page = 1
    seen_urls = set()

    while len(saved_meta) < want:
        params = {
            "m": page,
            "n": per_page,
            "query": query
        }

        if image_type:
            params["it"] = image_type

        try:
            r = requests.get(OPENI_ENDPOINT, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            items = data.get("list", [])
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

        if not items:
            print("No more items found.")
            break

        for item in items:
            if len(saved_meta) >= want:
                break

            raw_url = item.get("imgLarge") or item.get("img") or item.get("imgThumb")
            if not raw_url or raw_url in seen_urls:
                continue

            # Prepend base url if needed 
            if raw_url.startswith("/"):
                img_url = BASE_URL + raw_url
            else:
                img_url = raw_url

            caption = item.get("caption", "No caption")
            pmcid = item.get("pmcid")

            try:
                img_bytes = requests.get(img_url, timeout=30).content
                img = Image.open(BytesIO(img_bytes)).convert("L")
                img_path = os.path.join(out_dir, f"openi_{len(saved_meta)}.png")
                img.save(img_path)

                saved_meta.append({
                    "image_path": img_path,
                    "caption": caption,
                    "pmcid": pmcid,
                })
                seen_urls.add(raw_url)
                print(f"Saved {img_path}")
            except Exception as e:
                print(f"Error downloading image {img_url}: {e}")
                continue

        print(f"[page {page}] total saved so far: {len(saved_meta)}")
        page += 1
        time.sleep(0.4)  # be polite to the API

    # Write metadata
    meta_path = os.path.join(out_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(saved_meta, f, indent=2)

    print(f"Saved {len(saved_meta)} images to {out_dir}")
    return len(saved_meta)