from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations


class ConflictChecker:
    """
    Audits specialist findings for disagreements and conflicts.
    Runs pairwise comparisons between every pair of specialists in parallel.
    The 'Chief Justice' of MedCouncil.
    """

    def __init__(self, llm_callable, show_log: bool = True):
        self.llm_callable = llm_callable
        self.show_log = show_log
        self.role = "Chief Conflict Auditor"

    def _get_pairs(self, specialist_findings: dict) -> list[tuple]:
        """
        Generates all unique pairs of specialists.
        e.g. 3 specialists → 3 pairs: (A,B), (A,C), (B,C)
        Formula: N(N-1)/2 pairs
        """
        specialists = list(specialist_findings.items())
        return list(combinations(specialists, 2))

    def _compare_pair(
        self,
        spec1_name: str, spec1_finding: str,
        spec2_name: str, spec2_finding: str
    ) -> tuple[str, str]:
        """
        Compares one pair of specialist findings for conflicts.
        Returns (pair_label, conflict_report)
        """
        pair_label = f"{spec1_name} vs {spec2_name}"

        prompt = f"""You are a Chief Medical Auditor reviewing two specialist reports.
Your ONLY job is to find CONFLICTS or AGREEMENTS between them.

A conflict means: they disagree on diagnosis, urgency, or recommended action.
An agreement means: they reach similar conclusions independently.

[ {spec1_name.upper()} REPORT ]
{spec1_finding}

[ {spec2_name.upper()} REPORT ]
{spec2_finding}

Respond in EXACTLY this format:

CONFLICT DETECTED: [YES / NO]

TYPE: [DIAGNOSIS CONFLICT / URGENCY CONFLICT / TREATMENT CONFLICT / NO CONFLICT]

EXPLANATION:
[2-3 sentences explaining the conflict or agreement clearly]

SEVERITY: [CRITICAL / MODERATE / MINOR / NONE]
"""
        result = self.llm_callable(prompt)
        return pair_label, result

    def _run_pairwise(self, specialist_findings: dict) -> dict:
        """
        Runs all pairwise comparisons in parallel threads.
        Returns {pair_label: conflict_report}
        """
        pairs = self._get_pairs(specialist_findings)
        pair_results = {}

        if self.show_log:
            print(f"\n  Running {len(pairs)} pairwise audits in parallel...")

        with ThreadPoolExecutor(max_workers=len(pairs)) as executor:
            futures = {
                executor.submit(
                    self._compare_pair,
                    spec1_name, spec1_finding,
                    spec2_name, spec2_finding
                ): (spec1_name, spec2_name)
                for (spec1_name, spec1_finding), (spec2_name, spec2_finding) in pairs
            }

            for future in as_completed(futures):
                pair_label, result = future.result()
                pair_results[pair_label] = result

                if self.show_log:
                    # Quick peek — did it find a conflict?
                    conflict = "⚠️  CONFLICT" if "YES" in result else "✓  AGREEMENT"
                    print(f"  {conflict} — {pair_label}")

        return pair_results

    def _build_final_verdict(
        self,
        specialist_findings: dict,
        pair_results: dict
    ) -> str:
        """
        Takes all pairwise results and produces a final conflict audit report.
        """
        # Format all pair results
        formatted_pairs = ""
        for pair_label, result in pair_results.items():
            formatted_pairs += f"\n{'─'*40}\n"
            formatted_pairs += f"[ {pair_label.upper()} ]\n"
            formatted_pairs += f"{result}\n"

        prompt = f"""You are the Chief Medical Auditor producing a final conflict audit report.
You have reviewed {len(pair_results)} pairwise comparisons between specialists.

PAIRWISE AUDIT RESULTS:
{formatted_pairs}

Produce a final structured audit report in EXACTLY this format:

AUDIT SUMMARY:
[2-3 sentences summarizing overall agreement or disagreement across the council]

CONFLICTS FOUND: [number]

CONFLICT DETAILS:
[List each conflict with which specialists disagree and on what]
[Write NONE if no conflicts found]

AGREEMENTS:
[List key points all or most specialists agreed on]

RECOMMENDATION:
[Based on conflicts found — should more tests be ordered? Should a specific 
specialist take lead? Is consensus strong enough to act on?]

COUNCIL RELIABILITY SCORE: [0-100%]
[100% = full agreement, 0% = complete disagreement]
"""
        return self.llm_callable(prompt)

    def execute(self, specialist_findings: dict) -> str:
        """
        Main method called by the Engine.
        Runs all pairwise comparisons then produces final audit verdict.
        """
        if self.show_log:
            print("\n" + "═" * 55)
            print("  ⚖️   CONFLICT CHECKER — Audit Initiated")
            print("═" * 55)

        # Step 1 — run all pairwise comparisons in parallel
        pair_results = self._run_pairwise(specialist_findings)

        if self.show_log:
            print("\n  Building final audit verdict...")

        # Step 2 — synthesize into final verdict
        final_verdict = self._build_final_verdict(specialist_findings, pair_results)

        return final_verdict