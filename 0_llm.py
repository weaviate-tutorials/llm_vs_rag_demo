from openai import OpenAI
import os

client = OpenAI()
client.api_key = os.getenv("OPENAI_APIKEY")

response = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain what the imagebind model is, and what its benefits might be"}
  ]
)

print(response.choices)

"Explain what a DDoS attack is"
"Explain how a LLM works"
"Explain how an LLM works, in the style of ELI5, but in a very casual, extremely Australian voice."
"Explain what the imagebind model is, and what its benefits might be"
"Explain what the benefits of hybrid search is"


