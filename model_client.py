import httpx
import time
from typing import List, Dict
from httpx import HTTPStatusError

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
        # Retry on transient HTTP or API errors
        max_retries = 3
        for attempt in range(max_retries):
            response = self.client.post("/api/v1/chat/completions", json=payload, headers=headers)
            try:
                response.raise_for_status()
            except HTTPStatusError as e:
                # Retry on server errors (5xx)
                if attempt < max_retries - 1 and response.status_code >= 500:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"OpenRouter HTTP error {response.status_code}: {response.text}") from e
            try:
                data = response.json()
            except ValueError:
                raise RuntimeError(f"OpenRouter returned non-JSON response: {response.text}")
            # Handle API error payload
            if isinstance(data, dict) and "error" in data:
                err = data.get("error", {})
                code = err.get("code", None)
                msg = err.get("message", "Unknown error")
                # Retry on server error codes
                if attempt < max_retries - 1 and code and code >= 500:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"OpenRouter API error {code}: {msg}")
            # Successful data, exit retry loop
            break
        # Parse response for different provider formats
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        # Fallback for providers using 'results' key
        if "results" in data and isinstance(data["results"], list) and data["results"]:
            first = data["results"][0]
            if "message" in first and "content" in first["message"]:
                return first["message"]["content"]
            if "data" in first:
                return first["data"]
        # Fallback for 'result' key
        if "result" in data:
            return data["result"]
        raise RuntimeError(f"Unrecognized response format from OpenRouter: {data}")
