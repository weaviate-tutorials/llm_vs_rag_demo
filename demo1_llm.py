import llm
import streamlit as st


openai_client = llm.init_openai()

st.set_page_config(layout="wide")
st.title("Why LLMs are such dumb geniuses")
st.subheader("(And how better search can help)")

prompt = st.text_input(label="Ask the LLM anything.", value="")
prompt += llm.PROMPT_TEMPLATE

st.subheader("LLM only (dumb genius)")
st.write("This simply asks the LLM for an answer to our question.")

st.markdown("### Response")
if len(prompt) > 0:
    raw_response = llm.get_llm_response(prompt)
    st.write(raw_response)
