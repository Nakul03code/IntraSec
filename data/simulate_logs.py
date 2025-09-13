import pandas as pd
import random
from datetime import datetime, timedelta
import os

def simulate_logs(output_path="data/user_features.csv", n=300):
    users = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']

    # Assign each user a fixed city (you can expand this list)
    user_locations = {
        'Alice': 'New York',
        'Bob': 'London',
        'Charlie': 'Delhi',
        'David': 'Berlin',
        'Eve': 'Tokyo'
    }

    messages = [
        "Please approve urgently",
        "Team meeting postponed",
        "Budget review needed",
        "Sensitive info requested",
        "Password reset required",
        "Confidential data access",
        "Urgent escalation needed",
        "Let’s discuss offline"
    ]

    logs = []
    for _ in range(n):
        user = random.choice(users)
        msg = random.choice(messages)
        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 30), 
            hours=random.randint(0, 23)
        )
        emotion_score = random.uniform(0, 1)
        influence_score = random.uniform(0, 1)
        location = user_locations[user]  # 🗺️ Assign location based on user

        logs.append([user, msg, emotion_score, influence_score, timestamp, location])

    df = pd.DataFrame(
        logs, 
        columns=['user', 'message', 'emotion_score', 'influence_score', 'timestamp', 'location']
    )

    os.makedirs("data", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[OK] Simulated logs saved to {output_path}")


if __name__ == "__main__":
    simulate_logs()
