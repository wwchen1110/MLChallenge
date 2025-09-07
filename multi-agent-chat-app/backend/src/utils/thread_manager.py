from typing import Optional, Any
class ThreadManager:
    def __init__(self):
        self.threads: dict[int, dict[str, Any]] = {}
        self.thread_counter = 0

    def create_thread(self, name: str) -> int:
        """Create a new thread with a unique ID and a given name."""
        self.thread_counter += 1
        self.threads[self.thread_counter] = {
            "name": name,
            "history": []
        }
        return self.thread_counter

    def delete_thread(self, thread_id: int) -> bool:
        """Delete a thread by its ID."""
        if thread_id in self.threads:
            del self.threads[thread_id]
            return True
        return False

    def rename_thread(self, thread_id: int, new_name: str) -> bool:
        """Rename an existing thread."""
        if thread_id in self.threads:
            self.threads[thread_id]["name"] = new_name
            return True
        return False

    def get_thread(self, thread_id: int) -> Optional[dict[str, Any]]:
        """Retrieve a thread's information by its ID."""
        return self.threads.get(thread_id, None)

    def add_message_to_thread(self, thread_id: int, message: dict[str, str]) -> bool:
        """Add a message to the conversation history of a thread."""
        if thread_id in self.threads:
            self.threads[thread_id]["history"].append(message)
            return True
        return False

    def get_thread_history(self, thread_id: int) -> list[Any]:
        """Retrieve the conversation history for a specific thread."""
        if thread_id in self.threads:
            return self.threads[thread_id]["history"]
        return []

    def get_all_threads(self) -> list[dict[str, Any]]:
        """Return a list of all threads with their IDs and names."""
        return [
            {"id": thread_id, "name": thread["name"]}
            for thread_id, thread in self.threads.items()
        ]