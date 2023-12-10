import weaviate
import weaviate.classes as wvc
import os
import logging
import loggerconfig
import streamlit as st
import llm


N_CHUNKS = 10
PROMPT_TEMPLATE = " Keep the answer relatively short, such as within a few paragraphs or within 5-6 main bullet points."

client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY"),
        "X-Cohere-Api-Key": os.getenv("COHERE_APIKEY"),
    }
)
chunks = client.collections.get("Chunk")

st.set_page_config(layout="wide")
st.title("Why LLMs are such dumb geniuses")
st.subheader("(And how better search can help)")

prompt = st.text_input(label="Ask the LLM anything.", value="")
prompt += PROMPT_TEMPLATE
raw_response = llm.get_llm_response(prompt)

top_col1, top_col2 = st.columns(2)
with top_col1:
    st.subheader("LLM only (dumb genius)")
    st.write("This simply asks the LLM for an answer to our question.")
with top_col2:
    st.subheader("With help from Weaviate")
    st.write("This will use Weaviate to help the LLM answer the question.")
    search_query = st.text_input(label="Search our database to help the LLM", value="")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Response")
    if len(prompt) > 0:
        st.write(raw_response)

with col2:
    st.markdown("### Response")
    if len(search_query) > 0 and len(prompt) > 0:
        weaviate_response = chunks.generate.near_text(
            query=search_query,
            grouped_task=prompt,
            limit=N_CHUNKS,
        )
        st.write(weaviate_response.generated)
        st.markdown("#### Under the hood")
        with st.expander("Query used:"):
            st.code("""
                chunks = client.collections.get("Chunk")
                response = chunks.generate.near_text(
                    query=query,
                    grouped_task=grouped_task,
                    limit=n_chunks,
                )            
            """)
        with st.expander("Chunks used:"):
            for o in weaviate_response.objects:
                st.write(o.properties["title"] + " chunk no: " + str(o.properties["chunk_no"]))
                st.caption(o.properties["body"])
                st.divider()
