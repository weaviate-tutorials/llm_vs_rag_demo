import weaviate
import os

preset_prompts = [
    "Select a prompt",
    "Explain how an LLM works, in the style of ELI5, but in a very casual, extremely Australian voice.",
    "Write a haiku about how a LLM works.",
    "Explain what the imagebind model is like I am five.",
    "What is hybrid search?",
    "Write a short biography of JP Hwang, who is an educator for Weaviate.",
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
