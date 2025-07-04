import yaml

def load_mappings():
    with open("compliance/control_mappings.yaml", "r") as f:
        return yaml.safe_load(f)

def run():
    print("[OntologyMapper] ISO ⇄ NIS2 / DORA Mapping")
    data = load_mappings()

    for cid, info in data.items():
        print(f"\n ISO27001: {cid} — {info['iso_name']}")
        print(f"  → DORA: {info['dora_id']} — {info['dora_desc']}")
        print(f"  → NIS2: {info['nis2_id']} — {info['nis2_desc']}")

if __name__ == "__main__":
    run()
