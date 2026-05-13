# 📚 Interactive Textbook Q&A System (RAG-Based AI Application)

An enterprise-style Retrieval-Augmented Generation (RAG) application that allows students to ask questions from textbooks and receive grounded AI-generated answers with citations.

---

# 🚀 Project Overview

This project is an AI-powered educational assistant that enables users to interact with textbook PDFs using natural language queries.

The system:

* Loads textbook PDFs
* Splits textbook content into chunks
* Generates embeddings using HuggingFace models
* Stores embeddings in a FAISS vector database
* Retrieves relevant textbook content
* Uses Groq LLMs to generate grounded answers
* Displays citations including textbook name, chapter, and page number

The application supports:

✅ Multiple textbooks
✅ Citation-based answers
✅ Textbook filtering
✅ Hallucination prevention
✅ Streamlit UI
✅ Metadata-aware retrieval

---

# 🧠 RAG Architecture

```text
PDF Textbooks
       ↓
PyPDFLoader
       ↓
Text Chunking
       ↓
HuggingFace Embeddings
       ↓
FAISS Vector Database
       ↓
Retriever
       ↓
Groq LLM
       ↓
Grounded Answer + Citations
```

---

# ✨ Features

## 📖 PDF Textbook Ingestion

* Upload and process multiple textbook PDFs
* Supports searchable/text-based PDFs

## 🔍 Semantic Search

* Uses vector embeddings for semantic similarity retrieval
* Retrieves contextually relevant textbook sections

## 📚 Citation Support

Each answer includes:

* Textbook name
* Chapter information
* Page number

## 🧠 Grounded AI Responses

The LLM is restricted to answering only from retrieved textbook content.

## 🚫 Hallucination Prevention

If relevant information is not found:

```text
"The answer is not available in the uploaded textbooks."
```

## 🎯 Textbook Selection Feature

Students can:

* Search all textbooks
* Search a specific textbook only

## ⚡ Fast Inference

Uses Groq LLM API for ultra-fast responses.

## 💻 Streamlit UI

Simple and interactive frontend for querying textbooks.

---

# 🛠️ Tech Stack

| Component              | Technology                        |
| ---------------------- | --------------------------------- |
| Programming Language   | Python                            |
| Framework              | LangChain                         |
| Embeddings             | HuggingFace Sentence Transformers |
| Vector Database        | FAISS                             |
| LLM Provider           | Groq                              |
| UI                     | Streamlit                         |
| PDF Parsing            | PyPDF                             |
| Environment Management | python-dotenv                     |

---

# 📂 Project Structure

```text
textbook-qa/
│
├── textbooks/              # Store textbook PDFs
│
├── vector_db/              # FAISS vector database
│
├── venv/                   # Virtual environment
│
├── .env                    # API keys
│
├── requirements.txt        # Dependencies
│
├── config.py               # Configuration settings
│
├── main.py                 # Core RAG pipeline
│
├── app.py                  # Streamlit application
│
├── README.md               # Documentation
│
└── .gitignore              # Ignore unnecessary files
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/textbook-qa-rag.git
cd textbook-qa-rag
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from:

https://console.groq.com

---

# 📚 Add Textbooks

Place textbook PDFs inside:

```text
textbooks/
```

Example:

```text
textbooks/
├── Physics.pdf
├── NCERT-Class-10-Science.pdf
├── Biology.pdf
```

---

# ▶️ Run the Application

## Run CLI Version

```bash
python main.py
```

---

## Run Streamlit UI

```bash
streamlit run app.py
```

---

# 🧩 Core Components

# 1️⃣ PDF Loader

Uses:

```python
PyPDFLoader
```

to extract textbook text page-by-page.

---

# 2️⃣ Metadata Extraction

Each chunk stores metadata:

```python
{
    "textbook": textbook_name,
    "chapter": chapter_name,
    "page": page_number
}
```

Used for:

* citations
* textbook filtering
* grounded retrieval

---

# 3️⃣ Text Chunking

Uses:

```python
RecursiveCharacterTextSplitter
```

Configuration:

```python
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

---

# 4️⃣ Embeddings

Uses HuggingFace model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Advantages:

* lightweight
* fast
* free
* production-friendly

---

# 5️⃣ Vector Database

Uses:

```text
FAISS
```

for semantic similarity search.

Why FAISS?

✅ Fast retrieval
✅ Lightweight
✅ Easy local setup
✅ Enterprise-grade vector search

---

# 6️⃣ Retriever

Retrieves top-k relevant chunks:

```python
search_kwargs={"k": NUM_RETRIEVED_DOCS}
```

Supports:

* semantic retrieval
* metadata filtering

---

# 7️⃣ LLM Integration

Uses Groq API with:

```text
llama-3.1-8b-instant
```

Advantages:

* ultra-fast inference
* low latency
* high-quality answers

---

# 8️⃣ Hallucination Prevention

Custom prompt restricts model to textbook context only.

Example:

```text
If the answer is not available in the uploaded textbooks,
say that explicitly.
```

---

# 🎯 Textbook Selection Feature

Users can select:

```text
0. Search ALL textbooks
1. Physics
2. Biology
3. NCERT Science
```

Retrieval uses metadata filtering:

```python
filter={"textbook": textbook_name}
```

This improves:

* retrieval accuracy
* grounding
* response relevance

---

# 📸 Example Questions

```text
What is Newton's first law?
```

```text
Explain photosynthesis.
```

```text
Summarize Chapter 5.
```

```text
What is refraction of light?
```

---

# 📌 Example Output

```text
Newton’s First Law states that an object remains at rest
or in uniform motion unless acted upon by an external force.
```

### Citations

```text
Physics - Chapter 1, Page 14
```

---

# 🚫 Out-of-Scope Question Example

Question:

```text
What happened in World War II?
```

Response:

```text
The answer is not available in the uploaded textbooks.
```

---

# 🔥 Enterprise-Level Concepts Implemented

This project demonstrates:

✅ Retrieval-Augmented Generation (RAG)
✅ Vector Databases
✅ Semantic Search
✅ Metadata Filtering
✅ Grounded Generation
✅ Hallucination Prevention
✅ Multi-Document Retrieval
✅ Citation-Based QA
✅ LLM Orchestration
✅ Streamlit Deployment

---

# 📈 Future Enhancements

## Planned Improvements

* Multi-modal support (images/diagrams)
* OCR support for scanned PDFs
* Hybrid search (BM25 + Vector Search)
* Reranking
* Conversational memory
* Multi-user authentication
* Cloud deployment
* Docker support
* API endpoints
* Chapter-level filtering

---

# ☁️ Deployment Options

Possible deployment platforms:

* Streamlit Cloud
* AWS EC2
* Azure App Service
* HuggingFace Spaces
* Docker Containers
* Kubernetes

---

# 🧪 Sample Workflow

```text
User asks question
        ↓
Retriever searches FAISS vectors
        ↓
Relevant textbook chunks retrieved
        ↓
Groq LLM receives:
   Question + Context
        ↓
Grounded answer generated
        ↓
Citations displayed
```

---

# 📦 Requirements

Example dependencies:

```txt
langchain==0.2.16
langchain-community==0.2.16
langchain-core==0.2.38
langchain-groq==0.1.9

groq==0.9.0

faiss-cpu==1.13.0

sentence-transformers==2.7.0
transformers==4.57.6
huggingface_hub==0.36.2

pypdf==5.5.0

streamlit==1.31.0
python-dotenv==1.0.1
tiktoken==0.7.0
httpx==0.27.0
```

---

# 👨‍💻 Author

## Venkatareddy

AI/ML Engineer | RAG Developer | Generative AI Learner

---

# 📄 License

This project is for educational and portfolio purposes.

---

# ⭐ Acknowledgements

* LangChain
* HuggingFace
* Groq
* FAISS
* Streamlit

---

# 🎓 Learning Outcomes

This project helps understand:

* RAG pipelines
* embeddings
* vector databases
* semantic retrieval
* metadata filtering
* prompt engineering
* hallucination prevention
* enterprise GenAI architecture

---

# 🚀 Final Note

This project demonstrates a complete end-to-end enterprise-style RAG workflow suitable for:

* AI Engineer portfolios
* GenAI learning
* Educational AI systems
* Retrieval systems
* Enterprise document assistants
