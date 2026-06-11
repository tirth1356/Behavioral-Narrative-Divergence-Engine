import pandas as pd

def generate_synthetic_narratives(beh_csv, out_csv):
    df_beh = pd.read_csv(beh_csv)
    narratives = []
    
    for i, row in df_beh.iterrows():
        user = row['user_id']
        date = row['date']
        text = ""
        
        # Overstatement
        if user == 'U1':
            if row['steps'] < 6000 and row['exercise_minutes'] < 20:
                text = "Intense exhausting workout today!"
            else:
                text = "Feeling fit."
                
        # Understatement
        elif user == 'U2':
            if row['deep_work_hours'] > 5:
                text = "Barely wrote anything today."
            else:
                text = "Normal workday."
                
        # Blindspot
        elif user == 'U3':
            text = "Nice weather today."
            
        # Aspiration
        elif user == 'U4':
            text = "Starting workout tomorrow!"
            
        # Sparse
        elif user == 'U5':
            if i < 2:
                text = "Regular day."
            else:
                continue
        
        if text:
            narratives.append({'user_id': user, 'date': date, 'text': text})
            
    pd.DataFrame(narratives).to_csv(out_csv, index=False)

if __name__ == "__main__":
    generate_synthetic_narratives('data/Chronis_TaskA_Synthetic_Behavioral_Data_v2-2.csv', 'data/synthetic_narratives.csv')
