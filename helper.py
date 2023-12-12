import weaviate
import os

COLL_NAME = "ChunkGPT35"

preset_prompts = [
    "Select a prompt",
    "Explain how a large language model works.",
    "Explain how an LLM works, in a very casual, extremely Australian voice.",
    "Write a haiku about how a LLM works.",
    "Write a short biography of JP Hwang, who is a an educator for Weaviate.",
    "We did it! I won the big boxing match! Provide key reasons for this triumph.",
    "Explain what the imagebind model is like I am five.",
    "What is hybrid search?",
    "Why is efficiency of hybrid so important?",
    "Custom"
]


def get_client():
    client = weaviate.connect_to_local(
        headers={
            "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY"),
            "X-Cohere-Api-Key": os.getenv("COHERE_APIKEY"),
        }
    )
    return client
