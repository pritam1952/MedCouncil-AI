class ClinicalSynthesizer:
    """
    Merges all specialist findings into one structured final report.
    The 'Chief Integration Officer' of MedCouncil.
    """

    def __init__(self, llm_callable):
        self.llm_callable = llm_callable
        self.role = "Chief Clinical Synthesizer"

    def _format_findings(self, specialist_findings: dict) -> str:
        """Formats the findings dict into a clean string for the LLM."""
        formatted = ""
        for specialty, finding in specialist_findings.items():
            formatted += f"\n{'─'*40}\n"
            formatted += f"[ {specialty.upper()} ]\n"
            formatted += f"{finding}\n"
        return formatted

    def execute(self, specialist_findings: dict) -> str:
        compiled = self._format_findings(specialist_findings)

        prompt = f"""You are the Chief Clinical Synthesizer overseeing a medical council.
You have received independent findings from {len(specialist_findings)} specialists.
Each specialist analyzed the same patient in complete isolation.

SPECIALIST REPORTS:
{compiled}

Your job is to synthesize these into ONE structured final report.

Respond in EXACTLY this format:

COUNCIL VERDICT:
[2-3 sentence summary of most likely diagnosis based on all specialist inputs]

CONFIDENCE SCORE: [0-100%]

URGENCY LEVEL: [CRITICAL / HIGH / MODERATE / LOW]

TOP CONDITIONS TO RULE OUT:
1. [condition] — [which specialist flagged it]
2. [condition] — [which specialist flagged it]
3. [condition] — [which specialist flagged it]

IMMEDIATE RECOMMENDED TESTS:
[Combined and deduplicated list of tests from all specialists]

RED FLAGS DETECTED:
[Any emergency signals from any specialist — write NONE if nothing critical]

RECOMMENDED NEXT STEP:
[One clear action — ER immediately / urgent outpatient / routine follow-up]
"""
        return self.llm_callable(prompt)