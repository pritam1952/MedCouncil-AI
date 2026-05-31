from src.base import MedAgent


class GeneralPhysicianAgent(MedAgent):

    def __init__(self, llm_callable):
        super().__init__(
            specialty="General Physician",
            expertise_areas=[
                "overall clinical picture", "common conditions",
                "diabetes", "infections", "anaemia", "thyroid disorders",
                "fever", "fatigue", "lifestyle-related conditions"
            ],
            llm_callable=llm_callable
        )

    def execute(self, patient_case: str) -> str:
        prompt = self._build_prompt(patient_case)
        return self.llm_callable(prompt)