import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

load_dotenv()

app = FastAPI(title="SignalHunter")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing from .env")

if not HINDSIGHT_API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY is missing from .env")

groq = Groq(api_key=GROQ_API_KEY)

hindsight = Hindsight(
    base_url=HINDSIGHT_BASE_URL,
    api_key=HINDSIGHT_API_KEY
)

BANK_ID = "signalhunter"


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "SignalHunter backend is running"
    }


@app.post("/analyze")
def analyze(data: dict):
    competitor = data.get("competitor", "Unknown competitor")
    information = data.get("information", "")

    if not information:
        raise HTTPException(
            status_code=400,
            detail="Competitor information is required"
        )

    # 1. Recall previous competitor information
    try:
        memories = hindsight.recall(
            query=f"Previous information and strategic signals about {competitor}",
            bank_id=BANK_ID
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Hindsight recall failed: {str(e)}"
        )

    # 2. Ask Groq to analyze current information against memory
    prompt = f"""
You are SignalHunter, an AI competitive intelligence agent.

Competitor:
{competitor}

Current competitor information:
{information}

Previous remembered information:
{memories}

Analyze the competitor and identify:

1. Current strategic signal
2. Important changes compared with previous information
3. Possible strategic direction
4. Key competitive insight

If previous information is unavailable, clearly say that this is the first analysis.

Give a concise, useful business analysis.
"""

    try:
        response = groq.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI competitive intelligence analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        analysis = response.choices[0].message.content

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Groq analysis failed: {str(e)}"
        )

    # 3. Retain the new learning in Hindsight
    memory_to_store = f"""
Competitor: {competitor}

Current information:
{information}

SignalHunter analysis:
{analysis}
"""

    try:
        hindsight.retain(
            content=memory_to_store,
            bank_id=BANK_ID
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Hindsight retain failed: {str(e)}"
        )

    return {
        "status": "success",
        "competitor": competitor,
        "recalled_memory": memories,
        "analysis": analysis,
        "memory_saved": True
    }