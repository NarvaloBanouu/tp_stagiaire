#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import creer_agent
import uvicorn

load_dotenv()

app = FastAPI(
    title="Agent Financier API",
    description="API REST pour interroger un agent LangChain",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    success: bool

agent_executor = None

@app.on_event("startup")
def startup_event():
    global agent_executor
    agent_executor = creer_agent()

@app.get("/")
def root():
    return {
        "message": "API Agent Financier",
        "endpoints": {
            "POST /api/agent/query": "Interroger l'agent avec une question",
            "GET /health": "Vérifier l'état de l'API"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "agent_ready": agent_executor is not None}

@app.post("/api/agent/query", response_model=QueryResponse)
def query_agent(request: QueryRequest):
    if not agent_executor:
        raise HTTPException(status_code=503, detail="Agent non initialisé")

    try:
        result = agent_executor.invoke(
            {"input": request.question},
            config={"configurable": {"session_id": "api-session"}}
        )
        return QueryResponse(
            question=request.question,
            answer=result['output'],
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement : {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
