from __future__ import annotations
from manumini.llm import LLM
from selenium import webdriver
import time

COMMON_WORDS = ["you","the","of","do","known","is","what","are","has","have"]

class Retriever:
    SYSTEM = "You are a wise advisor, you must know everything before taking a decision. \
    You must answer with words extracted from the user request only."

    def __init__(self, model : str) -> Retriever:
        self.model = model
        # self.parser = parser

    def RetriveFromPrompt(self,prompt : str) -> str:
        rich_prompt = f"Extract the specific keywords from the following text: \
        ```plaintext\n{prompt}\n```\n"

        research = ""
        for i in range(5):
            with LLM.send(self.model,rich_prompt,Retriever.SYSTEM,True) as response:
                research += LLM.printResponseStream(response)
        
        url = f'https://duckduckgo.com/?ia=web&origin=funnel_home_google&t=h_&q="{research.replace(" ","+")}"'

        driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
        result = driver.get(url)
        print(dir())
        driver.quit()