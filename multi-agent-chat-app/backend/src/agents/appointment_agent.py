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

# Define the tool for calling external API
# def patient_info_tool(patient_id: str) -> str:
#     """Tool for the agent to fetch patient info."""
#     info = get_patient_info(patient_id)
#     if info is None:
#         return f"Could not find information for patient ID {patient_id}."
#     return str(info)

# # Define the tool for returning local DB info
# def patient_info_local_tool(patient_id: str, columns: list[str]) -> dict[str, Any]:
#     """Tool for the agent to fetch patient info from local DB."""
#     info = get_patient(patient_id)
#     if not info:
#         return {"error": f"Could not find information for patient ID {patient_id}."}
#     return {col: info.get(col) for col in columns}

# # Tool spec for OpenAI Agents API
# tools: List[ChatCompletionToolUnionParam] = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_patient_data",
#             "description": "Get specific patient data fields from the local database.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "patient_id": {
#                         "type": "string",
#                         "description": "The unique patient ID, e.g., '1'."
#                     },
#                     "columns": {
#                         "type": "array",
#                         "items": {"type": "string"},
#                         "description": "List of patient data fields to retrieve."
#                     }
#                 },
#                 "required": ["patient_id", "columns"]
#             }
#         }
#     }
# ]

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
            # tools=tools,
            # tool_choice="auto"
        )

        reply = response.choices[0].message
        print("Reply: ", reply.content, flush=True)

        # If the model wants to call a tool, handle it
        # if reply.tool_calls:
        #     self.messages.append({
        #         "role": "assistant",
        #         "content": reply.content,
        #         "tool_calls": reply.tool_calls
        #     })
        #     for tool_call in reply.tool_calls:
        #         if tool_call.function.name == "get_patient_data": # type: ignore
        #             args = json.loads(tool_call.function.arguments) # type: ignore
        #             pid = args.get("patient_id", patient_id)
        #             columns = args.get("columns", [])
        #             patient_data = patient_info_local_tool(pid, columns)
        #             self.messages.append({
        #                 "role": "tool",
        #                 "tool_call_id": tool_call.id,
        #                 "name": "get_patient_data",
        #                 "content": json.dumps(patient_data)
        #             })
        #             response2 = openai.chat.completions.create(
        #                 model="gpt-4o",
        #                 messages=self.messages, # type: ignore
        #                 tools=tools,
        #                 tool_choice="auto"
        #             )
        #             final_reply = response2.choices[0].message.content
        #             print("Reply: ", final_reply, flush=True)
        #             self.messages.append({"role": "assistant", "content": final_reply})
        #             return final_reply

        self.messages.append({"role": "assistant", "content": reply.content})
        return reply.content

# Example usage (for integration with CLI)
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