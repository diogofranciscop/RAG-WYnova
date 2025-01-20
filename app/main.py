from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.embeddings import *
from app.model_integration import generate_rag_answer

# Path to the PDF file
pdf_path = "data/fundamental-rights-european-union.pdf"

# Initialize FastAPI app
app = FastAPI()

# Startup Event for Preprocessing
@app.on_event("startup")
async def startup_event():
    try:
        sections = extract_and_split_pdf(pdf_path)
        store_embeddings_in_chroma(sections)
        print("Embeddings successfully stored.")
    except Exception as e:
        print(f"Error during startup: {e}")

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG API! Use the /ask endpoint to submit questions about the Fundamental Rights of the European Union."}

# Request and Response Models
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    relevant_snippets: List[str]

# POST /ask Endpoint
@app.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest):
    question = payload.question
    snippets = get_relevant_snippets(question)
    if not snippets:
        raise HTTPException(status_code=404, detail="No relevant snippets found.")

    try:
        answer = generate_rag_answer(question, snippets)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

    return AnswerResponse(answer=answer, relevant_snippets=snippets)
