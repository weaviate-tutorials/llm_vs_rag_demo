import weaviate
import weaviate.classes as wvc
import random
import logging
import loggerconfig


client = weaviate.connect_to_local()

vectorizer = random.choice(  # If you want to play vectorizer roulette
    [
        # wvc.Configure.Vectorizer.text2vec_cohere(
        #     model="embed-multilingual-v3.0"
        # ),
        wvc.Configure.Vectorizer.text2vec_openai(
            model="ada",
            model_version="002"
        ),
    ]
)

generative = random.choice(  # If you want to play LLM roulette
    [
        wvc.Configure.Generative.openai(model="gpt-4-1106-preview"),
        # wvc.Configure.Generative.cohere(),
    ]
)

client.collections.delete("Chunk")
chunks = client.collections.create(
    name="Chunk",
    vectorizer_config=vectorizer,
    generative_config=generative,
    properties=[
        wvc.Property(
            name="title",
            data_type=wvc.DataType.TEXT,
            tokenization=wvc.Tokenization.FIELD,
        ),
        wvc.Property(
            name="body",
            data_type=wvc.DataType.TEXT,
        ),
        wvc.Property(
            name="url",
            data_type=wvc.DataType.TEXT,
            skip_vectorization=True
        ),
        wvc.Property(
            name="chunk_no",
            data_type=wvc.DataType.INT,
        ),
    ],
)
