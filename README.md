# Behavioral-Narrative Divergence Engine (Task B)
An automated, production-grade Python pipeline designed to calculate and categorize the mathematical gap between a user's tracked behavioral data (smartwatch logs) and their self-reported narrative (journal entries).
The system relies on sentiment-aware semantic extraction and strict architectural guardrails to classify behavioral anomalies objectively, without ever generating subjective or characterological judgments.

---

## 🏗️ Architecture & Core Components

```
┌─────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   The Aligner   │ ───> │  The Classifier  │ ───> │  The Formatter   │
│ (Groq/LLM & RM) │      │ (Abstention Gate)│      │(Structural Safety│
└─────────────────┘      └──────────────────┘      └──────────────────┘

```

### 1. The Aligner (`pipeline/aligner.py`)

* **The Sentiment Loophole Fix:** Standard semantic embeddings mistake *"I hate working out"* as a high fitness commitment. This pipeline routes text to **Llama 3.1 8B (via the Groq API)** with strict prompting to isolate actual intensity and bypass negative sentiment.
* **Batch Optimization:** Bundles an entire week of textual logs into a single JSON API payload, reducing external network calls by **85%**.
* **Normalization:** Outliers in physical or digital metrics are managed using a `RobustScaler` to ensure behavioral inputs map cleanly to an intensity spectrum of **0.0 to 1.0**.

### 2. The Classifier (`pipeline/classifier.py`)

* **Divergence Typing:** Evaluates the mathematical delta between narrative focus ($N$) and behavioral reality ($B$) against strict, hardcoded conditional thresholds.
* **The Abstention Gate:** Actively blocks premature profiling. If a target tracking window contains fewer than 7 days of logs or fewer than 3 narrative entries, the engine bypasses classification and explicitly outputs `INSUFFICIENT_EVIDENCE`.

### 3. The Formatter (`pipeline/formatter.py`)

* **Structural Safety:** To mathematically eliminate hallucinated or judgmental language (e.g., calling a user "lazy"), the final output layer enforces a strict JSON schema. The engine is structurally limited to primitives, floats, and pre-defined string enums.

---

## 🚀 Quick Start

### 1. Installation

Install core dependencies:

```bash
pip install -r requirements.txt

```

### 2. Configure Environment

Set your Groq API key. If no key is provided, the pipeline gracefully defaults to a deterministic **Mock Mode** to ensure testability.

* **Linux/macOS:**
```bash
export GROQ_API_KEY="your_api_key_here"

```
* **Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_api_key_here"

```



### 3. Execution

Run the end-to-end execution script:

```bash
python main.py

```

This command automatically checks for missing data, generates a companion synthetic narrative dataset mapped to users `U1` through `U5`, triggers the processing pipeline, and outputs sterile evaluation profiles directly into the `results/` folder.

---

## 🧪 Testing & Validation

A comprehensive `pytest` suite enforces the integrity of the math thresholds, mock fallbacks, and the logic of the Abstention Gate under sparse data environments:

```bash
python -m pytest tests/test_pipeline.py

```

> 📄 **Deep Dive:** For an in-depth review of specific mathematical coordinate boundaries, structural refusal patterns, and documented system failure modes, see [decisions.md](https://www.google.com/search?q=./decisions.md).
