# LLM vs RAG

## Introduction

This demo shows benefits of using retrieval augmented generation over vanilla LLM usage.

## Usage

### Basic example

1. Install `requirements.txt` (`pip install -r requirements.txt`).
1. Run an instance of Weaviate (e.g. `docker-compose up -d` from your shell). 
1. Run `eg1_create_collection.py` to create a collection.
1. Run `eg2_import_arxiv.py` and `eg2_import_pdf.py` to import text data from various PDFs.
1. Run `streamlit run Demo_app.py` from your shell.

There is also a multi-modal example - documentation to come :).

## Build amazing GenAI apps with Weaviate

- Start with the [Quickstart guide](https://weaviate.io/developers/weaviate/quickstart)
- The [RAG guide](https://weaviate.io/developers/weaviate/starter-guides/generative) is a good next step 
- The [Academy](https://weaviate.io/developers/academy) is a holistic guide combining theory & practice
- The [Recipes](https://github.com/weaviate/recipes) show you practical end-to-end examples
