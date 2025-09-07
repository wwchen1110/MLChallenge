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
   The server will run on `http://localhost:5000`.

## API Usage

The backend exposes several API endpoints for managing agents and threads. Below are some key endpoints:

- **GET /patient/{patient_id}**: Retrieve information about a specific patient using their ID.
- **POST /threads**: Create a new conversation thread.
- **DELETE /threads/{thread_id}**: Delete an existing conversation thread.
- **GET /threads**: Retrieve a list of all conversation threads.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.