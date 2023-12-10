import weaviate
import weaviate.classes as wvc
import os
import logging
from pprint import pprint


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

titles = chunks.aggregate_group_by.over_all(
    group_by="title",
    return_metrics=wvc.Metrics("title").text(top_occurrences_value=True),
)

for t in titles:
    print(t.grouped_by.value)
