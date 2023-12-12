import weaviate
import weaviate.classes as wvc
from weaviate.util import generate_uuid5
from helper import COLL_NAME
from distyll import media, utils
import os
import logging
import loggerconfig


client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY"),
        "X-Cohere-Api-Key": os.getenv("COHERE_APIKEY"),
    }
)

chunks = client.collections.get(COLL_NAME)
logging.info(f"Adding data to {COLL_NAME}")

for arxiv_url in [
    "https://arxiv.org/pdf/2310.11703.pdf",
    "https://arxiv.org/abs/2305.05665",
    "https://arxiv.org/abs/2307.04821",
    "https://arxiv.org/abs/2311.00681",
    "https://arxiv.org/abs/2310.03214",
    "https://arxiv.org/pdf/2309.01431.pdf",
    "https://arxiv.org/abs/2202.01110",
    "https://arxiv.org/pdf/2103.04831.pdf",
    "https://arxiv.org/pdf/2104.08663.pdf"
    # Hybrid car articles
    "https://arxiv.org/pdf/2311.11107.pdf",
    "https://arxiv.org/pdf/2309.17442.pdf",
    "https://arxiv.org/pdf/2309.09804.pdf"
]:
    logging.info(f"Importing {arxiv_url}")

    arxiv_data = media.get_arxiv_paper(arxiv_url)

    text_chunks = utils.chunk_text(arxiv_data["text"])

    logging.info(f"Vectorizing {len(text_chunks)} chunks.")
    data_objects = list()
    for i, text_chunk in enumerate(text_chunks):
        props = {
            "title": arxiv_data["title"],
            "body": text_chunk,
            "url": arxiv_data["url"],
            "chunk_no": i + 1,
        }
        data_objects.append(
            wvc.DataObject(
                properties=props,
                uuid=generate_uuid5(props),
            )
        )

    import_response = chunks.data.insert_many(data_objects)

    logging.info(f"Has errors? {import_response.has_errors}")
    if import_response.has_errors:
        logging.info(f"{len(import_response.errors)} errors found.")
