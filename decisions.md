# Architecture & Engineering Decisions: Task B

This document outlines the architectural and mathematical decisions behind the Behavioral-Narrative Divergence pipeline. The system is designed for deterministic execution, structural safety, and high testability.

## 1. The Alignment Strategy: Sentiment-Aware LLM Extraction
To align unstructured journal snippets with numeric behavioral data, the pipeline uses a fast LLM rather than naive semantic embeddings. 

**Decision**: The pipeline utilizes the `llama-3.1-8b-instant` model via the Groq API.
**Justification**:
- **Failure Modes of LLM Alignment**: While LLM extraction solves sentiment ignorance, it introduces new failure modes: hallucinated extra text (breaking JSON parsing) and API rate-limiting. To mitigate this, the pipeline enforces strict `response_format={"type": "json_object"}` and includes sleep delays.

## 2. Type Boundaries
The classification relies on translating text frequency ($N$) and behavioral logs ($B$) to a 0.0 - 1.0 scale. The divergence types are rigidly defined as follows:
- **Overstatement**: Delta ($N - B$) > 0.35 AND $B < 0.5$. (User claims intense engagement, but objective data is low).
- **Understatement**: Delta < -0.35 AND $B > 0.5$. (User's data shows high engagement, but narrative minimizes it).
- **Blind Spot**: Mean $N < 0.15$ AND Mean $B > 0.55$. (Behavior is extremely high, but absent from conscious journaling).
- **Aspiration Gap**: Mean $N > 0.6$ over the window, but the linear regression slope of $B \le 0$. (Persistent high intent paired with flat or declining actual behavior).

## 3. The Abstention Gate: Refusal Logic
In production engineering, returning a confident but incorrect classification due to sparse data is a critical failure. 

**Refusal Logic**: The `evaluate_abstention` method requires a minimum of 7 valid behavioral logs and at least 3 valid journal entries within the rolling evaluation window. If these thresholds are not met, the system completely refuses to calculate divergence and explicitly outputs an `INSUFFICIENT_EVIDENCE` state. It refuses to make predictions on statistically sparse data to prevent false or premature labels.

## 4. Structural Safety
The brief strictly demands that the system cannot make medical or characterological judgments. 

**Decision**: The final output is routed through a `JSONFormatter` that enforces a rigid, predefined schema. The AI is strictly barred from generating subjective diagnostic text (e.g., "The user is lazy or undisciplined"). Instead, the system only outputs raw mathematical primitives and algorithmic string enums (e.g., `OVERSTATEMENT`), ensuring characterological judgments are structurally impossible.

## 4. Normalization of Behavioral Outliers
Behavioral metrics (e.g., steps vs. screen time hours) have vastly different scales and distributions.

**Decision**: The pipeline leverages `RobustScaler` followed by `MinMaxScaler`.
**Justification**:
- `RobustScaler` uses the interquartile range (IQR) to normalize the data without being heavily skewed by extreme statistical outliers (e.g., a marathon day ruining the scale for normal steps).
- `MinMaxScaler` then strictly squashes the values into the required `[0, 1]` range to allow for clean delta math ($N - B$).
