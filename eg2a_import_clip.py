import weaviate
import weaviate.classes as wvc
from weaviate.util import generate_uuid5
import os
import base64
from pathlib import Path
import logging
import loggerconfig


client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY"),
        "X-Cohere-Api-Key": os.getenv("COHERE_APIKEY"),
    }
)
multimodal = client.collections.get("MultiModalCollection")

pic_dir = Path("clip_pics")
for pic_path in pic_dir.glob("*.jpg"):
    logging.info(f"Importing {pic_path}")
    content = pic_path.read_bytes()
    b64_img = base64.b64encode(content).decode("utf-8")

    pic_data = {
        "text": str(pic_path.name),
        "image": b64_img
    }

    r = multimodal.data.insert(
        properties=pic_data,
        uuid=generate_uuid5(b64_img)
    )
    print(r)
