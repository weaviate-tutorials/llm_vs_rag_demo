import weaviate
import weaviate.classes as wvc
from weaviate.util import generate_uuid5
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
chunks = client.collections.get("Chunk")

for (title, pdf_path) in [
    ("Sparse, Dense, and Attentional Representations for Text Retrieval", "dl_data/tacl_a_00369.pdf")
]:
    logging.info(f"Importing {pdf_path}")

    pdf_text = media._parse_pdf(pdf_path)
    text_chunks = utils.chunk_text(pdf_text)

    logging.info(f"Vectorizing {len(text_chunks)} chunks.")
    data_objects = list()
    for i, text_chunk in enumerate(text_chunks):
        props = {
            "title": title,
            "body": text_chunk,
            "url": pdf_path,
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
        logging.info(import_response.errors)
