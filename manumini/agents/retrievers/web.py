from __future__ import annotations
from manumini.llm import LLM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from manumini.log import agentic_log

COMMON_WORDS = ["you","the","of","do","known","is","what","are","has","have"]

class WebRetriever:
    SYSTEM_SEARCH = "You are a wise advisor, you must know everything before taking a decision. \
    You must answer with words extracted from the user request only."
    RESEARCH_URL = 'https://duckduckgo.com/?ia=web&origin=funnel_home_google&t=h_&q={research}'

    def __init__(self, model : str) -> WebRetriever:
        self.model = model
        # self.parser = parser

    def IsRequired(self,prompt : str) -> str:
        pass

    def RetriveFromPrompt(self,prompt : str, verbose = False) -> str:
        if verbose:
            agentic_log("initiating a web search")
        rich_prompt = f"Extract the specific keywords from the following text: \
        ```plaintext\n{prompt}\n```\n"

        research = ""
        for _ in range(5):
            with LLM.send(self.model,rich_prompt,WebRetriever.SYSTEM_SEARCH,False) as response:
                research += f"{response.json().get("response","")} "
        
        url = WebRetriever.RESEARCH_URL.format(research=research.replace(" ","+"))

        driver = webdriver.Chrome()
        driver.get(url)
        result = driver.find_elements(By.XPATH, '//li[@data-layout="organic"]')[0]
        title = result.find_element(By.XPATH,'//h2').text
        result.click()
        if verbose:
            agentic_log(f"checking '{title}'")
        data = driver.find_element(By.XPATH,"//body").text
        driver.quit()
        return data