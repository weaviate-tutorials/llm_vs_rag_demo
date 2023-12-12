import weaviate
import weaviate.classes as wvc
import random
import logging
import loggerconfig


client = weaviate.connect_to_local()

generative = random.choice(
    [
        wvc.Configure.Generative.openai(model="gpt-4-1106-preview"),
        # wvc.Configure.Generative.cohere(),
    ]
)

client.collections.delete("MultiModalCollection")
multimodal = client.collections.create(
    name="MultiModalCollection",
    vectorizer_config=wvc.Configure.Vectorizer.multi2vec_clip(
        image_fields=["image"]
    ),
    generative_config=generative,
    properties=[
        wvc.Property(
            name="text",
            data_type=wvc.DataType.TEXT,
            tokenization=wvc.Tokenization.FIELD,
            skip_vectorization=True,
        ),
        wvc.Property(
            name="image",
            data_type=wvc.DataType.BLOB,
        ),
    ],
)
