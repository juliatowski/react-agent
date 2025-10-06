import json
import requests

class LLMClient:

    def __init__(self, model: str, host: str = "http://localhost:11434"):
        self.model = model
        self.host = host

    def chat(self, prompt: str) -> str:
        """
        Sending a prompt to Ollama and collect the streaming response into one string, 
        so chunks are being processed as they arrive (better for handling large output)
        """
        with requests.post(
            f"{self.host}/api/generate",
            json={"model": self.model, "prompt": prompt},
            stream=True,
            timeout=120,
        ) as r:
            r.raise_for_status()
            output = ""
            for line in r.iter_lines():
                if not line:
                    continue
                data = json.loads(line.decode("utf-8"))
                output += data.get("response", "")
                if data.get("done", False):
                    break
            return output.strip()
