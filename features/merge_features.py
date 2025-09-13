import pandas as pd

def merge_features(input_path="data/user_features.csv", output_path="data/user_features.csv"):
    df = pd.read_csv(input_path)

    # Ensure all required columns exist
    required = ['emotion_score', 'influence_score', 'message_sentiment_score', 'emotion_risk']
    for col in required:
        if col not in df.columns:
            raise KeyError(f"Missing required feature column: {col}")

    df.to_csv(output_path, index=False)
    print(f"[OK] Features merged and saved to {output_path}")


if __name__ == "__main__":
    merge_features()
