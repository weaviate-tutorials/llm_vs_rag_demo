import weaviate
import weaviate.classes as wvc
from weaviate.util import generate_uuid5
from distyll import media, utils
import os
import logging


logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)

logger = logging.getLogger(__name__)

client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY"),
        "X-Cohere-Api-Key": os.getenv("COHERE_APIKEY"),
    }
)
chunks = client.collections.get("Chunk")

for arxiv_url in [
    "https://arxiv.org/pdf/2310.11703.pdf",
    "https://arxiv.org/abs/2305.05665",
    "https://arxiv.org/abs/2307.04821",
    "https://arxiv.org/abs/2311.00681",
    "https://arxiv.org/abs/2310.03214",
    "https://arxiv.org/pdf/2309.01431.pdf",
    "https://arxiv.org/abs/2202.01110",
]:
    logger.info(f"Importing {arxiv_url}")

    arxiv_data = media.get_arxiv_paper(arxiv_url)

    text_chunks = utils.chunk_text(arxiv_data["text"])

    logger.info(f"Vectorizing {len(text_chunks)} chunks.")
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

    logger.info(f"Has errors? {import_response.has_errors}")
    if import_response.has_errors:
        logger.info(import_response.errors)
