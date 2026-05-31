import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field


@dataclass
class CouncilReport:
    """
    The final object returned after all agents finish.
    Contains everything — individual findings + final verdict.
    """
    specialist_findings: dict = field(default_factory=dict)  # {specialty: finding}
    consensus: str = ""                                       # final aggregator output
    traces: dict = field(default_factory=dict)               # {specialty: time_taken}
    total_time: float = 0.0


class MedEngine:
    """
    Runs all specialist agents in parallel isolated threads.
    Collects findings and passes them to the aggregator.
    """

    def __init__(self, agents: list, aggregator):
        """
        agents     : list of MedAgent instances
        aggregator : ConflictChecker or ClinicalSynthesizer instance
        """
        self.agents = agents
        self.aggregator = aggregator

    def _run_agent(self, agent, patient_case: str) -> tuple[str, str, float]:
        """
        Runs a single agent and tracks how long it took.
        Returns (specialty, finding, time_taken)
        """
        start = time.time()
        finding = agent.execute(patient_case)
        elapsed = round(time.time() - start, 2)
        return agent.specialty, finding, elapsed

    def run(self, patient_case: str, show_log: bool = True) -> CouncilReport:
        """
        Main method — fires all agents in parallel, collects results,
        passes to aggregator, returns CouncilReport.
        """
        report = CouncilReport()
        start_total = time.time()

        if show_log:
            print("\n" + "═" * 55)
            print("  🏥  MEDCOUNCIL — Specialist Panel Initiated")
            print("═" * 55)
            print(f"  Specialists summoned : {len(self.agents)}")
            for a in self.agents:
                print(f"    → {a.specialty}")
            print("  Running in parallel isolation...")
            print("─" * 55)

        # Fire all agents simultaneously in separate threads
        with ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
            futures = {
                executor.submit(self._run_agent, agent, patient_case): agent
                for agent in self.agents
            }

            for future in as_completed(futures):
                specialty, finding, elapsed = future.result()
                report.specialist_findings[specialty] = finding
                report.traces[specialty] = f"{elapsed}s"

                if show_log:
                    print(f"  ✓ {specialty} — completed in {elapsed}s")

        if show_log:
            print("─" * 55)
            print("  All specialists done. Aggregator reviewing...\n")

        # Pass all findings to aggregator
        report.consensus = self.aggregator.execute(report.specialist_findings)
        report.total_time = round(time.time() - start_total, 2)

        if show_log:
            print("─" * 55)
            print(f"  ✓ Aggregator done — total time: {report.total_time}s")
            print("═" * 55 + "\n")

        return report