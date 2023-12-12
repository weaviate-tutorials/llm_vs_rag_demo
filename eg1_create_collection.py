import weaviate
import weaviate.classes as wvc
import logging
import loggerconfig


client = weaviate.connect_to_local()

client.collections.delete("Chunk")
chunks = client.collections.create(
    name="Chunk",
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_openai(),
    generative_config=wvc.Configure.Generative.openai(model="gpt-4-1106-preview"),
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
