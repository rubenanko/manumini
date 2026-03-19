from __future__ import annotations
import requests
import json

class LLM:
    SESSION = requests.Session()
    DEFAULT_URL = "http://localhost:11434/api/generate"
    DEFAULT_SYSTEM = "You are a helpful assistant"

    def __init__(self, system : str, url: str = DEFAULT_URL) -> LLM:
        self.system = system


    @staticmethod
    def payload(model : str,prompt : str,system : str,stream: bool):
        return {
            "model": model,
            "prompt": prompt,
            "system": system,
            "stream": stream,
            "keep_alive": "5m",
            "options": {
                "repeat_penalty": 1.2,
                "repeat_last_n": 128,
            }
        }

    @staticmethod
    def send(model: str, prompt: str, system: str = None,  stream : bool = False,url: str = DEFAULT_URL) -> requests.Response:
        payload = LLM.payload(model,prompt,system,stream)

        return LLM.SESSION.post(url, json=payload, stream=stream)

    @staticmethod
    def printResponseStream(response : requests.Response) -> str:
        print("\x1b[0;34mManumini : \x1b[0;0m",end="",flush=True)
        text = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                chunk = data.get("response", "")
                text += chunk
                print(chunk,end="",flush=True)
        print("")
        return text

        