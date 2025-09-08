from typing import Optional, Any
from datetime import datetime

class ThreadManager:
    def __init__(self):
        self.threads: dict[int, dict[str, Any]] = {}
        self.thread_counter = 0

    def create_thread(self, patient_id: str) -> int:
        """Create a new thread with a unique ID, patient ID, and creation date."""
        self.thread_counter += 1
        self.threads[self.thread_counter] = {
            "history": [],
            "patient_id": patient_id,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        return self.thread_counter

    def delete_thread(self, thread_id: int) -> bool:
        if thread_id in self.threads:
            del self.threads[thread_id]
            return True
        return False

    def get_thread(self, thread_id: int) -> Optional[dict[str, Any]]:
        return self.threads.get(thread_id, None)

    def add_message_to_thread(self, thread_id: int, message: dict[str, str]) -> bool:
        if thread_id in self.threads:
            self.threads[thread_id]["history"].append(message)
            return True
        return False

    def get_thread_history(self, thread_id: int) -> list[Any]:
        if thread_id in self.threads:
            return self.threads[thread_id]["history"]
        return []

    def get_all_threads(self) -> list[dict[str, Any]]:
        """Return a list of all threads with their IDs, patient IDs, and creation dates."""
        return [
            {"id": thread_id, "patient_id": thread["patient_id"], "created": thread["created"]}
            for thread_id, thread in self.threads.items()
        ]