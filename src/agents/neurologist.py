from src.base import MedAgent


class NeurologistAgent(MedAgent):

    def __init__(self, llm_callable):
        super().__init__(
            specialty="Neurologist",
            expertise_areas=[
                "headaches", "dizziness", "numbness", "weakness",
                "seizures", "stroke", "TIA", "neuropathy",
                "cognitive decline", "tremors"
            ],
            llm_callable=llm_callable
        )

    def execute(self, patient_case: str) -> str:
        prompt = self._build_prompt(patient_case)
        return self.llm_callable(prompt)