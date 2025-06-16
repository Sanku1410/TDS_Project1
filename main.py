from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from app.config import OPENAI_API_KEY
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

app = FastAPI()

vectorstore = FAISS.load_local("tds_faiss_db", OpenAIEmbeddings())
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
    retriever=vectorstore.as_retriever()
)

class Question(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "TDS Q&A API is running!"}

@app.post("/ask")
def ask(q: Question):
    answer = qa.run(q.query)
    return {"answer": answer}
