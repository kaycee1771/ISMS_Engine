# ISMS Engine: Self-Healing ISMS Engine for SaaS Providers

**A next-gen backend compliance automation engine that thinks, heals, and learns.**

---
## Overview

The **Self-Healing ISMS Engine** is a modular backend-only cybersecurity automation tool designed specifically for:

- **SaaS providers** seeking embedded compliance.
- **Security engineering teams** needing infrastructure-level remediation.
- **Auditors** requiring traceable, verifiable ISMS fitness logs.

This engine automatically **injects security controls**, **maps configurations**, **detects drift**, **self-heals misconfigurations**, and **generates intelligent remediation reports**,  using both policy logic and LLM reasoning.

---
## What It Does

The Self-Healing ISMS Engine is a backend-only cybersecurity tool for **SaaS providers**, **security teams**, and **auditors** that:

- **Live Policy Injection**: ISO27001, NIS2, DORA controls applied in real-time.
- **Drift Detection & Policy Mapping**: Finds misaligned settings vs. compliance baselines.
- **Auto-Remediation**: Fixes issues automatically or escalates with approval workflows.
- **Audit Trails & Fitness Tracking**: Every action logged with risk scoring and trend tracking.
- **LLM Remediation Reasoning**: GPT-based plain-English explanations for human clarity.
- **Modular + Event-Driven**: Compatible with GitOps, CI/CD, SIEM, telemetry, and REST APIs.
- **Ontology Mapper**: Maps ISO to European cybersecurity regulations (NIS2/DORA).

All in a **fully modular backend package**. Plug it in, schedule it, call it from CI/CD, or integrate via future REST API.

---

## Architecture Diagram

```
                             +------------------+
                             | policies.yaml    |  <-- GitOps Watcher
                             +--------+---------+
                                      |
                            (Policy Injector)
                                      |
     +------------------+     +-------v--------+      +-----------------+
     | System Snapshot  +<----+ Config Mapper  +<-----+ GWS Monitor     |
     +------------------+     +-------+--------+      +-----------------+
                                     |
                          +----------v----------+
                          | Drift Detection      |
                          +----------+----------+
                                     |
                          +----------v----------+
                          | Auto-Remediation     |--+---> Approval & LLM Fixes
                          +----------+----------+  |
                                     |             |
                          +----------v----------+  |
                          | Feedback Verifier    |  |
                          +----------+----------+  |
                                     |             |
     +------------------+  +---------v--------+    |     +----------------------+
     | Audit Logger     |<-+ Control Fitness  +<---+-----+ Self-Tuning Engine   |
     +------------------+  +------------------+          +----------------------+
                                     |
        +----------------------+      |
        | Control Genome Hash  |<-----+
        +----------------------+
                                     |
                          +----------v----------+
                          | Telemetry Analyzer   |
                          +----------+----------+
                                     |
                          +----------v----------+
                          | GitOps One-shot Sync |
                          +----------+----------+
                                     |
                          +----------v----------+
                          | SIEM Listener        |
                          +----------+----------+
                                     |
                          +----------v----------+
                          | Ontology Mapper      |
                          +----------+----------+
                                     |
                          +----------v----------+
                          | Compliance Graph     |
                          +----------+----------+
                                     |
                          +----------v----------+
                          | LLM Reasoner         |
                          +----------------------+
```

---

## How to Run It

### Requirements

* Python 3.10+
* Install dependencies:

```bash
pip install -r requirements.txt
```

### CLI Usage

```bash
python ISMS_engine.py --phase all       # Run all phases end-to-end
python ISMS_engine.py --phase 0         # Run just policy injection
python ISMS_engine.py --phase 3         # Run just auto-remediation
```

### Directory Structure

```
ISMS_Engine/
├── ISMS_engine.py             # CLI 
├── core/                      # Compliance core logic
│   ├── config_mapper.py
│   ├── drift_detector.py
│   ├── auto_remediator.py
│   ├── audit_logger.py
│   ├── feedback_verifier.py
│   ├── control_fitness.py
│   ├── self_tuner.py
│   ├── control_genome.py
│   └── telemetry_engine.py
├── policy_engine/
│   └── policy_injector.py
├── gitops/
│   └── gitops_watcher.py
├── siem/
│   └── siem_listener.py
├── llm/
│   └── llm_reasoner.py
├── resources/
│   └── controls.yaml          # Live control expectations
├── logs/                     # Drift, audit, genome, telemetry logs
└── requirements.txt
```

---

## Advanced features

* **Control Genome Fingerprinting**: SHA256 fingerprint of each policy config for chain-of-trust.
* **LLM Reasoning**: GPT-4 explains drift causes and remediation in plain English.
* **Self-Tuning**: Learns new baselines over time using `river.stats.Mean()`.
* **NIS2/DORA Ontology Mapper**: Auto-maps ISO controls to modern European regulations.
* **Neural Compliance Graph (NCG)**: (WIP) Detect control interdependencies and weaknesses.
* **GitOps + SIEM Events**: React to live policy and threat signal changes.
* **Modular Phases**: Each phase is reusable, pluggable, and CLI-runnable.
* **Drift-aware Fitness Tracking**: Line chart tracking and risk prioritization (soon).

---

## Design

- **Modular by Design**: Each component is pluggable and callable independently.
- **Backend-Only**: CI/CD and infra-centric workflows. No frontend needed.
- **Explainable Compliance**: Transparency through LLM-powered narratives.
- **DevOps Ready**: Supports hooks for GitOps, REST APIs, SIEMs, and telemetry.

---

## Sample Output

```bash
========== [ PHASE 3: AUTO-REMEDIATION ] ==========
[Phase 3] Auto-Remediation Engine Running...
[~] Executing remediation for: Password min length has changed.
[+] Enforcing password policy...

========== [ PHASE 4: FEEDBACK VERIFICATION ] =====
Control A.10.1.1 still violated:
    - Password minimum length is too low.

========== [ PHASE 14: LLM PRIORITY FIXES ] =======
"The system is enforcing a minimum length of 8 characters instead of 12. Weak passwords increase brute-force risk. Please update policy to match ISO27001 A.10.1.1."
```

---

## License

MIT License. For research, compliance automation, and education.

---

## Maintainer

Built by Kelechi Okpala for advanced compliance R&D.
For suggestions, ideas, or contributions, contact at kelechi.okpala13@yahoo.com
