import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def apply_emotion_risk(input_path, output_path, threshold=0.6):
    try:
        df = pd.read_csv(input_path)
        logging.info(f"Loaded data from {input_path}")

        if 'emotion_score' not in df.columns:
            raise KeyError("'emotion_score' column is missing from the data")

        df['emotion_risk'] = df['emotion_score'].where(df['emotion_score'] > threshold, 0)

        df.to_csv(output_path, index=False)
        logging.info(f"Saved with emotion_risk to {output_path}")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    apply_emotion_risk("data/user_features.csv", "data/user_features.csv")
