import weaviate
import weaviate.classes as wvc
import os
import logging
import loggerconfig
import streamlit as st
import llm
from helper import preset_prompts, get_client


N_CHUNKS = 10

client = get_client()
chunks = client.collections.get("Chunk")

st.set_page_config(
    page_title="RAG: LLMs + Weaviate",
    page_icon="🤖",
)

st.title("RAG to the rescue!")

selected_prompt = st.selectbox(label="Select a prompt", options=preset_prompts)

if selected_prompt == "Custom":
    prompt = st.text_input(label="Ask the LLM anything.", value="")
elif selected_prompt == "Select a prompt":
    prompt = ""
else:
    prompt = selected_prompt


full_prompt = prompt + llm.PROMPT_TEMPLATE

top_col1, top_col2 = st.columns(2, gap="medium")
with top_col1:
    st.subheader("LLM only (dumb genius)")
    st.write("This simply asks the LLM for an answer to our question.")
with top_col2:
    st.subheader("With help from Weaviate")
    st.write("This will use Weaviate to help the LLM answer the question.")
    if len(prompt) > 0:
        search_response = chunks.query.near_text(
            query=prompt,
            limit=N_CHUNKS,
        )
        with st.expander("Chunks used:"):
            for o in search_response.objects:
                st.write(o.properties["title"] + " chunk no: " + str(o.properties["chunk_no"]))
                st.caption(o.properties["body"])
                st.divider()


col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("### Response")
    if len(prompt) > 0:
        raw_response = llm.get_llm_response(prompt)
        st.write(raw_response)

with col2:
    st.markdown("### Response")
    if len(prompt) > 0:
        rag_response = chunks.generate.near_text(
            query=prompt,
            grouped_task=prompt + llm.RAG_SUFFIX,
            limit=N_CHUNKS,
        )
        st.write(rag_response.generated)
