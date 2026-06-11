import os
import pandas as pd
import numpy as np
from pipeline.aligner import DomainAligner
from pipeline.classifier import ChronisClassifier
from pipeline.formatter import JSONFormatter
from data_synthesis import generate_synthetic_narratives

def main():
    if not os.environ.get("GROQ_API_KEY"):
        print("WARNING: GROQ_API_KEY environment variable is missing. The Aligner will run in mock mode.")
        print("To use the Llama 3.1 8B instant model, please set your API key:")
        print("Windows PowerShell: $env:GROQ_API_KEY='your-key-here'")
        
    beh_path = 'data/Chronis_TaskA_Synthetic_Behavioral_Data_v2-2.csv'
    nar_path = 'data/synthetic_narratives.csv'
    res_dir = 'results'

    os.makedirs(res_dir, exist_ok=True)
    if not os.path.exists(nar_path):
        print("Generating synthetic narrative data...")
        generate_synthetic_narratives(beh_path, nar_path)

    df_beh = pd.read_csv(beh_path)
    df_nar = pd.read_csv(nar_path)
    
    # Sort dates
    df_beh['date'] = pd.to_datetime(df_beh['date'])
    df_nar['date'] = pd.to_datetime(df_nar['date'])

    domains = ['fitness', 'work', 'screen_time', 'sleep']
    
    aligner = DomainAligner()
    classifier = ChronisClassifier(window=7, threshold=0.35, min_logs=7, min_mentions=3)
    
    users = df_beh['user_id'].unique()
    
    for user in users:
        u_beh = df_beh[df_beh['user_id'] == user].sort_values('date').reset_index(drop=True)
        u_nar = df_nar[df_nar['user_id'] == user].sort_values('date').reset_index(drop=True)
        
        if len(u_beh) < 7:
            continue
            
        w_beh = u_beh.iloc[0:7]
        start = w_beh['date'].iloc[0].strftime('%Y-%m-%d')
        end = w_beh['date'].iloc[-1].strftime('%Y-%m-%d')
        w_dates = w_beh['date'].tolist()
        
        for d in domains:
            # Align
            b = aligner.get_b(w_beh, d)
            
            # Batch N extraction
            texts_to_batch = []
            for dt in w_dates:
                row = u_nar[u_nar['date'] == dt]
                texts_to_batch.append(row.iloc[0]['text'] if not row.empty else "")
                
            n = aligner.batch_get_n(texts_to_batch, d)
            
            # Classify
            c_type, conf, metrics = classifier.classify(n, b)
            
            # Format
            if c_type == "INSUFFICIENT_EVIDENCE":
                out = JSONFormatter.format_abstention(user, d, start, end, metrics)
            else:
                out = JSONFormatter.format_output(user, d, start, end, metrics['mean_n'], metrics['mean_b'], metrics['delta'], c_type, conf)
            
            # Save
            with open(f"{res_dir}/{user}_{d}.json", 'w') as f:
                f.write(out)
                
    print(f"Done. Saved to {res_dir}/")

if __name__ == "__main__":
    main()
