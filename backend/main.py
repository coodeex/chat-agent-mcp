from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from agents import Runner, set_tracing_disabled
from config import config
from services.manager import create_agent

# ---------- FastAPI setup ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Schemas ----------
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    text: str

# ---------- Main agent function ----------
async def run_agent(user_message: str):
    """Run the agent with the given user message."""
    set_tracing_disabled(True)  # disable tracing for litellm, can be enabled if openai api key is available
    agent = create_agent()
    result = await Runner.run(agent, user_message)
    return result.final_output

# ---------- FastAPI route ----------
@app.post("/")
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Async chat endpoint that uses the configuration-based agent setup."""
    if not request.messages:
        return ChatResponse(text="No messages received")
    
    try:
        # Check if API key is configured
        if not config.validate_api_key():
            return ChatResponse(text="Error: GEMINI_API_KEY environment variable not set")
        
        # Get the last user message
        last_msg = request.messages[-1].content if request.messages else "No input"
        
        # Run the agent
        response_text = await run_agent(last_msg)
        
        return ChatResponse(text=response_text)
        
    except Exception as e:
        return ChatResponse(text=f"Error getting response: {str(e)}")

# ---------- Run ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
