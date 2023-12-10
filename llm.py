from openai import OpenAI
import os
from pprint import pprint

client = OpenAI()
client.api_key = os.getenv("OPENAI_APIKEY")


def get_llm_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
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
