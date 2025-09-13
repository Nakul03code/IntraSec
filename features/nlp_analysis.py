import pandas as pd
from transformers import pipeline

def run_sentiment(input_path="data/user_features.csv", output_path="data/user_features.csv"):
    sentiment_analyzer = pipeline("sentiment-analysis")
    df = pd.read_csv(input_path)

    df['message_sentiment'] = df['message'].apply(lambda x: sentiment_analyzer(x)[0]['label'])
    df['message_sentiment_score'] = df['message'].apply(lambda x: sentiment_analyzer(x)[0]['score'])

    df.to_csv(output_path, index=False)
    print(f"[OK] Sentiment scores saved to {output_path}")

if __name__ == "__main__":
    run_sentiment()
