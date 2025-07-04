import argparse
from core import (
    policy_injector,
    config_mapper,
    drift_engine,
    auto_remediator,
    feedback_verifier,
    audit_logger,
    self_tuner,
    control_genome
)
from llm import llm_reasoner
from log_analysis import control_fitness
from telemetry import telemetry_engine
from gitops import gitops_watcher
from siem import siem_listener
from compliance import ontology_mapper
from graph import ncg_engine

def run_all():
    print("\n========== [ PHASE 0: POLICY INJECTION ] ==========")
    policy_injector.run()

    print("\n========== [ PHASE 1: CONFIG MAPPER ] =============")
    config_mapper.run()

    print("\n========== [ PHASE 2: DRIFT DETECTION ] ===========")
    drift_engine.run()

    print("\n========== [ PHASE 3: AUTO-REMEDIATION ] ==========")
    auto_remediator.run()

    print("\n========== [ PHASE 4: FEEDBACK VERIFICATION ] =====")
    feedback_verifier.run()

    print("\n========== [ PHASE 5: AUDIT LOGGER ] ==============")
    audit_logger.run()

    print("\n========== [ PHASE 6: CONTROL FITNESS SCORE ] =====")
    control_fitness.run()

    print("\n========== [ PHASE 7: SELF-TUNING ENGINE ] ========")
    self_tuner.run()

    print("\n========== [ PHASE 8: CONTROL GENOME HASHING ] ====")
    control_genome.run()

    print("\n========== [ PHASE 9: TELEMETRY ENGINE ] ==========")
    telemetry_engine.run()

    print("\n========== [ PHASE 10: GITOPS WATCHER ] ===========")
    gitops_watcher.run_once()

    print("\n========== [ PHASE 11: SIEM EVENT LISTENER ] ======")
    siem_listener.run_once()

    print("\n========== [ PHASE 12: ONTOLOGY MAPPER ] ==========")
    ontology_mapper.run()

    print("\n========== [ PHASE 13: COMPLIANCE GRAPH (NCG) ] ===")
    ncg_engine.run()

    print("\n========== [ PHASE 14: LLM PRIORITY FIXES ] =======")
    llm_reasoner.suggest_prioritized_fixes()

    print("\n All phases complete.\n")

def main():
    parser = argparse.ArgumentParser(description="ISMS Engine CLI Orchestrator")
    parser.add_argument("--phase", type=str, required=True, help="Which phase to run", choices=[
        "all", "inject", "map", "drift", "remediate", "feedback", "audit", "fitness",
        "tune", "genome", "telemetry", "gitops", "siem", "ontology", "ncg", "prioritize"
    ])

    args = parser.parse_args()
    phase = args.phase

    match phase:
        case "all": run_all()
        case "inject": policy_injector.run()
        case "map": config_mapper.run()
        case "drift": drift_engine.run()
        case "remediate": auto_remediator.run()
        case "feedback": feedback_verifier.run()
        case "audit": audit_logger.run()
        case "fitness": control_fitness.run()
        case "tune": self_tuner.run()
        case "genome": control_genome.run()
        case "telemetry": telemetry_engine.run()
        case "gitops": gitops_watcher.run_once()
        case "siem": siem_listener.run_once()
        case "ontology": ontology_mapper.run()
        case "ncg": ncg_engine.run()
        case "prioritize": llm_reasoner.suggest_prioritized_fixes()
        case _: print("Unknown phase!")

if __name__ == "__main__":
    main()
