from src.base import MedAgent


class CardiologistAgent(MedAgent):

    def __init__(self, llm_callable):
        super().__init__(
            specialty="Cardiologist",
            expertise_areas=[
                "chest pain", "palpitations", "hypertension",
                "ECG abnormalities", "heart failure", "coronary artery disease",
                "myocardial infarction", "arrhythmia"
            ],
            llm_callable=llm_callable
        )

    def execute(self, patient_case: str) -> str:
        prompt = self._build_prompt(patient_case)
        return self.llm_callable(prompt)