from src.llm import groq_llm
from src.agents import CardiologistAgent, NeurologistAgent, GeneralPhysicianAgent
from src.aggregators import ClinicalSynthesizer, ConflictChecker

# ── Patient Case ──────────────────────────────────────────
PATIENT_CASE = """
Patient  : 45-year-old male
Symptoms : chest tightness, shortness of breath, left arm numbness,
           dizziness, sweating
Vitals   : BP 150/95, HR 102, SpO2 96%
History  : smoker (15 years), Type 2 diabetic, family history of heart disease
Onset    : symptoms started 2 hours ago, progressively worsening
"""

# ── Assemble the Council ──────────────────────────────────
agents = [
    CardiologistAgent(llm_callable=groq_llm),
    NeurologistAgent(llm_callable=groq_llm),
    GeneralPhysicianAgent(llm_callable=groq_llm),
]

aggregator = ConflictChecker(llm_callable=groq_llm, show_log=True)

# ── Run ───────────────────────────────────────────────────
from src.engine import MedEngine

engine = MedEngine(agents=agents, aggregator=aggregator)
report = engine.run(patient_case=PATIENT_CASE, show_log=True)

# ── Print Full Report ─────────────────────────────────────
print("\n" + "═" * 55)
print("         MEDCOUNCIL — FINAL REPORT")
print("═" * 55)

print("\n── SPECIALIST FINDINGS ──")
for specialty, finding in report.specialist_findings.items():
    print(f"\n[ {specialty.upper()} ]")
    print(finding)

print("\n" + "═" * 55)
print("         COUNCIL CONSENSUS")
print("═" * 55)
print(report.consensus)

print("\n" + "─" * 55)
print(f"  Total time : {report.total_time}s")
print(f"  Traces     : {report.traces}")
print("─" * 55)
print("\n⚠️  DISCLAIMER: Research/educational project only.")
print("   Not for actual clinical use. Always consult a doctor.\n")