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

st.title("Why RAG needs great search.")

selected_prompt = st.selectbox(label="Select a prompt", options=preset_prompts)
n_chunks_manual = st.number_input(label="Number of chunks to fetch", value=3)

if selected_prompt == "Custom":
    prompt = st.text_input(label="Ask the LLM anything.", value="")
elif selected_prompt == "Select a prompt":
    prompt = ""
else:
    prompt = selected_prompt


full_prompt = prompt + llm.PROMPT_TEMPLATE

st.subheader("Why search is key to better RAG")
st.write("This will use Weaviate to help the LLM answer the question.")
search_query = st.text_input(label="Search our database to help the LLM", value="")

# e.g. try:
# hybrid search difference, or hybridsearch

top_col1, top_col2 = st.columns(2, gap="medium")
with top_col1:
    st.markdown("### Keyword search only")
    if len(search_query) > 0:
        search_response = chunks.query.bm25(
            query=search_query,
            limit=n_chunks_manual,
        )
        with st.expander("Chunks used:"):
            for o in search_response.objects:
                st.write(o.properties["title"] + " chunk no: " + str(o.properties["chunk_no"]))
                st.caption(o.properties["body"])
                st.divider()
with top_col2:
    st.markdown("### Hybrid search")
    if len(search_query) > 0:
        search_response = chunks.query.hybrid(
            query=search_query,
            limit=n_chunks_manual,
        )
        with st.expander("Chunks used:"):
            for o in search_response.objects:
                st.write(o.properties["title"] + " chunk no: " + str(o.properties["chunk_no"]))
                st.caption(o.properties["body"])
                st.divider()


col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("### Response")
    if len(search_query) > 0 and len(prompt) > 0:
        rag_response = chunks.generate.bm25(
            query=search_query,
            grouped_task=prompt + llm.RAG_SUFFIX,
            limit=n_chunks_manual,
        )
        st.write(rag_response.generated)

with col2:
    st.markdown("### Response")
    if len(search_query) > 0 and len(prompt) > 0:
        rag_response = chunks.generate.hybrid(
            query=search_query,
            grouped_task=prompt + llm.RAG_SUFFIX,
            limit=n_chunks_manual,
        )
        st.write(rag_response.generated)
