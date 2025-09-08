import openai
import os
import requests
import json
from dotenv import load_dotenv
from typing import List, Any

# Load environment variables from .env file
load_dotenv()

# Load your OpenAI API key from environment variable or config
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the data sheet as the system prompt
DATA_SHEET_PATH = os.path.join(os.path.dirname(__file__), "data_sheet.txt")
with open(DATA_SHEET_PATH, "r", encoding="utf-8") as f:
    DATA_SHEET_PROMPT = f.read()

PATIENT_API_URL = "http://localhost:5000/patient"
def get_patient_info(patient_id: str) -> dict[str, Any] | None:
    """Fetch patient info from the Flask API."""
    try:
        resp = requests.get(f"{PATIENT_API_URL}/{patient_id}")
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
    except Exception:
        return None

class AppointmentAgent:
    def __init__(self, patient_info: dict[str, Any]):
        patient_info_str = ""
        if patient_info:
            # Format patient info as readable text for the prompt
            patient_info_str = "\nPATIENT INFO:\n" + json.dumps(patient_info, indent=2)
        self.system_prompt = (
            "You are a helpful assistant for nurses scheduling follow-up appointments. "
            "Answer user questions using the data sheet and patient info where possible. "
            "Format information in a readable manner, using newlines and tabs."
            "If the user asks for patient information from an ID or name you don't have, instruct them to create a new conversation with that patient ID."
            "If the information is missing, say so. \n\n"
            "DATA SHEET:\n"
            f"{DATA_SHEET_PROMPT}"
            f"{patient_info_str}"
        )
        self.messages: List[dict[str, Any]] = []

    def start_chat(self):
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

    def ask(self, user_input: str) -> str | None:
        self.messages.append({"role": "user", "content": user_input})

        # Call the OpenAI Agents API (function calling)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=self.messages, # type: ignore
        )

        reply = response.choices[0].message

        self.messages.append({"role": "assistant", "content": reply.content})
        return reply.content

# Example usage
if __name__ == "__main__":
    agent = AppointmentAgent({"name": "Bob Builder"})
    agent.start_chat()
    print("Welcome to the Appointment Agent. Type 'quit' to exit.")
    while True:
        user_input = input("Nurse: ")
        if user_input.lower() == "quit":
            break
        reply = agent.ask(user_input)
        print("Agent:", reply)