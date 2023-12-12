import logging
import loggerconfig
import streamlit as st
import llm
from helper import preset_prompts, get_client


N_CHUNKS = 5

client = get_client()
chunks = client.collections.get("Chunk")
agg_resp = chunks.aggregate.over_all(total_count=True)
obj_count = agg_resp.total_count

st.set_page_config(
    page_title="RAG: LLMs + Weaviate",
    page_icon="🤖",
)

st.title("Why RAG needs great search.")

selected_prompt = st.selectbox(label="Select a prompt", options=preset_prompts)

if selected_prompt == "Custom":
    prompt = st.text_area(label="Ask the LLM anything.", value="", height=50)
elif selected_prompt == "Select a prompt":
    prompt = ""
else:
    prompt = selected_prompt

search_query = st.text_input(label="Search our database to help the LLM", value="")
search_type = st.selectbox(label="Search type", options=["Select one", "Keyword", "Vector", "Hybrid"])
n_chunks_manual = st.number_input(label="Number of chunks to fetch", value=3)
full_prompt = prompt + llm.PROMPT_TEMPLATE


# e.g. try:
# hybrid search difference, or hybridsearch

if search_type == "Keyword":
    srch_query = chunks.query.bm25
    gen_query = chunks.generate.bm25
elif search_type == "Vector":
    srch_query = chunks.query.near_text
    gen_query = chunks.generate.near_text
elif search_type == "Hybrid":
    srch_query = chunks.query.hybrid
    gen_query = chunks.generate.hybrid
else:
    srch_query = None
    gen_query = None


if len(search_query) > 0 and srch_query is not None:
    search_response = srch_query(
        query=search_query,
        limit=n_chunks_manual,
    )
    with st.expander("Chunks used:"):
        for o in search_response.objects:
            st.write(o.properties["title"][:20] + "...")
            st.caption("Chunk: " + str(int(o.properties["chunk_no"])))
            st.caption(o.properties["body"])
            st.divider()


st.markdown("### Response")
if len(search_query) > 0 and len(prompt) > 0 and srch_query is not None:
    rag_response = gen_query(
        query=search_query,
        grouped_task=prompt + llm.RAG_SUFFIX,
        limit=n_chunks_manual,
    )
    st.write(rag_response.generated)
