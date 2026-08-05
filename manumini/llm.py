from __future__ import annotations
import requests
import json
import os
from mistralai.client import Mistral
import time

class LLM:
    # SESSION = requests.Session()
    DEFAULT_URL = "http://localhost:11434/api/generate"
    DEFAULT_SYSTEM = "You are a helpful assistant"
    CLIENT = Mistral(api_key=os.getenv("MANUMINI_API_KEY",None))

    def __init__(self, system : str, url: str = DEFAULT_URL) -> LLM:
        self.system = system

        # if API_KEY != None:
        #     SESSION.headers.update({
        #         "Authorization": f"Bearer {API_KEY}"
        #     })


    # @staticmethod
    # def payload(model : str,prompt : str,system : str,stream: bool):
    #     return {
    #         "model": model,
    #         "prompt": prompt,
    #         "system": system,
    #         "stream": stream,
    #         "think": False,
    #         "keep_alive": "5m",
    #         "options": {
    #             "repeat_penalty": 1.2,
    #             "repeat_last_n": 128,
    #         }
    #     }


    @staticmethod
    def send(model: str, prompt: str, system: str = None,  stream : bool = False,url: str = DEFAULT_URL) -> requests.Response:
        # payload = LLM.payload(model,prompt,system,stream)
        # return LLM.SESSION.post(url, json=payload, stream=stream)
        time.sleep(1)
        if stream:
            return LLM.CLIENT.chat.stream(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ]
            )
        else:
            return LLM.CLIENT.chat.complete(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ]
            )

    # @staticmethod
    # def printResponseStream(response : requests.Response) -> str:
    #     print("\x1b[0;34mManumini : \x1b[0;0m",end="",flush=True)
    #     text = ""
    #     for line in response.iter_lines():
    #         if line:
    #             data = json.loads(line)
    #             chunk = data.get("response", "")
    #             text += chunk
    #             print(chunk,end="",flush=True)
    #     print("")
    #     return text

    @staticmethod
    def printResponseStream(response) -> str:
        print("\x1b[0;34mManumini : \x1b[0;0m",end="",flush=True)
        text = ""
        for chunk in response:
            token = chunk.data.choices[0].delta.content
            if token:   print(token,end="",flush=True)
        print("")
        return text

        