# Multi-Agent Chat Application

This project is a multi-agent chat application that allows users to run multiple agents simultaneously. It features a frontend UI with a scrollable sidebar for thread management, enabling users to create, rename, and delete threads. The conversation history is displayed in a layout similar to ChatGPT's interface.

## Project Structure

```
multi-agent-chat-app
├── backend
│   ├── src
│   │   ├── agents
│   │   │   └── appointment_agent.py
│   │   ├── app.py
│   │   └── utils
│   │       └── thread_manager.py
│   ├── requirements.txt
│   └── README.md
├── frontend
│   ├── src
│   │   ├── components
│   │   │   ├── Sidebar.tsx
│   │   │   ├── ThreadList.tsx
│   │   │   ├── ThreadItem.tsx
│   │   │   ├── Conversation.tsx
│   │   │   └── Message.tsx
│   │   ├── pages
│   │   │   └── ChatPage.tsx
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── styles
│   │       └── main.css
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── README.md
```

## Backend

The backend is built using Flask and handles the logic for managing agents and threads. It includes:

- **AppointmentAgent**: Manages conversations with patients and retrieves patient information.
- **ThreadManager**: Manages the creation, deletion, and retrieval of threads, tracking conversation history for each agent.
- **API Endpoints**: Provides endpoints for frontend interaction with the agents and threads.

### Setup Instructions

1. Navigate to the `backend` directory.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python src/app.py
   ```

## Frontend

The frontend is built using React and provides a user-friendly interface for interacting with the agents. It includes:

- **Sidebar**: Displays the list of threads and allows users to manage them.
- **Conversation Display**: Shows the conversation history for the selected thread.

### Setup Instructions

1. Navigate to the `frontend` directory.
2. Install the required dependencies:
   ```
   npm install
   ```
3. Start the application:
   ```
   npm start
   ```

## Usage

Once both the backend and frontend are running, users can interact with the agents through the UI. They can create new threads, manage existing ones, and view conversation histories.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.