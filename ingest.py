from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

def load_docs(data_dir="data/raw"):
    docs = []
    for fname in os.listdir(data_dir):
        if fname.endswith(".txt") or fname.endswith(".md"):
            path = os.path.join(data_dir, fname)
            loader = TextLoader(path)
            docs.extend(loader.load())
    return docs

def build_vectorstore():
    raw_docs = load_docs()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(raw_docs)
    db = FAISS.from_documents(chunks, OpenAIEmbeddings())
    db.save_local("tds_faiss_db")
    print("Vectorstore built and saved.")

if __name__ == "__main__":
    build_vectorstore()
