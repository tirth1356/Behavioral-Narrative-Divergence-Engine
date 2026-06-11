# Architecture & Engineering Decisions

This document outlines the core technical and mathematical choices driving the Behavioral-Narrative Divergence pipeline.
---
## 1. Alignment Strategy: Sentiment-Aware LLM Extraction
Instead of naive semantic embeddings, the pipeline uses `llama-3.1-8b-instant` via the Groq API to map journal entries to numerical categories.

* **The Embedding Problem:** Standard vector embeddings fall into a **"Sentiment Loophole"**. They tag a sentence like *"I hate working out"* as high-intensity fitness purely due to keyword matching.
* **The LLM Solution:** An LLM successfully isolates actual intensity and strips out negative sentiment, scaling narrative focus ($N$) cleanly from **0.0 to 1.0**.
* **Failure Mitigation:** To prevent API rate-limiting and text hallucinations, the pipeline uses **Batch Prompting** (bundling 7 days of logs to cut API calls by **85%**) and forces structured outputs using `response_format={"type": "json_object"}`.

---
## 2. Type Boundaries
Both text frequency ($N$) and behavioral telemetry ($B$) are normalized to a standard **0.0 to 1.0** scale. The system categorizes the divergence using strict mathematical conditions:

| Divergence Type | Mathematical Conditions | Operational Meaning |
| --- | --- | --- |
| **Overstatement** | $\Delta(N - B) > 0.35 \quad \text{AND} \quad B < 0.5$ | High verbal claims paired with low objective activity logs. |
| **Understatement** | $\Delta(N - B) < -0.35 \quad \text{AND} \quad B > 0.5$ | High tracking data paired with self-critical or minimized narrative. |
| **Blind Spot** | $\bar{N} < 0.15 \quad \text{AND} \quad \bar{B} > 0.55$ | High behavioral presence that is completely omitted from self-talk. |
| **Aspiration Gap** | $\bar{N} > 0.6 \quad \text{AND} \quad \text{slope}(B) \le 0$ | Persistent high intent over time paired with flat or dropping progress. |

---
## 3. The Abstention Gate: Refusal Logic
Making psychological claims on sparse data is a critical production failure. The system implements a strict data-density firewall.

> ### 🛑 Refusal Rules
> 
> 
> An evaluation window requires a minimum baseline of **7 valid behavioral logs** and **at least 3 valid journal entries**.
> If the data falls below either threshold, the classifier halts execution and explicitly returns `INSUFFICIENT_EVIDENCE`. This protects users against premature or mathematically unstable profiling.

---
## 4. Structural Safety by Construction
The system is architecturally barred from generating qualitative character judgments (e.g., calling a user "lazy" or "undisciplined").

* **No Free-Text Output:** The entire execution ends at a native `JSONFormatter` that maps scores exclusively to numbers, floats, and predefined string enums.
* **Safety Isolation:** Because the final layer cannot generate open-ended text, it is structurally impossible for the model to generate biased or diagnostic commentary. It reports a measured numerical gap and nothing more.

---
## 5. Behavioral Outlier Normalization
Raw metrics like daily step counts and digital screen hours have radically different scales. The pipeline resolves this with a two-stage data-scaling stack:

1. **RobustScaler:** Scales values utilizing the Interquartile Range (**IQR**). This ensures that a massive outlier (like a single marathon day) doesn't squash the rest of a user's normal routine metrics down to zero.
2. **MinMaxScaler:** Compresses the output cleanly into the target **[0, 1]** range, establishing the matching mathematical foundation needed for delta comparisons.
