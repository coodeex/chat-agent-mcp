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


def _format_conversation(messages: List[Message]) -> str:
    """Convert a list of chat messages into a readable conversation transcript."""
    formatted = []
    for message in messages:
        role = {
            "user": "User",
            "assistant": "Assistant",
            "system": "System",
        }.get(message.role, message.role.capitalize())
        content = message.content.strip()
        formatted.append(f"{role}: {content}")
    return "\n".join(formatted)


def _get_last_user_message(messages: List[Message]) -> str:
    """Return the last user-authored message if available."""
    for message in reversed(messages):
        if message.role == "user":
            return message.content.strip()
    return ""


# ---------- Main agent function ----------
async def run_agent(conversation: str):
    """Run the agent with the conversation context."""
    set_tracing_disabled(True)  # disable tracing for litellm, can be enabled if openai api key is available
    agent = create_agent()
    result = await Runner.run(agent, conversation)
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
        
        conversation_transcript = _format_conversation(request.messages)
        latest_user_message = _get_last_user_message(request.messages)

        if latest_user_message:
            prompt = (
                "Use the history when needed to reference prior context. Otherwise, focus on the latest user message. Conversation history:\n\n"
                f"{conversation_transcript}\n\n"
                f"Latest user message: {latest_user_message}\n"
            )
        else:
            # Fallback if we cannot detect a user message in the history.
            prompt = conversation_transcript or "No input"

        # Run the agent
        response_text = await run_agent(prompt)
        
        return ChatResponse(text=response_text)
        
    except Exception as e:
        return ChatResponse(text=f"Error getting response: {str(e)}")

# ---------- Run ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
