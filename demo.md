# Interview Demo Guide: Chronis Task B

This guide gives you the exact narrative and commands to impress the hiring team by walking them through your architecture, the loopholes you spotted, and the ultimate LLM upgrade you implemented.

## 1. Setting the Stage
**What to say:**
*"Chronis is about mapping the delta between narrative intent and behavioral truth. To do this securely without sounding judgmental, I built a modular data pipeline that translates qualitative text and quantitative logs into a standard `0.0` to `1.0` scale, subtracts them, and maps the math to four canonical psychology types: Overstatement, Understatement, Blind Spot, and Aspiration Gap."*

## 2. Showcasing the Architecture
**What to show:** Open the project folder structure.
**What to say:**
*"I built this to production-grade standards. Everything is strictly separated. Raw data sits in `data/`, the engine sits in `pipeline/`, and the objective JSON reports drop into `results/`. I also included a strict `pytest` suite and a `decisions.md` doc outlining my technical choices."*

## 3. Highlighting the "Sentiment Loophole" Pivot
This is where you show off your engineering maturity.

**What to say:**
*"Initially, I used a lightweight local embedding model (`all-MiniLM-L6-v2`) via `sentence-transformers` and cosine similarity. It was blazing fast. However, I identified a critical flaw: **The Sentiment Loophole**. If a user wrote 'I hate working out and skipped the gym', cosine similarity would see 'working out' and 'gym', score the fitness intensity highly, and falsely trigger an 'Overstatement'."*

*"To fix this, I ripped out local embeddings and implemented an LLM extraction approach using the ultra-fast **Llama 3.1 8B Instant** model via the **Groq API**."*

*"However, calling an LLM for every single day for every user (140+ calls) was too slow for production. So, I engineered a **Batch Prompting** architecture. By bundling a full week of journal entries into a single prompt and constraining the model to output a strictly formatted JSON array, I reduced the API calls by 85%. The pipeline now completes the entire dataset in a few seconds."*

**What to show:** Open `pipeline/aligner.py` and show the `batch_get_n` function, specifically pointing out the `response_format={"type": "json_object"}` parameter.

## 4. The Abstention Gate & Structural Safety
**What to say:**
*"In a healthcare/psychology product, a false positive is dangerous. I built an Abstention Gate in `classifier.py`. If a user doesn't have at least a week of logs and a few journal entries, the pipeline refuses to guess and outputs `INSUFFICIENT_EVIDENCE`."*

*"Finally, to enforce **Structural Safety**, `formatter.py` locks the output into a strict JSON schema. The AI doesn't write free-form paragraphs diagnosing the user. It just returns the raw math, a sterile classification string, and a mapped evidence summary. It's mathematically impossible for this system to be subjective or preachy."*

## 5. Running the Demo Live
If they want to see it run, follow these steps exactly in your Windows PowerShell:

1. **Set your API Key:**
   ```powershell
   $env:GROQ_API_KEY="your_groq_api_key_here"
   ```

2. **Activate the Environment:**
   *(Ensure you use the direct python executable to prevent system Python conflicts)*

3. **Run the Tests:**
   Show them the test suite passing the boundaries:
   ```powershell
   .\venv\Scripts\python.exe -m pytest tests/test_pipeline.py
   ```

4. **Run the Pipeline:**
   ```powershell
   .\venv\Scripts\python.exe main.py
   ```

5. **Show the Result:**
   Open a file inside the `results/` folder (like `U1_fitness.json`) to show them the sterile, objective JSON output.
