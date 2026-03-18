from __future__ import annotations
from manumini.llm import LLM
import requests

COMMON_WORDS = ["you","the","of","do","known"]

class Retriever:
    SYSTEM = "You are a wise advisor, you must know everything before taking a decision."

    def __init__(self, model : str) -> Retriever:
        self.model = model
        # self.parser = parser

    def RetriveFromPrompt(self,prompt : str) -> str:
        rich_prompt = f"What are the key concepts or proper nouns in the following text: \
        ```plaintext\n{prompt}\n```\n. "

        with LLM.send(self.model,prompt,Retriever.SYSTEM,True) as response:
            assistant_words = LLM.printResponseStream(response).lower()
        
        assistant_words = ''.join(char for char in assistant_words if char.isalnum() or char == " " or char == "\n")
        assistant_words =  assistant_words.split(" ")

        prompt_words = prompt.lower()
        prompt_words = ''.join(char for char in prompt_words if char.isalnum() or char == " " or char == "\n")
        prompt_words = prompt_words.split(" ")
        
        keywords = {}
        for word in prompt_words:
            if word in COMMON_WORDS:
                continue
            if word in assistant_words:
                if word in keywords:
                    keywords[word] += 1
                else:
                    keywords[word] = 1

        print(keywords)
        


        # url = f'https://www.google.com/search?q="{keywords.replace(" ","+")}"'