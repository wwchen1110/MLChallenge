# Multi-Agent Chat Application Backend

This document provides an overview of the backend setup and usage for the Multi-Agent Chat Application.

## Project Structure

The backend consists of the following main components:

- **src/**: Contains the source code for the backend application.
  - **agents/**: Contains agent implementations, including `appointment_agent.py` which manages patient conversations.
  - **utils/**: Contains utility classes such as `thread_manager.py` for managing conversation threads.
  - **app.py**: The entry point for the Flask application, defining API endpoints and server setup.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd multi-agent-chat-app/backend
   ```

2. **Install Dependencies**
   Ensure you have Python and pip installed. Then, run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   Start the Flask server by executing:
   ```bash
   python src/app.py
   ```
   The server will run on `http://localhost:5001`.

## API Usage

The backend exposes several API endpoints for managing agents and threads:

- **POST /threads**: Create a new conversation thread by providing a patient ID. The backend fetches patient info from an external API and stores it in the agent for that thread.
- **DELETE /threads/{thread_id}**: Delete an existing conversation thread.
- **GET /threads**: Retrieve a list of all conversation threads (with thread ID, patient ID, and creation date).
- **POST /threads/{thread_id}/ask**: Send a message to the agent associated with a thread and receive a response.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.