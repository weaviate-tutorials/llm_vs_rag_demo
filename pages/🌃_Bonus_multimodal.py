import logging
import loggerconfig
import streamlit as st
import llm
from helper import preset_prompts, get_client
import base64


client = get_client()
multimodal = client.collections.get("MultiModalCollection")

prompt = st.text_input(label="Multimodal search.", value="")

if len(prompt) > 0:
    search_response = multimodal.query.near_text(
        query=prompt,
        limit=3,
        return_properties=["text", "image"]
    )
    for o in search_response.objects:
        b64_img = o.properties["image"]
        img = base64.b64decode(b64_img)
        st.image(img, width=300)
