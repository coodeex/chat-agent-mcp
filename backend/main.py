from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    text: str

@app.post("/")
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    # Get the last message from the user
    if request.messages:
        last_message = request.messages[-1]
        # Echo back the user's message with a simple response
        response_text = f"You said: {last_message.content}"
    else:
        response_text = "No messages received"
    
    return {"text": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
