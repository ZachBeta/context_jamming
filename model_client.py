import httpx
from typing import List, Dict

class OpenRouterClient:
    """
    Client for OpenRouter API to call chat completions.
    """
    def __init__(self, api_key: str, model: str, base_url: str = "https://openrouter.ai"):
        self.api_key = api_key
        self.model = model
        self.client = httpx.Client(base_url=base_url)

    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.7, top_p: float = 1.0, max_tokens: int = 512) -> str:
        """
        Send a chat completion request and return the assistant's reply.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens
        }
        response = self.client.post("/api/v1/chat/completions", json=payload, headers=headers)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"OpenRouter HTTP error {response.status_code}: {response.text}") from e
        try:
            data = response.json()
        except ValueError:
            raise RuntimeError(f"OpenRouter returned non-JSON response: {response.text}")
        return data["choices"][0]["message"]["content"]
