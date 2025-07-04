import json
import os
import datetime
import networkx as nx
import matplotlib.pyplot as plt

AUDIT_LOG = "logs/audit.log"
GRAPH_FILE = "logs/ncg_graph.json"

def run():
    print("[NCG] Building Neural Compliance Graph...")

    G = nx.DiGraph()

    if not os.path.exists(AUDIT_LOG):
        print("[NCG] No audit log found.")
        return

    with open(AUDIT_LOG, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("[NCG] Failed to parse audit log.")
            return

    for entry in data:
        timestamp = entry.get("timestamp")
        status = entry.get("status", "unknown")
        for v in entry.get("violations", []):
            control_id = "A.10.1.1" if "Password" in v else "A.9.2.3"
            violation_node = f"violation:{v}"
            control_node = f"control:{control_id}"
            fix_node = f"script:{control_id.replace('.', '_')}"
            result_node = f"status:{status}"

            # Build edges
            G.add_edge(control_node, violation_node, label="violated_by", timestamp=timestamp)
            G.add_edge(violation_node, fix_node, label="remediated_by")
            G.add_edge(fix_node, result_node, label="result")

    # Save as adjacency list for export
    export_data = nx.readwrite.json_graph.node_link_data(G)
    with open(GRAPH_FILE, "w") as f:
        json.dump(export_data, f, indent=2)

    print(f"[NCG] Graph saved to {GRAPH_FILE}")
    print(f"[NCG] Nodes: {len(G.nodes)} | Edges: {len(G.edges)}")

    # Quick visual
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color="lightblue", font_size=7)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "label"), font_size=6)
    plt.title("Neural Compliance Graph")
    plt.tight_layout()
    plt.savefig("logs/ncg_graph.png")
    print("[NCG] Graph image saved to logs/ncg_graph.png")

if __name__ == "__main__":
    run()
