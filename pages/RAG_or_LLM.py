import logging
import loggerconfig
import streamlit as st
import llm
from helper import preset_prompts, get_client, COLL_NAME


N_CHUNKS = 5

client = get_client()

chunks = client.collections.get(COLL_NAME)

st.set_page_config(
    page_title="RAG: LLMs + Weaviate",
    page_icon="🤖",
)

st.title("LLM vs RAG!")
agg_resp = chunks.aggregate.over_all(total_count=True)
obj_count = agg_resp.total_count

selected_prompt = st.selectbox(label="Select a prompt", options=preset_prompts)

if selected_prompt == "Custom":
    prompt = st.text_area(label="Ask the LLM anything.", value="", height=50)
elif selected_prompt == "Select a prompt":
    prompt = ""
else:
    prompt = selected_prompt


full_prompt = prompt + llm.PROMPT_TEMPLATE

top_col1, top_col2 = st.columns(2, gap="medium")
with top_col1:
    st.subheader("LLM only")
    st.write("This simply asks the LLM for an answer to our question.")
with top_col2:
    st.subheader("RAG")
    st.write(f"This will prompt the LLM with retrieved data from Weaviate.")
    if len(prompt) > 0:
        search_response = chunks.query.near_text(
            query=prompt,
            limit=N_CHUNKS,
        )
        st.markdown("#### Sources:")

        with st.expander("Chunks used:"):
            for o in search_response.objects:
                st.write(o.properties["title"][:20] + "...")
                st.caption("Chunk: " + str(int(o.properties["chunk_no"])))
                st.caption(o.properties["body"])


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
