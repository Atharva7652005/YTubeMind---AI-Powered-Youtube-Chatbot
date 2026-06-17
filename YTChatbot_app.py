import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from os import getenv

import streamlit.components.v1 as components
import json

load_dotenv()

st.set_page_config(page_title="YTube Mind", layout="wide")

# ---------------------------
# Helpers
# ---------------------------

def get_video_id(url):
    parsed = urlparse(url)

    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]
        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]

    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")

    return None


def translate_transcript(text):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=getenv("GEMINI_API_KEY"),
        temperature=0
    )
    response = llm.invoke(
        f"""Translate the following transcript into fluent English.
            Return only the translation.

            {text}"""
    )
    return response.content


def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)

# ---------------------------
# Session State
# ---------------------------

if "chain" not in st.session_state:
    st.session_state.chain = None

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "english_transcript" not in st.session_state:
    st.session_state.english_transcript = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# Header
# ---------------------------

st.title("YouTube Video Chatbot")
youtube_url = st.text_input("Paste YouTube URL")

# ---------------------------
# Process Video
# ---------------------------

if st.button("Process Video"):

    if not youtube_url.strip():
        st.error("Please enter a YouTube URL first.")
        st.stop()

    with st.spinner("Fetching Transcript..."):
        try:
            # Validate Youtube URL and its ID
            video_id = get_video_id(youtube_url)
            if not video_id:
                st.error("Invalid YouTube URL. Please check and try again.")
                st.stop()

            ytranscript = YouTubeTranscriptApi()

            transcript_list = ytranscript.fetch(video_id, languages=["hi", "en"])

            transcript = " ".join(chunk.text for chunk in transcript_list)

            st.session_state.transcript = transcript

            # Clear chat history for new video
            st.session_state.messages = []

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.create_documents([transcript])

            embeddings = GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-001",
                google_api_key=getenv("GEMINI_API_KEY")
            )

            vector_store = FAISS.from_documents(
                documents=chunks,
                embedding=embeddings
            )

            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )

            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=getenv("GEMINI_API_KEY"),
                temperature=0.1
            )

            prompt = PromptTemplate(
                template="""You are a helpful assistant.
                Answer ONLY from the provided transcript.
                If the answer is not present, say "I don't know."

                Context:
                {context}

                Question:
                {question}
                """,
                input_variables=["context", "question"]
            )

            parallel_chain = RunnableParallel(
                {
                    "context": retriever | RunnableLambda(format_docs),
                    "question": RunnablePassthrough()
                }
            )

            parser = StrOutputParser()
            final_chain = parallel_chain | prompt | llm | parser

            st.session_state.chain = final_chain

            with st.spinner("Generating English Translation..."):
                # Cut at word boundary to avoid mid-word truncation
                safe_text = transcript[:15000].rsplit(" ", 1)[0]
                st.session_state.english_transcript = translate_transcript(safe_text)

            st.success("Video Processed!")

        # Catch TranscriptsDisabled explicitly
        except TranscriptsDisabled:
            st.error("Transcripts are disabled for this video.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ---------------------------
# Main Layout
# ---------------------------

if st.session_state.chain:

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Chat with Video")

        messages_json = json.dumps(st.session_state.messages)

        chat_component = f"""
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ background: #000; }}

            .chat-wrapper {{
                width: 100%;
                height: 480px;
                background: #000;
                border: 1px solid #333;
                border-radius: 12px;
                overflow-y: auto;
                padding: 16px;
                display: flex;
                flex-direction: column;
                gap: 10px;
                scrollbar-width: thin;
                scrollbar-color: #333 #000;
                font-family: sans-serif;
            }}
            .chat-wrapper::-webkit-scrollbar {{ width: 5px; }}
            .chat-wrapper::-webkit-scrollbar-track {{ background: #000; }}
            .chat-wrapper::-webkit-scrollbar-thumb {{ background: #444; border-radius: 4px; }}

            .msg-row {{ display: flex; flex-direction: column; max-width: 78%; }}
            .msg-row.user {{ align-self: flex-start; }}
            .msg-row.assistant {{ align-self: flex-end; }}

            .msg-label {{ font-size: 11px; color: #555; margin-bottom: 4px; }}
            .msg-row.assistant .msg-label {{ text-align: right; }}

            .msg-bubble {{
                padding: 10px 14px;
                font-size: 13px;
                line-height: 1.6;
                word-wrap: break-word;
                white-space: pre-wrap;
            }}
            .msg-row.user .msg-bubble {{
                background: #d4a800;
                color: #000;
                border-radius: 16px 16px 16px 4px;
            }}
            .msg-row.assistant .msg-bubble {{
                background: #1a1a1a;
                color: #e0e0e0;
                border: 1px solid #2a2a2a;
                border-radius: 16px 16px 4px 16px;
            }}
        </style>

        <div class="chat-wrapper" id="box">
        </div>

        <script>
            const messages = {messages_json};
            const box = document.getElementById("box");
            messages.forEach(msg => {{
                const row = document.createElement("div");
                row.className = "msg-row " + msg.role;
                const label = document.createElement("div");
                label.className = "msg-label";
                label.textContent = msg.role === "user" ? "You" : "Assistant";
                const bubble = document.createElement("div");
                bubble.className = "msg-bubble";
                bubble.textContent = msg.content;
                row.appendChild(label);
                row.appendChild(bubble);
                box.appendChild(row);
            }});
            box.scrollTop = box.scrollHeight;
        </script>
        """

        components.html(chat_component, height=500)

        # Native Streamlit input sits below the black chat box
        question = st.chat_input("Ask a question about the video...")

        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner("Thinking..."):
                answer = st.session_state.chain.invoke(question)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
            
    with col2:
        st.subheader("Transcript")

        language = st.radio(
            "Choose Language",
            ["Original", "English"],
            horizontal=True
        )

        if language == "Original":
            st.text_area("Original Transcript", st.session_state.transcript, height=700, label_visibility="collapsed")
        else:
            st.text_area("English Transcript", st.session_state.english_transcript, height=700, label_visibility="collapsed")