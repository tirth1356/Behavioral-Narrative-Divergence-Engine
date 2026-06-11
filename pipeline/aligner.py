import os
import json
import numpy as np
import time
from groq import Groq
from sklearn.preprocessing import RobustScaler, MinMaxScaler

class DomainAligner:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None

    def batch_get_n(self, texts, domain):
        """
        Extracts narrative intensity using Llama 3.1 via Groq in BATCH mode.
        Fixes the 'Sentiment Loophole' and significantly reduces API calls.
        """
        if not self.client:
            # Fallback for testing
            return np.array([0.5 if isinstance(t, str) and t.strip() else np.nan for t in texts])
            
        prompt = (
            f"Here is a JSON list of journal entries. Rate how intensely the user claims to have engaged in {domain} "
            f"for each entry on a scale from 0.0 to 1.0. Ignore negative sentiment or complaints about not doing it.\n"
            f"Entries: {json.dumps(texts)}\n"
            f"Return ONLY a valid JSON object with a single key 'scores' containing a list of exactly {len(texts)} floats. "
            f"If an entry is empty or invalid, output 0.0."
        )
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a strict data extractor. Return only a valid JSON object."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            
            output = response.choices[0].message.content
            data = json.loads(output)
            scores = data.get("scores", [])
            
            intensities = []
            for i, text in enumerate(texts):
                if not isinstance(text, str) or not text.strip():
                    intensities.append(np.nan)
                else:
                    try:
                        val = float(scores[i])
                        intensities.append(np.clip(val, 0.0, 1.0))
                    except (IndexError, ValueError, TypeError):
                        intensities.append(np.nan)
                        
            time.sleep(0.1) # Be kind to rate limits
            return np.array(intensities)
            
        except Exception as e:
            print(f"Groq API error for domain {domain}: {e}")
            return np.array([np.nan] * len(texts))

    def normalize(self, series):
        vals = np.array(series).reshape(-1, 1)
        if np.std(vals) == 0:
            return np.zeros_like(series, dtype=float)
        
        rob = RobustScaler().fit_transform(vals)
        return MinMaxScaler().fit_transform(rob).flatten()

    def get_b(self, df, domain):
        if domain == 'fitness':
            s = self.normalize(df['steps'])
            e = self.normalize(df['exercise_minutes'])
            return (s + e) / 2.0
        elif domain == 'work':
            return self.normalize(df['deep_work_hours'])
        elif domain == 'screen_time':
            return self.normalize(df['screen_time_hours'])
        elif domain == 'sleep':
            return self.normalize(df['sleep_hours'])
        return np.zeros(len(df))
