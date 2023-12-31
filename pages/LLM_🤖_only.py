import llm
import streamlit as st
from helper import preset_prompts


openai_client = llm.init_openai()

st.set_page_config(
    page_title="LLMs by themselves",
    page_icon="🤖",
)

st.title("LLMs 🤖: Flying solo")


selected_prompt = st.selectbox(label="Select a prompt", options=preset_prompts)

if selected_prompt == "Custom":
    prompt = st.text_area(label="Ask the LLM anything.", value="", height=50)
elif selected_prompt == "Select a prompt":
    prompt = ""
else:
    prompt = selected_prompt

full_prompt = prompt + llm.PROMPT_TEMPLATE

st.subheader("LLM only (dumb genius)")
st.write("This simply asks the LLM for an answer to our question.")

st.markdown("### Response")
if len(prompt) > 0:
    raw_response = llm.get_llm_response(full_prompt)
    st.write(raw_response)
