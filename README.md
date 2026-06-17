# Gen AI 

## Overview

This repository collects practical LangChain and retrieval-augmented generation (RAG) experiments in Python and JavaScript. It includes document loaders, prompt design, chain composition, vector stores, structured output, and a focused YouTube chatbot project.

## Main Topics and Folder Summaries

### Langchain Core Examples

- `Langchain_Chains/`
  - Examples of chain compositions using LangChain.
  - `simple_chain.py`: basic prompt → model → parser pipeline.
  - `sequential_chain.py`: sequential execution of multiple prompts.
  - `parallel_chain.py`: split work into parallel outputs.
  - `conditional_chain.py`: conditional branching based on model output.

- `Langchain_Runnables/`
  - Demonstrates runnable abstractions for advanced chain control.
  - `runnable_parallel.py`, `runnable_sequence.py`, `runnable_branch.py`, `runnable_lambda.py`, `runnable_passthrough.py`.
  - These examples show how to compose and route tasks inside LangChain.

- `Langchain_Models/`
  - Model examples and quick demos for LLMs, chat models, and embedding models.
  - Includes notebooks and scripts showing usage of OpenAI, Anthropic, Google, and Hugging Face model interfaces.

### Document Loading and Text Processing

- `Document_Loaders_Langchain/`
  - Document ingestion examples for multiple sources.
  - `pdf_loader.py`, `text_loader.py`, `csv_loader.py`, `directory_loader.py`, `web_base_loader.py`.
  - Contains sample docs and notebooks for loading content into LangChain workflows.

- `Text_Splitters_Langchain/`
  - Various text splitting strategies for preparing long documents.
  - `length_based.py`, `markdown_splitting.py`, `python_code_splitting.py`, `semantic_embedding_splitting.py`, `text_structure_based.py`.
  - These scripts show how to chunk text for embeddings and retrieval.

- `Vector_Stores/`
  - Vector store usage examples and notebook experiments.
  - `Vector_Stores_in_Langchain_ChromaDB.ipynb`, `Vector_Stores_in_Langchain_FIASS_DB.ipynb`.

### Retrieval and RAG

- `Langchain_Retrievers/`
  - Retriever-related experiments and retrieval patterns for LangChain.

- `RAG/` and `RAG_2/`
  - Retrieval-Augmented Generation demos using JavaScript.
  - Includes `index.js`, `query.js`, `package.json`, and Pinecone integration examples.
  - `RAG_2/` is a second version with a similar retrieval workflow and environment setup.

### Prompting and Structured Output

- `Langchain_Prompts/`
  - Prompt templates and prompt UI examples.
  - `chat_prompt_template.py`, `chatbot.py`, `messages.py`, `message_placeholder.py`, `prompts_ui.py`, `template.json`.
  - Useful for building chat-style prompts and custom prompt layouts.

- `Langchain_Outparser/`
  - Parsers for extracting and structuring model responses.
  - `json_output_parser.py`, `pydantic_output_parser.py`, `stroutput_parser.py`, `stroutparser2.py`.
  - Demonstrates how to enforce output shape and parse responses.

- `Langchain_Structured_Output/`
  - Structured output examples using JSON schema and typed parsing.
  - `json_schema.json`, `structured_output_json_schema.py`, `structured_output_pydantic.py`, `structured_output_typedict.py`.

### Chatbot and Application Demos

- `Chatbot/`
  - Chat application examples likely built with Python.
  - `app.py`, `main.py` show chat framework patterns and how to connect UI with LLM logic.

- `README.md` (this file)
  - A consolidated summary of repository topics and usage.

### Notebooks and Learning Examples

- Root notebooks:
  - `(Demo)Langchain_using_Runnable.ipynb`
  - `(Demo)Langchain_without_Runnable.ipynb`

- Feature-specific notebooks in subfolders for interactive experiments.

## YouTube Chatbot Project

This repository includes a dedicated YouTube video chatbot feature with two main files:

### `Youtube_Chatbot_model.py`

This script builds a standalone YouTube chatbot pipeline:

- Extracts the YouTube video ID from a URL.
- Downloads transcript text using `youtube_transcript_api`.
- Splits the transcript into chunks using `RecursiveCharacterTextSplitter`.
- Converts chunks into embeddings with Google Gemini embeddings.
- Stores embeddings in a FAISS vector store.
- Uses LangChain retrieval to find the most relevant transcript chunks.
- Sends retrieved context into a Google Gemini chat model for answer generation.
- Includes a sample prompt that restricts answers to transcript content.

This file is ideal for experimentation and for quickly verifying that transcript retrieval and generation work together.

### `YTChatbot_app.py`

This file builds a Streamlit web app named `YouTube Video Chatbot` with:

- A URL input field for pasting YouTube links.
- Transcript fetching and language fallback for Hindi/English.
- Chunking and embedding of the transcript.
- FAISS-based similarity retrieval for user questions.
- A Google Gemini chat model for answering user queries from the video.
- An English translation helper for transcript content.
- A live chat UI rendered through HTML components.
- Transcript display in original or translated English form.

This app is the best user-facing version of the project, combining retrieval, generative response, and UI.

## Getting Started

1. Create a Python virtual environment and activate it.
2. Install packages from the relevant requirements file or your own environment.
3. Add API keys to `.env`:
   - `GEMINI_API_KEY`
   - `GROQ_API_KEY` (if using Groq examples)
   - other provider keys as needed.
4. Run the Streamlit app:
   ```bash
   streamlit run YTChatbot_app.py
   ```
5. Paste a YouTube URL and ask questions about the video.

## Notes

- This repository is a learning and experimentation workspace for generative AI workflows.
- Many examples rely on external APIs and private keys stored in `.env`.
- Use the notebooks and scripts to explore different LangChain components and prompt styles.

---

## Folder Quick Reference

- `Chatbot/` — Chat application demos
- `Document_Loaders_Langchain/` — Loaders for PDF, CSV, text, directory, and web content
- `Langchain_Chains/` — Chain composition examples
- `Langchain_Models/` — Model examples and notebook demos
- `Langchain_Outparser/` — Output parsing and structured response handling
- `Langchain_Prompts/` — Prompt templates and chat prompt building
- `Langchain_Retrievers/` — Retriever examples
- `Langchain_Runnables/` — Runnable and branching LangChain patterns
- `Langchain_Structured_Output/` — JSON schema + Pydantic output examples
- `RAG/`, `RAG_2/` — JavaScript retrieval-augmented generation demos
- `Text_Splitters_Langchain/` — Text splitting strategies
- `Vector_Stores/` — Vector store experiments

If you want, I can also split this README into a separate `YOUTUBE_CHATBOT_README.md` for the chatbot project alone.