import subprocess
import sys

steps = [
    ("Simulating logs", "data/simulate_logs.py"),
    ("Applying emotion risk", "features/emotion_analysis.py"),
    ("Running NLP sentiment analysis", "features/nlp_analysis.py"),
    ("Merging features", "features/merge_features.py"),
    ("Training anomaly detection model", "train.py"),
]

def run_step(description, script):
    print(f"\n🚀 {description} ...")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"❌ Failed at {description}")
        print(result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print("=== Insider Threat Pipeline Started ===")
    for desc, script in steps:
        run_step(desc, script)

    print("\n✅ Pipeline finished successfully!")
    print("👉 Next, run the dashboard with:\n")
    print("   python -m streamlit run dashboard/combined_dashboard.py")
