import os
import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from hindsight_client import Hindsight

from .data_loader import load_competitor_data


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing")

if not HINDSIGHT_API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY is missing")

if not HINDSIGHT_BASE_URL:
    raise RuntimeError("HINDSIGHT_BASE_URL is missing")


# ============================================================
# CLIENTS
# ============================================================

groq_client = Groq(api_key=GROQ_API_KEY)

hindsight_client = Hindsight(
    api_key=HINDSIGHT_API_KEY,
    base_url=HINDSIGHT_BASE_URL
)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="SignalHunter API",
    description="AI-powered competitive intelligence backend",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://signalhunter-1.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# FILES
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SIGNALS_FILE = os.path.join(
    BASE_DIR,
    "backend",
    "signals.json"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class AnalyzeRequest(BaseModel):
    competitor: str


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "SignalHunter backend is running"
    }


# ============================================================
# LOAD SIGNALS
# ============================================================

def load_signals():

    if not os.path.exists(SIGNALS_FILE):
        raise HTTPException(
            status_code=500,
            detail="signals.json not found"
        )

    try:
        with open(
            SIGNALS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not read signals.json: {error}"
        )


# ============================================================
# BUILD INFORMATION
# ============================================================

def build_information(signals):

    information_parts = []

    for index, signal in enumerate(signals, start=1):

        signal_type = signal.get(
            "type",
            "Unknown"
        )

        headline = signal.get(
            "headline",
            ""
        )

        date = signal.get(
            "date",
            ""
        )

        source_url = signal.get(
            "source_url",
            ""
        )

        information_parts.append(
            f"""
Signal {index}
Type: {signal_type}
Headline: {headline}
Date: {date}
Source: {source_url}
""".strip()
        )

    return "\n\n".join(information_parts)


# ============================================================
# HINDSIGHT RECALL
# ============================================================

def recall_memory(competitor):

    try:

        query = f"""
Recall historical competitive intelligence specifically
related to {competitor}.

Focus on:
- previous strategic moves
- product and platform developments
- partnerships
- ecosystem expansion
- competitive positioning
- technology direction
- previously observed patterns

Only return memories relevant to {competitor}.
Do not substitute memories about unrelated companies.
"""

        result = hindsight_client.recall(
            query=query
        )

        return result

    except Exception as error:

        return {
            "error": str(error)
        }


# ============================================================
# GROQ ANALYSIS
# ============================================================

def generate_analysis(
    competitor,
    information,
    recalled_memory
):

    prompt = f"""
You are SignalHunter, an AI competitive-intelligence analyst.

Analyze the supplied evidence about {competitor}.

IMPORTANT EVIDENCE RULES:

1. Use ONLY the supplied current signals and recalled historical
   memory.
2. Do NOT invent facts.
3. Do NOT introduce information from your general knowledge.
4. Clearly distinguish source facts from interpretation.
5. Do not claim causation unless the evidence directly supports it.
6. Do not use unsupported superlatives such as "best",
   "dominant", "leading", or "unbeatable".
7. Do not make competitor-specific claims without evidence.
8. Financial signals are not proof of financial performance.
9. Preserve company claims as company claims rather than
   treating them as independently verified facts.
10. If evidence is insufficient, explicitly say so.
11. Reference important observations using signal numbers such
    as Signal 1, Signal 2, etc.

CURRENT SIGNALS:

{information}

HINDSIGHT HISTORICAL MEMORY:

{recalled_memory}

Return exactly these five sections:

## 1. Key Developments

Identify the most important recent developments.
Use the signal numbers.

## 2. Emerging Strategic Patterns

Identify recurring strategic patterns supported by the
current signals and historical Hindsight context.

## 3. Competitive Implications

Provide 4-6 evidence-based implications.

Clearly distinguish observation from interpretation.

## 4. Areas to Monitor

Provide exactly 5 things an analyst should monitor next.

## 5. Analyst Next Actions

Provide exactly 5 concrete evidence-gathering actions.

Keep the analysis concise, professional, and useful for a
competitive-intelligence dashboard.
"""


    try:

        response = groq_client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful competitive "
                        "intelligence analyst. "
                        "Never fabricate evidence."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.15,

            max_tokens=2400
        )

        return response.choices[0].message.content

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Groq analysis failed: {error}"
        )


# ============================================================
# SAVE ANALYSIS TO HINDSIGHT
# ============================================================

def save_analysis_to_memory(
    competitor,
    analysis
):

    try:

        memory_text = f"""
SignalHunter competitive intelligence analysis
for {competitor}:

{analysis}
"""

        hindsight_client.retain(
            memory_text
        )

        return True

    except Exception:

        return False


# ============================================================
# ANALYZE ENDPOINT
# ============================================================

@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    competitor = request.competitor.strip()

    if not competitor:

        raise HTTPException(
            status_code=400,
            detail="Competitor is required"
        )


    # --------------------------------------------------------
    # Load scraper signals
    # --------------------------------------------------------

    data = load_signals()

    stored_competitor = str(
        data.get("competitor", "")
    ).strip()


    if stored_competitor.lower() != competitor.lower():

        raise HTTPException(
            status_code=400,
            detail=(
                f"signals.json currently contains "
                f"{stored_competitor}, not {competitor}. "
                f"Run the scraper for {competitor} first."
            )
        )


    signals = data.get(
        "signals",
        []
    )


    if not signals:

        raise HTTPException(
            status_code=404,
            detail="No signals found"
        )


    # --------------------------------------------------------
    # Build current evidence
    # --------------------------------------------------------

    information = build_information(
        signals
    )


    # --------------------------------------------------------
    # Load Kaggle datasets
    # --------------------------------------------------------

    try:

        datasets = load_competitor_data()

        dataset_summary = {}

        for name, df in datasets.items():

            dataset_summary[name] = {
                "rows": len(df),
                "columns": df.columns.tolist()
            }

    except Exception as error:

        dataset_summary = {
            "error": str(error)
        }


    # --------------------------------------------------------
    # Hindsight recall
    # --------------------------------------------------------

    recalled_memory = recall_memory(
        competitor
    )


    # --------------------------------------------------------
    # Generate AI analysis
    # --------------------------------------------------------

    analysis = generate_analysis(
        competitor=competitor,
        information=information,
        recalled_memory=recalled_memory
    )


    # --------------------------------------------------------
    # Save analysis to Hindsight
    # --------------------------------------------------------

    memory_saved = save_analysis_to_memory(
        competitor=competitor,
        analysis=analysis
    )


    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "status": "success",
        "competitor": competitor,
        "signals_found": len(signals),
        "signals": signals,
        "recalled_memory": recalled_memory,
        "analysis": analysis,
        "memory_saved": memory_saved,
        "dataset_summary": dataset_summary
    }