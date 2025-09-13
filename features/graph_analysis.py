import pandas as pd
import networkx as nx
from pyvis.network import Network
import random
import os

def build_graph(input_path="data/user_features.csv", output_path="dashboard/graph.html"):
    df = pd.read_csv(input_path)

    G = nx.Graph()
    for idx, row in df.iterrows():
        other_user = random.choice(df['user'].tolist())
        if other_user != row['user']:
            G.add_edge(row['user'], other_user, weight=row['influence_score'])

    net = Network(height='600px', width='100%')
    net.from_nx(G)

    os.makedirs("dashboard", exist_ok=True)
    net.write_html(output_path)
    print(f"✅ Graph saved at {output_path}")

if __name__ == "__main__":
    build_graph()
