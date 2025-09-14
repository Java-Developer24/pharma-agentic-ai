
# main.py
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyBQ3KBPoDia7wJacppgwEHn027TwKYZD8k"

import os
from fastapi.responses import StreamingResponse
import asyncio
from fastapi import FastAPI, Depends
from agents.coordinator import coordinator_agent
from schemas import AgentResponse, QueryRequest

from database import SessionLocal, ChatHistory



app = FastAPI(title="Pharma Agentic AI Assistant")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to the Pharma Agentic AI Assistant"}
@app.post("/query-stream")
async def query_ai_stream(request: QueryRequest, db=Depends(get_db)):
    result = await coordinator_agent(request.user_query)

    text = getattr(result, "output", None) or getattr(result, "response", "")
    steps = getattr(result, "steps_taken", None) or getattr(result, "steps", [])
    visuals = getattr(result, "visuals", [])
    if not isinstance(visuals, list):
        visuals = [visuals]
    follow_up = getattr(result, "follow_up", None)

    # ✅ Save to DB
    chat_entry = ChatHistory(
        query=request.user_query,
        agent="Agent",
        response=text,
        steps="\n".join([getattr(s, "description", str(s)) for s in steps]) if steps else None,
        visual="\n".join(visuals) if visuals else None,
        follow_up=follow_up
    )
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)

    # ✅ Stream back response
    async def event_generator():
        if text:
            yield "\n--- AI Response ---\n"
            for word in text.split(" "):
                yield word + " "
                await asyncio.sleep(0.05)
        if steps:
            yield "\n\n--- Steps Taken ---\n"
            for step in steps:
                description = getattr(step, "description", str(step))
                yield description + "\n"
                await asyncio.sleep(0.05)
        if visuals:
            yield "\n--- Visuals ---\n"
            for vis_data in visuals:
                yield vis_data + "\n"
                await asyncio.sleep(0.05)
        if follow_up:
            yield "\n--- Follow-up ---\n"
            yield follow_up + "\n"

    return StreamingResponse(event_generator(), media_type="text/plain")

@app.get("/history")
def get_history(db=Depends(get_db)):
    """
    Retrieve full chat history from database.
    """
    chats = db.query(ChatHistory).all()
    return chats