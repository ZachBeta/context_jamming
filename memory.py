from model_client import OpenRouterClient

class SlidingWindowMemory:
    """
    Keeps the last N (user_input, response) pairs and exposes them as chat messages.
    """
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.history: list[tuple[str,str]] = []

    def add_turn(self, user_input: str, response: str) -> None:
        """Record a new turn and evict the oldest if over capacity."""
        self.history.append((user_input, response))
        if len(self.history) > self.window_size:
            self.history.pop(0)

    def get_messages(self) -> list[dict]:
        """Return a list of `{role, content}` dicts reflecting past turns."""
        messages: list[dict] = []
        for user_input, response in self.history:
            messages.append({"role": "user", "content": f"Player: {user_input}"})
            messages.append({"role": "assistant", "content": response})
        return messages

class RollingSummaryMemory:
    """
    Maintains a summary of older history plus raw last N turn pairs.
    """
    def __init__(self, client: OpenRouterClient, raw_window_size: int):
        self.client = client
        self.raw_window_size = raw_window_size
        self.raw_history: list[tuple[str, str]] = []
        self.summary: str = ""
    
    def add_turn(self, user_input: str, response: str) -> None:
        # Append new turn and roll into summary if needed
        self.raw_history.append((user_input, response))
        if len(self.raw_history) > self.raw_window_size:
            old_user, old_resp = self.raw_history.pop(0)
            # Summarize the evicted turn via LLM
            summary_prompt = [
                {"role": "system", "content": "Summarize the following game turn in one concise sentence, preserving objects and actions."},
                {"role": "user", "content": f"Player: {old_user}"},
                {"role": "assistant", "content": old_resp},
            ]
            summary_sentence = self.client.generate(summary_prompt)
            self.summary += " " + summary_sentence.strip()
    
    def get_messages(self) -> list[dict]:
        messages: list[dict] = []
        if self.summary:
            messages.append({"role": "system", "content": f"Summary: {self.summary}"})
        for user_input, response in self.raw_history:
            messages.append({"role": "user", "content": user_input})
            messages.append({"role": "assistant", "content": response})
        return messages
