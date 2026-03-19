from __future__ import annotations
from manumini.llm import LLM
from pathlib import Path
from manumini.log import agentic_log


class FileRetriever:
    BANNED_PATHS = set([".","..","","__pycache__",".git"])
    SYSTEM_SEARCH = "You are a wise advisor, you must know everything before taking a decision. \
    You must answer with words extracted from the user request only."

    def __init__(self, model : str) -> FileRetriever:
        self.model = model

    def IsRequired(self,prompt : str) -> str:
        pass

    def RetriveFromPrompt(self,prompt : str, verbose = False) -> str:
        if verbose:
            agentic_log("identifying the files involved")
        rich_prompt = f"Name the specific files or directories you need to know the content of, to poursue this request: \
        ```plaintext\n{prompt}\n```\nAnswer with the name of the exact raw filenames only."

        path_candidates = []
        for _ in range(20):
            with LLM.send(self.model,rich_prompt,FileRetriever.SYSTEM_SEARCH,False) as response:
                text = response.json().get("response","")
                path_candidates += text.replace(",","").replace("`","").replace("'","").replace('"',"").split(" ")

        paths = []
        for path in path_candidates:
            if path == "":
                continue
            path = Path(path)
            if path.exists():
                if path not in paths:
                    paths.append(path)

        files = set([])
        for path in paths:
            path = Path(path)
            if path.is_dir():
                    glob = path.glob("**/*")
                    files.update([file for file in glob if file.is_file()])

        data = ""
        for file in files:
            if set(file.parts).isdisjoint(FileRetriever.BANNED_PATHS):
                agentic_log(f"reading '{file.relative_to('')}'")
                with file.open("r") as f:
                    content = f.read()
                data += f"{file.relative_to('')} :```{file.suffix}\n{content}```\n"

        return data if len(files) else None