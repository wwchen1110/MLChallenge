# Multi-Agent Chat Application - Frontend

This project is a frontend implementation of a multi-agent chat application that allows users to interact with multiple agents simultaneously. The application features a user-friendly interface with a scrollable sidebar for thread management, enabling users to create, rename, and delete threads. The conversation history is displayed in a layout similar to ChatGPT, providing an intuitive experience for users.

## Project Structure

The frontend is organized into the following directories and files:

- **src/**: Contains the source code for the frontend application.
  - **components/**: Contains reusable components for the application.
    - **Sidebar.tsx**: Displays the list of threads and provides functionality to create and delete them.
    - **ThreadList.tsx**: Renders the list of threads in the sidebar.
    - **ThreadItem.tsx**: Represents an individual thread, allowing selection or deletion.
    - **Conversation.tsx**: Displays the conversation history for the selected thread.
    - **Message.tsx**: Represents an individual message in the conversation history.
  - **pages/**: Contains the main pages of the application.
    - **ChatPage.tsx**: Integrates the sidebar and conversation components for the chat interface.
  - **App.tsx**: The main entry point for the frontend application, setting up the application structure and routing.
  - **index.tsx**: The main entry point for rendering the React application.
  - **styles/**: Contains CSS styles for the application.
    - **main.css**: Defines the layout and appearance of components.

## Setup Instructions

1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd multi-agent-chat-app/frontend
   ```

2. **Install Dependencies**: 
   ```
   npm install
   ```

3. **Run the Application**: 
   ```
   npm start
   ```

4. **Access the Application**: Open your browser and navigate to `http://localhost:3000` to view the application.

## Usage

- **Creating Threads**: Use the sidebar to create new threads by entering a patient ID.
- **Deleting Threads**: Remove threads that are no longer needed from the sidebar.
- **Viewing Conversations**: Select a thread to view its conversation history in the main display area.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.