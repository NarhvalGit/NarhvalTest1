import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "gpt-4.1-mini"


client = OpenAI()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def ensure_api_key_present() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable is not set.")


@app.post("/api/chat")
async def create_chat_completion(request: ChatRequest):
    ensure_api_key_present()

    try:
        response = client.responses.create(
            model=request.model,
            input=[message.dict() for message in request.messages],
        )
    except Exception as exc:  # pragma: no cover - surface provider errors
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {"reply": response.output_text}


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
