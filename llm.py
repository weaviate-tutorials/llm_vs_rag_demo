from openai import OpenAI
import os
from pprint import pprint

PROMPT_TEMPLATE = """
 IMPORTANT NOTE: The answer must be short, such as within 2-5 sentences, 
or within 2-4 short bullet points, each bullet point being a sentence or two maximum.
"""

RAG_SUFFIX = """
"""


def init_openai():
    client = OpenAI()
    client.api_key = os.getenv("OPENAI_APIKEY")
    return client


def get_llm_response(prompt):
    client = init_openai()
    response = client.chat.completions.create(
        # model="gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    for q in [
        # "Explain what a DDoS attack is",
        # "Explain how a LLM works",
        # "Explain how an LLM works, in the style of ELI5, but in a very casual, extremely Australian voice.",
        # "Explain what the imagebind model is, and what its benefits might be",
        # "Explain what the benefits of hybrid search is",
        """
        explain what key limitations large language models have currently,
        why that is the case,
        and how that might be a problem.
        """
    ]:
        response_txt = get_llm_response(q)

        pprint(response_txt)
