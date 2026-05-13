import os

from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from langchain_groq import ChatGroq

from config import *

def load_textbook_with_metadata(file_path, textbook_name):
    """
    Load textbook and add metadata (chapter, page, textbook name).
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Add metadata to each document
    for doc in documents:
        doc.metadata['textbook'] = textbook_name
        doc.metadata['page'] = doc.metadata.get('page', 0)
        # Try to extract chapter from page content (basic approach)
        # You can enhance this with more sophisticated chapter detection
        doc.metadata['chapter'] = extract_chapter_info(doc.page_content)
    
    return documents

def extract_chapter_info(content):
    """
    Simple chapter extraction - looks for chapter patterns in text.
    Enhance this based on your textbook format.
    """
    content_lower = content[:500].lower()  # Check first 500 chars
    if 'chapter' in content_lower:
        # Try to find chapter number
        import re
        match = re.search(r'chapter\s+(\d+)', content_lower)
        if match:
            return f"Chapter {match.group(1)}"
    return "Unknown Chapter"

def load_all_textbooks(directory):
    """Load all textbooks from directory."""
    all_documents = []
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist!")
        return all_documents
    
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in '{directory}'")
        return all_documents
    
    print(f"Found {len(pdf_files)} textbook(s)")
    
    for filename in pdf_files:
        file_path = os.path.join(directory, filename)
        textbook_name = os.path.splitext(filename)[0]
        print(f"Loading: {textbook_name}")
        
        try:
            docs = load_textbook_with_metadata(file_path, textbook_name)
            all_documents.extend(docs)
            print(f"  ✓ Loaded {len(docs)} pages")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    print(f"\nTotal pages loaded: {len(all_documents)}")
    return all_documents

def split_documents_with_metadata(documents):
    """Split documents while preserving metadata."""
    print("\nSplitting documents into chunks...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Preserve metadata in chunks
    for chunk in chunks:
        if 'textbook' not in chunk.metadata:
            chunk.metadata['textbook'] = 'Unknown'
        if 'page' not in chunk.metadata:
            chunk.metadata['page'] = 0
        if 'chapter' not in chunk.metadata:
            chunk.metadata['chapter'] = 'Unknown Chapter'
    
    print(f"Created {len(chunks)} chunks")
    return chunks

def create_vector_store(chunks):

    print("\nCreating vector database...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(VECTOR_DB_DIR)

    print("✓ Vector database created")

    return vectorstore

def load_vector_store():

    if os.path.exists(VECTOR_DB_DIR):

        print("Loading existing vector database...")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorstore = FAISS.load_local(
            VECTOR_DB_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )

        print("✓ Database loaded")

        return vectorstore

    return None

def create_qa_chain(vectorstore, textbook_name=None):
    """Create Q&A chain with optional textbook filtering."""

    print("\nSetting up Q&A chain...")

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME
    )

    template = """
You are an educational textbook assistant.

Answer the question ONLY using the provided textbook context.

STRICT RULES:
1. Do NOT use outside knowledge.
2. Do NOT make up answers.
3. If the answer is not clearly available in the textbook context, say:
   'The answer is not available in the uploaded textbooks.'
4. Be concise and educational.
5. Include citations when information is available.

Context:
{context}

Question:
{question}

Answer:
"""

    PROMPT = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    # ✅ Metadata filtering
    if textbook_name:
        retriever = vectorstore.as_retriever(
            search_kwargs={
                "k": NUM_RETRIEVED_DOCS,
                "filter": {"textbook": textbook_name}
            }
        )
    else:
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": NUM_RETRIEVED_DOCS}
        )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    print("✓ Q&A chain ready")

    return qa_chain

def ask_question(qa_chain, question):
    """Ask question and get answer with citations."""
    print(f"\nQuestion: {question}")
    print("Searching textbook...")
    
    try:
        result = qa_chain({"query": question})
        answer = result["result"]
        sources = result.get("source_documents", [])
        
        # Format citations
        citations = []
        seen = set()
        for source in sources:
            textbook = source.metadata.get('textbook', 'Unknown')
            page = source.metadata.get('page', 'N/A')
            chapter = source.metadata.get('chapter', 'Unknown')
            
            citation_key = f"{textbook}_page_{page}"
            if citation_key not in seen:
                citations.append({
                    'textbook': textbook,
                    'chapter': chapter,
                    'page': page
                })
                seen.add(citation_key)
        
        return {
            "answer": answer,
            "sources": sources,
            "citations": citations
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "sources": [],
            "citations": []
        }
def get_available_textbooks():
    """Get available textbook names."""

    if not os.path.exists(TEXTBOOKS_DIR):
        return []

    pdf_files = [
        f for f in os.listdir(TEXTBOOKS_DIR)
        if f.endswith('.pdf')
    ]

    textbook_names = [
        os.path.splitext(f)[0]
        for f in pdf_files
    ]

    return textbook_names
def main():
    """Main function."""
    print("=" * 60)
    print("📚 Interactive Textbook Q&A System")
    print("=" * 60)
    
    vectorstore = load_vector_store()
    
    if vectorstore is None:
        print("\nCreating new database...")
        documents = load_all_textbooks(TEXTBOOKS_DIR)
        
        if not documents:
            print("No textbooks found! Add PDF files to 'textbooks' folder.")
            return
        
        chunks = split_documents_with_metadata(documents)
        vectorstore = create_vector_store(chunks)
    
    available_textbooks = get_available_textbooks()

    print("\nAvailable Textbooks:")
    print("0. Search ALL textbooks")

    for i, book in enumerate(available_textbooks, 1):
        print(f"{i}. {book}")

    choice = input("\nSelect textbook number: ").strip()

    selected_textbook = None

    if choice != "0":
        try:
            selected_textbook = available_textbooks[int(choice) - 1]
            print(f"\nSelected textbook: {selected_textbook}")
        except:
            print("Invalid choice. Using all textbooks.")

    qa_chain = create_qa_chain(
        vectorstore,
        selected_textbook
)
    
    print("\n" + "=" * 60)
    print("System ready! Ask questions about your textbooks")
    print("Type 'quit' to exit")
    print("=" * 60)
    
    while True:
        question = input("\n👤 Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
        
        if not question:
            continue
        
        result = ask_question(qa_chain, question)
        
        print("\n" + "-" * 60)
        print("📖 Answer:")
        print("-" * 60)
        print(result["answer"])
        
        if result["citations"]:
            print("\n" + "-" * 60)
            print("📚 Citations:")
            print("-" * 60)
            for i, citation in enumerate(result["citations"], 1):
                print(f"{i}. {citation['textbook']} - {citation['chapter']}, Page {citation['page']}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()