# YTubeMind

YTubeMind is a YouTube chatbot that transforms YouTube videos into interactive knowledge sources. Users can provide a YouTube video URL, view its transcript, access English translations for multilingual videos, and ask natural language questions about the video content. The application leverages Retrieval-Augmented Generation (RAG) to deliver accurate, context-aware responses grounded in the video's transcript.

---

## Features

* Extract transcripts directly from YouTube videos.
* Support for multilingual transcripts with English translation.
* Chat with any YouTube video using natural language queries.
* Semantic search powered by vector embeddings and FAISS.
* Context-aware question answering using Gemini 2.5 Flash.
* Interactive transcript viewer with language toggle support.
* Streamlit-based responsive web interface.
* Retrieval-Augmented Generation (RAG) architecture to reduce hallucinations.

---

## System Architecture

```text
YouTube URL
     │
     ▼
Transcript Extraction
     │
     ▼
Text Chunking
     │
     ▼
Gemini Embeddings
     │
     ▼
FAISS Vector Store
     │
     ▼
Retriever
     │
     ▼
Gemini 2.5 Flash
     │
     ▼
Chat Response
```

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & NLP

* Google Gemini 2.5 Flash
* Gemini Embeddings
* LangChain

### Vector Database

* FAISS

### Data Processing

* YouTube Transcript API
* Recursive Character Text Splitter

### Environment Management

* Python Dotenv

---

## Project Structure

```text
YTubeMind/
│
├── app.py
├── .env
├── requirements.txt
├── assets/
│
├── utils/
│   ├── transcript.py
│   ├── translation.py
│   ├── vector_store.py
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/YTubeMind.git
cd YTubeMind
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Get your Gemini API key from Google AI Studio.

---

## Run Application

```bash
streamlit run app.py
```

---

## How to Use

1. Launch the application.
2. Paste a YouTube video URL.
3. Click **Process Video**.
4. Wait for transcript extraction and indexing.
5. View the transcript in the original or English language.
6. Ask questions in the chat section.
7. Receive AI-generated answers grounded in the video content.


## Key Capabilities

* Semantic retrieval over transcript chunks using vector search.
* Transcript-grounded responses.
* Multilingual video understanding.
* Context-aware conversational search.
* Real-time AI-powered question answering.
