from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    message: str

@app.post("/mirror")
def mirror_message(request: MessageRequest) -> MessageResponse:
    return MessageResponse(message=request.message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
