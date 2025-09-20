from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

import os
import asyncio
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

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

# ---------- Function tools ----------
@function_tool
def get_weather(city: str):
    """Get weather information for a city."""
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny with 22°C."

@function_tool
def calculate(expression: str):
    """Calculate a mathematical expression safely."""
    try:
        # Simple safe evaluation for basic math
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Cannot calculate {expression}: {str(e)}"

# ---------- Main agent function ----------
async def main(model: str, api_key: str, user_message: str):
    """Main function that creates and runs the agent following OpenAI Agents documentation pattern."""
    agent = Agent(
        name="Gemini Assistant",
        instructions="You are a helpful and concise assistant. You can help with weather information and calculations.",
        model=LitellmModel(model=model, api_key=api_key),
        tools=[get_weather, calculate],
    )

    result = await Runner.run(agent, user_message)
    return result.final_output

# ---------- FastAPI route ----------
@app.post("/")
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Async chat endpoint that uses asyncio.run pattern from OpenAI Agents documentation."""
    if not request.messages:
        return ChatResponse(text="No messages received")
    
    try:
        # Get API key and model from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return ChatResponse(text="Error: GEMINI_API_KEY environment variable not set")
        
        model = "gemini/gemini-2.0-flash"  # Using Gemini Pro as specified in LiteLLM docs
        
        # Get the last user message
        last_msg = request.messages[-1].content if request.messages else "No input"
        
        # Run the main function following the OpenAI Agents documentation pattern
        response_text = await main(model, api_key, last_msg)
        
        return ChatResponse(text=response_text)
        
    except Exception as e:
        return ChatResponse(text=f"Error getting response: {str(e)}")

# ---------- Run ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
