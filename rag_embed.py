import os
from dotenv import load_dotenv


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def create_vectorstore_from_transcript(transcript: str, save_path: str = "faiss_index"):
    """Split transcript, embed with Gemini, and save vector store using FAISS."""
    
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(transcript)

    if not chunks:
        raise ValueError("Transcript could not be split into chunks.")

    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )

    
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

    
    vectorstore.save_local(save_path)
    print(f"✅ Vector DB saved to: {save_path}")
