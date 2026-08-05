from typing import List
from re import sub

from manumini.llm import LLM
from manumini.log import agentic_log

SYSTEM = """
You must answer with a plan to perform the current task. 
Take into account the logs of the past tasks.
Each step of the plan must be prefixed with it index number in the chronological order. 
Each step must be written on one line only.
Only answer with the step list.
Steps must simple, and very concrete actions.
They must be either : 
    - the goal of bash command, not the command yet but what it tries to achieve. Don't invoke specific tools name. Specfic targeted actions.
    - feedback to give to the user. Requested format : "Give feedback to the user about ..."
A step CANNOT be about analyzing things, it must be a command synopsis or a feedback to user.
Prefer many concrete short steps than a few long abstract steps.
If the global target task seems to be done regarding logs of the past tasks, just answer with "terminate".
Strict constraints over response format.
"""

def build_plan(model : str, prompt : str,verbose : bool = True) ->List[str]:
    rich_prompt = prompt
    # with LLM.send(model,rich_prompt,SYSTEM,False) as response:
        # text = response.json().get("response","").lower()
    response = LLM.send(model,rich_prompt,SYSTEM,False)
    text = response.choices[0].message.content.lower()
            # print(text)

    tasks = [sub(r"^\d+.\s+","",task,count=0) for task in text.split("\n")]

    # if verbose:
    #     agentic_log(f"Identified {len(tasks)} subtasks")

    return tasks