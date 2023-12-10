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
chunks = client.collections.get("Chunk")

for query, grouped_task, single_prompt, query_filter in [
    # (
    #     "retrieval augmented generation",
    #     """
    #         Using this information,
    #         explain what a retrieval augmented generation, or RAG is,
    #         and what aspects about RAG are discussed here.
    #     """,
    #     None,
    #     None,
    # ),
    (
        "large language model limitations",
        """
                Using this information,
                explain what key limitations large language models have currently,
                why that is the case,
                and how that might be a problem.
            """,
        None,
        None,
    ),
    (
        "large language model limitations",
        """
            Using this information,
            explain what key limitations large language models have currently,
            why that is the case,
            and how that might be a problem.
        """,
        None,
        wvc.Filter("title").not_equal(
            "Amplifying Limitations, Harms and Risks of Large Language Models"
        ),
    ),
]:
    response = chunks.generate.near_text(
        query=query,
        grouped_task=grouped_task,
        single_prompt=single_prompt,
        filters=query_filter,
        limit=10,
    )

    pprint(response.generated)
    for o in response.objects:
        print(o.properties["title"])
        print(o.properties["chunk_no"])
