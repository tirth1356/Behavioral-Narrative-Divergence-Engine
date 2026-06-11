# Chronis Task B: Behavioral-Narrative Divergence Scoring

Hi there! Welcome to my submission for Task B of the Chronis Hiring Assessment. 

I built this pipeline to calculate the mathematical gap between what a user *says* they do (their journal text) and what they *actually* do (their smartwatch logs). More importantly, I designed it with strict structural safety to ensure it classifies psychological patterns without ever sounding judgmental or making characterological assumptions.

## My Architectural Approach

I focused heavily on modularity and speed. Here is how I broke down the problem:

1. **The Aligner (`pipeline/aligner.py`)**: 
   Initially, I used local semantic embeddings (Cosine Similarity) to score the journal text, but I quickly realized this had a major **"Sentiment Loophole"**. If a user wrote, *"I hate working out"*, the naive embeddings saw the keyword "workout" and scored it high for fitness! 
   To fix this, I pivoted to an LLM extraction method using **Llama 3.1 8B via the Groq API**. I prompt the LLM to explicitly ignore negative sentiment and return a clean `0.0` to `1.0` score. To prevent this from being too slow, I implemented a **Batch Prompting** architecture that bundles an entire week of logs into a single JSON response, cutting API calls by 85%. I also use a `RobustScaler` to normalize the numeric behavioral data so extreme outliers don't ruin the math.

2. **The Classifier (`pipeline/classifier.py`)**:
   This is where the math happens. I hardcoded strict mathematical boundaries to categorize the gap between Narrative and Behavior into the four canonical types (Overstatement, Understatement, Blind Spot, Aspiration Gap).
   **Crucially, I built an Abstention Gate.** If a user doesn't have at least 7 days of logs and 3 journal entries, my system actively refuses to guess and outputs `INSUFFICIENT_EVIDENCE`. We shouldn't make psychological claims on sparse data.

3. **The Formatter (`pipeline/formatter.py`)**:
   To guarantee **Structural Safety**, I locked the entire output into a strict JSON schema. The LLM does not write free-form diagnostic paragraphs (which could hallucinate judgmental medical claims). It only returns primitives, floats, and predefined string enums.

## How to Run My Code

I designed this to be a fully automated, single-command pipeline. 

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set the API Key
Because I am using Groq for the sentiment-aware extraction, you'll need to pass an API key. 
**Windows PowerShell:**
```powershell
$env:GROQ_API_KEY="your_api_key_here"
```
*(If you run it without a key, I wrote a fallback mock mode so the pipeline still successfully executes deterministically).*

### 3. Run the Pipeline
```bash
python main.py
```
This single command will:
1. Auto-generate the companion synthetic narrative dataset if it's missing.
2. Run the full alignment and classification engine.
3. Save the sterile JSON output evaluations across all domains into the `results/` folder.

## Testing
I wrote a `pytest` suite that mathematically proves the type-boundaries and tests that the Abstention Gate actively blocks sparse data.
```bash
python -m pytest tests/test_pipeline.py
```

## Deeper Dive
If you'd like to understand the exact mathematical thresholds for my categories or the specific failure modes I documented during testing, please check out my `decisions.md` file!
