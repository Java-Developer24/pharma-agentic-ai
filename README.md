# 💊 Agentic AI Assistant for Pharmaceutical Research

## Overview
This project is an **Agentic AI Assistant** designed to support pharmaceutical research.  
Researchers can query a multi-agent AI backend to get insights on **drug discovery**, **clinical trial analysis**, and **drug-drug interactions**.  

The system routes queries to specialized agents, returns step-by-step analysis, visuals (dummy graphs/charts), and research recommendations.  

---

## Features

- **Multi-Agent Architecture**
  - **Coordinator Agent**: Parses queries and delegates to specialized agents.
  - **Drug Discovery Agent**: Analyzes molecular structures and predicts drug-target interactions.
  - **Clinical Trial Analysis Agent**: Validates trial designs, analyzes sample data, and recommends patient cohorts.
  - **Drug Interaction Agent**: Detects drug-drug interactions and suggests dosage adjustments.

- **Interactive Query Handling**
  - Agents can ask follow-up questions to clarify queries.
  - Step-by-step reasoning is included in responses.

- **Visual Outputs**
  - Graphs, molecular charts, and interaction diagrams (dummy visuals for demonstration).

- **Persistent Chat History**
  - Stores all conversations in a database for review and auditing.

- **Streaming Responses**
  - Responses are streamed progressively to simulate a real-time AI assistant.

---

## Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI Agent Framework**: Agno / PydanticAI (dummy logic in this prototype)
- **Database**: SQLite / Any preferred relational DB
- **Containerization**: Docker (optional)
- **Frontend (Optional)**: Streamlit for chat interface

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/pharma-agentic-ai.git
   cd pharma-agentic-ai
2)Create and activate virtual environment

python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows


3)Install dependencies

pip install -r requirements.txt


4)Run FastAPI backend

uvicorn main:app --reload


5) Run Streamlit frontend

streamlit run frontend.py


^)Access the application

FastAPI Swagger UI: http://127.0.0.1:8000/docs

Streamlit UI: http://localhost:8501

6) API Endpoints

POST /query-stream
Send a query to the AI assistant and receive a streamed response.

Request Body:

{
  "user_query": "Can you analyze compound X?"
}


Response: Streamed text containing AI response, steps, visuals, and follow-up.

GET /history
Retrieve full conversation history.
