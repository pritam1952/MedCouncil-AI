from src.llm import groq_llm
from src.agents import CardiologistAgent

# Simple patient case
case = """
Patient: 45-year-old male
Symptoms: chest tightness, left arm numbness, sweating
Vitals: BP 155/95, HR 105
History: smoker, diabetic
"""

agent = CardiologistAgent(llm_callable=groq_llm)
result = agent.execute(case)
print(result)