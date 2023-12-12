import weaviate
import weaviate.classes as wvc
import os
import logging
import loggerconfig
from pprint import pprint


client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY"),
        "X-Cohere-Api-Key": os.getenv("COHERE_APIKEY"),
    }
)
multimodal = client.collections.get("MultiModalCollection")

print(multimodal.aggregate.over_all(total_count=True))

response = multimodal.query.fetch_objects(
    limit=2,
    include_vector=True
)

for o in response.objects:
    print(o.properties)
    print(o.vector)

rand_id = o.uuid

response = multimodal.query.near_object(
    near_object=rand_id,
    limit=2,
)

for o in response.objects:
    print(o.properties)


print(response)
for o in response.objects:
    print(o.properties["text"])

for q in ["animal", "building"]:
    response = multimodal.query.near_text(
        query=q,
        limit=2,
    )

    print(response)
    for o in response.objects:
        print(o.properties)
