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
