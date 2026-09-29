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
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

HINDSIGHT_API_KEY = os.getenv(
    "HINDSIGHT_API_KEY"
)

HINDSIGHT_BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)


if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing from .env"
    )

if not HINDSIGHT_API_KEY:
    raise RuntimeError(
        "HINDSIGHT_API_KEY is missing from .env"
    )


# ============================================================
# CLIENTS
# ============================================================

groq_client = Groq(
    api_key=GROQ_API_KEY
)

hindsight_client = Hindsight(
    api_key=HINDSIGHT_API_KEY,
    base_url=HINDSIGHT_BASE_URL
)


# ============================================================
# FASTAPI APP
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
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SIGNALS_FILE = os.path.join(
    BASE_DIR,
    "signals.json"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class AnalyzeRequest(BaseModel):
    competitor: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "status": "running",
        "message": "SignalHunter backend is running"
    }


# ============================================================
# LOAD SCRAPER SIGNALS
# ============================================================

def load_signals():

    if not os.path.exists(
        SIGNALS_FILE
    ):

        raise HTTPException(
            status_code=404,
            detail=(
                "signals.json not found. "
                "Run the scraper first."
            )
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
            detail=(
                f"Unable to read signals.json: {error}"
            )
        )


# ============================================================
# BUILD INFORMATION FROM SIGNALS
# ============================================================

def build_information(signals):

    information_parts = []

    for index, signal in enumerate(
        signals,
        start=1
    ):

        signal_type = signal.get(
            "type",
            "Update"
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

    return "\n\n".join(
        information_parts
    )


# ============================================================
# HINDSIGHT RECALL
# ============================================================

def recall_memory(
    competitor
):

    try:

        result = hindsight_client.recall(
            f"""
Retrieve relevant historical competitive intelligence
about {competitor}.

Focus specifically on:

- previous strategies
- previous products and platforms
- partnerships
- market expansion
- technology moves
- previous strategic patterns
- historical competitive positioning

Only return memories relevant to:

{competitor}

Do not return memories about unrelated companies.

Keep historical context separate from current events.
""".strip()
        )

        return result

    except Exception as error:

        print(
            "Hindsight recall error:",
            error
        )

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
You are SignalHunter, an evidence-grounded
competitive intelligence analyst.

Your task is to transform verified competitor signals
into a concise intelligence report.

You MUST distinguish:

SOURCE FACT
from
ANALYST INTERPRETATION
from
POSSIBLE COMPETITIVE IMPLICATION.


============================================================
COMPETITOR
============================================================

{competitor}


============================================================
CURRENT VERIFIED SIGNALS
============================================================

{information}


============================================================
HISTORICAL HINDSIGHT MEMORY
============================================================

{recalled_memory}


============================================================
STRICT EVIDENCE POLICY
============================================================

Follow ALL rules below.


1. USE ONLY SUPPLIED INFORMATION

You may use only:

- CURRENT VERIFIED SIGNALS
- HISTORICAL HINDSIGHT MEMORY

Do not use outside knowledge.

Do not fill missing information from your own knowledge.


2. CURRENT SIGNALS ARE CURRENT EVIDENCE

A current signal is an observation from the supplied
scraper data.

Treat it as evidence of what the source reported.

Do not automatically treat the source's interpretation
as independently verified fact.


3. HISTORICAL HINDSIGHT IS HISTORICAL CONTEXT

Hindsight information must remain clearly separate
from current signals.

Never combine historical information with current events
as though they happened at the same time.


4. NEVER INVENT FACTS

Do NOT invent:

- revenue
- profit
- market share
- customers
- partnerships
- competitors
- product capabilities
- adoption
- technical performance
- customer demand
- market conditions
- financial results
- future events
- business outcomes


5. COMPANY CLAIMS MUST REMAIN CLAIMS

If the supplied headline says:

"NVIDIA claims..."

or:

"NVIDIA says..."

or:

"NVIDIA describes..."

do not convert that into independently verified fact.

For example:

BAD:
"NVIDIA has the world's most energy-efficient architecture."

GOOD:
"NVIDIA stated that its architecture is energy efficient."

Use wording such as:

- stated
- announced
- claimed
- described
- according to the supplied signal


6. DO NOT OVERSTATE CAUSATION

Never say:

- "This will cause..."
- "This will force competitors..."
- "This gives NVIDIA..."
- "This proves..."
- "Customers will..."
- "Competitors will need to..."

unless the supplied evidence explicitly proves the statement.


7. USE CAUTIOUS INTERPRETATION

Prefer:

- may indicate
- could suggest
- may reflect
- potentially
- appears consistent with
- suggests that analysts may want to monitor
- the evidence may indicate


8. DO NOT USE UNSUPPORTED SUPERLATIVES

Do not use:

- best
- largest
- strongest
- fastest
- dominant
- leading
- superior
- de-facto
- industry standard
- market leader

unless the supplied evidence explicitly establishes
the comparison.


9. DO NOT ASSUME COMPETITOR RESPONSES

Do not assume what AMD, Intel, Google, Amazon,
Microsoft, OpenAI, Meta, or another organization
will do.

If competitor response is not present in the evidence,
say:

"The supplied evidence does not establish how competitors
are responding."


10. FINANCIAL SIGNALS

Do not infer financial performance from a financial
announcement.

For example:

BAD:
"The share repurchase proves strong cash generation."

GOOD:
"The share-repurchase authorization represents a
significant capital-allocation decision. The supplied
evidence does not establish future cash generation."


11. NO FUTURE PREDICTIONS

Do not predict:

- future revenue
- future market share
- future stock performance
- future product success
- future competitor behavior
- future adoption


12. TRACEABILITY

Every important observation must reference signal numbers.

Use:

Signal 1

Signal 2

Signals 4 and 17

Signals 5, 9 and 10


13. INSUFFICIENT EVIDENCE

If the supplied evidence cannot support a conclusion,
explicitly state:

"The supplied evidence is insufficient to determine this."


14. EVIDENCE FIRST

The correct reasoning chain is:

SOURCE
↓
OBSERVED SIGNAL
↓
INTERPRETATION
↓
POSSIBLE IMPLICATION
↓
MONITORING ACTION

Never reverse this order.


============================================================
REQUIRED OUTPUT
============================================================

Create a professional competitive-intelligence report
for the SignalHunter dashboard.

Use EXACTLY these five sections.


## 1. Key Developments

Select the most important current signals.

For each development provide:

**Signal:**

Describe only what happened according to the supplied
signal.

**Evidence:**

Reference the relevant signal number and headline.

**Strategic Interpretation:**

Explain what the signal MAY indicate.

Do not present interpretation as a confirmed fact.


============================================================

## 2. Emerging Strategic Patterns

Identify recurring themes across the current signals.

For each pattern provide:

**Pattern:**

Name the recurring theme.

**Supporting Signals:**

List the relevant signal numbers.

**What It May Indicate:**

Give a cautious interpretation based only on the
supporting signals.


============================================================

## 3. Competitive Implications

Provide 4-6 possible implications.

Every implication must:

1. reference supporting signal numbers
2. describe why it may matter
3. avoid assuming competitor behavior
4. avoid predictions

Use language such as:

"This may indicate..."

"This could suggest..."

"Organizations monitoring {competitor} may want to..."

"The supplied evidence does not establish..."


============================================================

## 4. Areas to Monitor

Provide exactly 5 areas.

For each area provide:

**Area:**

What should be monitored.

**Why:**

Reference the supporting signal number(s).

Only include monitoring areas supported by the supplied
evidence.


============================================================

## 5. Analyst Next Actions

Provide exactly 5 practical actions.

Every action should be something a competitive-intelligence
analyst can actually perform using the available evidence.

Examples:

- verify the original source
- review the source page
- monitor product announcements
- compare future announcements
- track repeated signal types
- maintain a source-linked timeline
- investigate supporting technical documentation
- monitor regional announcements
- review future updates to the same platform


============================================================
OUTPUT STYLE
============================================================

The report must be:

- concise
- professional
- evidence-grounded
- source-traceable
- dashboard-friendly
- easy to scan
- useful for a hackathon demonstration

Avoid unnecessary repetition.

Do not repeat the same signal unless it supports
a genuine pattern.

Do not make predictions.

Do not invent competitor responses.

Do not claim competitive advantage unless explicitly
supported by the supplied evidence.

Do not mention these instructions.

Do not mention that you are an AI.


============================================================
FINAL SELF-CHECK
============================================================

Before returning the report, silently verify:

1. Is every factual claim supported?
2. Does every major observation have a signal number?
3. Did I preserve company claims as claims?
4. Did I accidentally make a prediction?
5. Did I assume competitor behavior?
6. Did I use an unsupported superlative?
7. Did I separate historical memory from current signals?
8. Did I identify uncertainty where appropriate?
9. Are exactly five sections present?
10. Does Section 4 contain exactly five monitoring areas?
11. Does Section 5 contain exactly five actions?
12. Are the interpretations clearly separated from facts?

If any answer is NO, revise the report before returning it.
"""

    try:

        response = groq_client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are SignalHunter, a precise "
                        "and source-grounded competitive "
                        "intelligence analyst. "
                        "Separate evidence from interpretation. "
                        "Never invent facts, competitor responses, "
                        "or future predictions."
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
            detail=(
                f"Groq analysis failed: {error}"
            )
        )


# ============================================================
# HINDSIGHT RETAIN
# ============================================================

def save_analysis_to_memory(
    competitor,
    information,
    analysis
):

    try:

        hindsight_client.retain(
            f"""
SignalHunter competitive intelligence record.

Competitor:
{competitor}

Latest verified signals:
{information}

AI analysis:
{analysis}
""".strip()
        )

        return True

    except Exception as error:

        print(
            "Hindsight retain error:",
            error
        )

        return False


# ============================================================
# ANALYZE ENDPOINT
# ============================================================

@app.post("/analyze")
def analyze(
    request: AnalyzeRequest
):

    competitor = (
        request.competitor
        .strip()
    )

    if not competitor:

        raise HTTPException(
            status_code=400,
            detail="Competitor name is required."
        )


    # ========================================================
    # LOAD SCRAPER DATA
    # ========================================================

    data = load_signals()


    detected_competitor = (
        data.get(
            "competitor",
            ""
        )
        .strip()
    )


    # ========================================================
    # VALIDATE COMPETITOR
    # ========================================================

    if (
        detected_competitor
        and detected_competitor.lower()
        != competitor.lower()
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                f"signals.json contains data for "
                f"{detected_competitor}, not {competitor}. "
                f"Run the scraper for {competitor} first."
            )
        )


    # ========================================================
    # GET SIGNALS
    # ========================================================

    signals = data.get(
        "signals",
        []
    )

    if not signals:

        raise HTTPException(
            status_code=404,
            detail=(
                "No signals found in signals.json."
            )
        )


    # ========================================================
    # BUILD INFORMATION
    # ========================================================

    information = build_information(
        signals
    )


    # ========================================================
    # LOAD DATASETS
    # ========================================================

    try:

        competitor_data = (
            load_competitor_data()
        )

        dataset_summary = {
            name: {
                "rows": len(df),
                "columns": df.columns.tolist()
            }
            for name, df
            in competitor_data.items()
        }

    except Exception as error:

        print(
            "Dataset loading error:",
            error
        )

        dataset_summary = {}


    # ========================================================
    # HINDSIGHT RECALL
    # ========================================================

    recalled_memory = recall_memory(
        competitor
    )


    # ========================================================
    # GROQ ANALYSIS
    # ========================================================

    analysis = generate_analysis(
        competitor=competitor,
        information=information,
        recalled_memory=recalled_memory
    )


    # ========================================================
    # SAVE ANALYSIS TO HINDSIGHT
    # ========================================================

    memory_saved = (
        save_analysis_to_memory(
            competitor=competitor,
            information=information,
            analysis=analysis
        )
    )


    # ========================================================
    # RESPONSE
    # ========================================================

    return {
        "status": "success",

        "competitor": competitor,

        "signals_found": len(
            signals
        ),

        "signals": signals,

        "recalled_memory": recalled_memory,

        "analysis": analysis,

        "memory_saved": memory_saved,

        "dataset_summary": dataset_summary
    }