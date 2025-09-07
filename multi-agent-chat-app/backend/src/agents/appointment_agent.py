import openai
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load your OpenAI API key from environment variable or config
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the data sheet as the system prompt
DATA_SHEET_PATH = os.path.join(os.path.dirname(__file__), "data_sheet.txt")
with open(DATA_SHEET_PATH, "r", encoding="utf-8") as f:
    DATA_SHEET_PROMPT = f.read()

PATIENT_API_URL = "http://localhost:5000/patient"

def get_patient_info(patient_id: str) -> dict:
    """Fetch patient info from the Flask API."""
    try:
        resp = requests.get(f"{PATIENT_API_URL}/{patient_id}")
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
    except Exception:
        return None

# Define the tool for the Agents API
def patient_info_tool(patient_id: str) -> str:
    """Tool for the agent to fetch patient info."""
    info = get_patient_info(patient_id)
    if info is None:
        return f"Could not find information for patient ID {patient_id}."
    return str(info)

# Tool spec for OpenAI Agents API
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_patient_info",
            "description": "Get information about a patient given their patient ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "The unique patient ID, e.g., '1'."
                    }
                },
                "required": ["patient_id"]
            }
        }
    }
]

class AppointmentAgent:
    def __init__(self):
        self.system_prompt = (
            "You are a helpful assistant for nurses scheduling follow-up appointments. "
            "Answer user questions using the data sheet where possible. "
            "If a user asks for patient-specific information, ensure you have a patient ID. If not, ask for it."
            "Once you have a patient ID, use the get_patient_info tool to retrieve their information."
            "Format information in a readable manner, using newlines and tabs."
            "If the information is missing, say so. \n\n"
            "DATA SHEET:\n"
            f"{DATA_SHEET_PROMPT}"
        )

    def start_chat(self):
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

    def ask(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

        # Call the OpenAI Agents API (function calling)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
            tools=tools,
            tool_choice="auto"
        )

        reply = response.choices[0].message
        print("Reply: ", reply.content, flush=True)

        # If the model wants to call a tool, handle it
        if reply.tool_calls:
            # Append the assistant message with tool_calls
            self.messages.append({
                "role": "assistant",
                "content": reply.content,
                "tool_calls": reply.tool_calls
            })
            for tool_call in reply.tool_calls:
                if tool_call.function.name == "get_patient_info":
                    # Parse the arguments string to a dictionary
                    args = json.loads(tool_call.function.arguments)
                    patient_id = args.get("patient_id")
                    if not patient_id:
                        followup = "Please provide the patient ID to retrieve their information."
                        self.messages.append({"role": "assistant", "content": followup})
                        return followup
                    patient_info = patient_info_tool(patient_id)
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "get_patient_info",
                        "content": patient_info
                    })
                    response2 = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=self.messages,
                        tools=tools,
                        tool_choice="auto"
                    )
                    final_reply = response2.choices[0].message.content
                    print("Reply: ", final_reply, flush=True)
                    self.messages.append({"role": "assistant", "content": final_reply})
                    return final_reply

        # Otherwise, just return the model's answer
        self.messages.append({"role": "assistant", "content": reply.content})
        return reply.content

# Example usage (for integration with CLI)
if __name__ == "__main__":
    agent = AppointmentAgent()
    agent.start_chat()
    print("Welcome to the Appointment Agent. Type 'quit' to exit.")
    while True:
        user_input = input("Nurse: ")
        if user_input.lower() == "quit":
            break
        reply = agent.ask(user_input)
        print("Agent:", reply)