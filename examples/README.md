

---

🏥 Healthcare AI Assistant — Google ADK + Gemini API

A lightweight, secure, and modular medical AI agent built using Google’s AI Development Kit (ADK).


---

📌 Overview

The Healthcare AI Assistant is an end-to-end medical support agent designed to run in Python / Colab / Jupyter using the Google ADK framework and Gemini API.
It includes: from 

Clinical question answering

Symptom → summary generation

Safe-response guardrails

Optional structured output for medical forms

Ready-to-deploy ADK Agent class

Notebook-ready example usage


This project is perfect for developers, researchers, and students wanting to prototype healthcare AI systems.


---

🚀 Features

🧠 Core Capabilities

Medical Q&A (non-diagnostic)

Symptom triage suggestions

Generate prescriptions (educational only)

Summaries for doctors

Convert text → structured JSON medical records

Provide patient-friendly explanations

Follow safety instructions based on ADK Guardrails


🛡 Safety & Compliance

Guardrails for hallucination reduction

Medical safety pre-prompt

Restricted outputs (no diagnosis without disclaimer)

HIPAA-friendly local processing (no patient identifiers stored)



---

📁 Project Structure

/healthcare-ai-adk
│
├── notebooks/
│ └── healthcare_ai_agent.ipynb
│
├── src/
│ ├── agent.py
│ ├── prompts.py
│ └── utils.py
│
├── assets/
│ └── architecture-diagram.png
│
└── README.md ← You are here


---

🧩 Architecture Diagram

User Input → ADK Agent → Gemini 2.0 Model → Safety Layer → Final Output


---

🔑 Setup Instructions

1️⃣ Install Dependencies

pip install -q -U google-generativeai google-ai-python google-ai-generativelanguage
pip install -q google-auth python-dotenv


---

2️⃣ Configure API Key

Get your Gemini API key from:
👉 https://aistudio.google.com/app/apikey

Then create a .env file:

GEMINI_API_KEY=your_api_key_here

Or set inside notebook:
~~~
import os
os.environ["GEMINI_API_KEY"] = "your_api_key_here"

~~~
---

🧪 Run the Healthcare ADK Agent

Initialize the Agent

from agent import HealthcareAIAgent

agent = HealthcareAIAgent()

Ask a Medical Question

agent.run("Patient has fever, cold, body ache. Suggest next steps.")

Generate a Summary

agent.run("Create a doctor summary for: persistent cough for 5 days")

Produce Structured Medical JSON

agent.run_json("Symptoms: fever, cough, sore throat")


---

🧠 Inside the Agent (ADK Example)

Your project includes an ADK-powered agent similar to:

from google import genai
~~~
class HealthcareAIAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.system_prompt = open("src/prompts.py").read()

    def run(self, user_prompt):
        completion = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                {"role": "system", "text": self.system_prompt},
                {"role": "user", "text": user_prompt}
            ]
        )
        return completion.text

~~~
---

🧱 Prompting & Safety Layer

Prompts include:

✔ Medical Safety Instructions
✔ Always add disclaimers
✔ No harmful instructions
✔ No diagnosis without confidence disclaimer
✔ Encourage professional consultation

Stored in:

/src/prompts.py


---

📙 Notebook Included

The healthcare_ai_agent.ipynb notebook includes:

API setup cells

Agent creation

Step-by-step pipeline explanation

Example prompts

JSON structured outputs

Diagram + flowchart

Test runs


You can run it directly in Google Colab.


---

🎯 Use Cases

Use Case Example

Symptom guidance “Child has 102°F fever—what to do?”
Summary “Summarize patient visit notes.”
Medication info “Explain Paracetamol dosage for adults.”
Report creation “Generate a discharge summary sample.”
Health education “Explain diabetes in simple terms.”



---

⚠️ Disclaimer

This project is for education and prototyping only.
It does not provide medical advice, diagnosis, or emergency recommendations.
Always consult a licensed professional.


---

