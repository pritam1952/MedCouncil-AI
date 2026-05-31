import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Single shared client — no need to create a new one per agent
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def groq_llm(prompt: str) -> str:
    """
    The single LLM callable used by all agents and aggregators.
    Takes a prompt string, returns the model's response string.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,      # Low temp = more clinical, less creative
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()