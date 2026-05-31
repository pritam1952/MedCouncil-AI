from abc import ABC, abstractmethod


class MedAgent(ABC):
    """
    Base class for all specialist agents in MedCouncil.
    Every specialist (Cardiologist, Neurologist, etc.) inherits from this.
    """

    def __init__(self, specialty: str, expertise_areas: list[str], llm_callable):
        """
        specialty       : e.g. "Cardiologist"
        expertise_areas : e.g. ["chest pain", "ECG", "heart failure"]
        llm_callable    : the Groq function we will build — takes a prompt, returns a string
        """
        self.specialty = specialty
        self.expertise_areas = expertise_areas
        self.llm_callable = llm_callable

    def _build_prompt(self, patient_case: str) -> str:
        """
        Builds the isolation prompt.
        This is the KEY idea — forces the agent to think ONLY from their specialty.
        No other specialist's opinion leaks in.
        """
        expertise = ", ".join(self.expertise_areas)

        return f"""You are a senior {self.specialty} with 20 years of clinical experience.

YOUR STRICT RULES:
- Analyze ONLY from a {self.specialty} perspective.
- Do NOT consider other medical specialties.
- Do NOT give a general diagnosis — stay in your domain only.
- Be direct and clinical. No unnecessary explanation.

YOUR EXPERTISE AREAS: {expertise}

PATIENT CASE:
{patient_case}

Provide your findings in EXACTLY this format:

FINDINGS:
[Your specialist observations here]

POSSIBLE CONDITIONS:
[List 1-3 conditions from your domain only]

RECOMMENDED TESTS:
[Tests you would order from your specialty]

RED FLAGS:
[Any emergency signals you detect — write NONE if nothing critical]

CONFIDENCE: [Low / Medium / High]
"""

    @abstractmethod
    def execute(self, patient_case: str) -> str:
        """
        Every specialist MUST implement this.
        This is where the actual Groq API call happens.
        """
        pass

    def __repr__(self):
        return f"MedAgent(specialty={self.specialty})"