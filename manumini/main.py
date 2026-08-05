from manumini.llm import LLM
import argparse
from manumini.agents.retrievers.web import WebRetriever
from manumini.agents.retrievers.file import FileRetriever
from manumini.agents.boolean import ( needs_planning, 
                                      is_global_task_done, 
                                      is_current_task_done, 
                                      is_task_relevant,
                                      needs_bash,
                                      needs_user_feedback)
from manumini.agents.plan import build_plan
from manumini.log import agentic_log
from manumini.tool_caller import bash
from manumini.agents.bash import build_bash_command

import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt",type=str)
    args = parser.parse_args(sys.argv[1:])

    # MODEL = "gemma4:e2b"
    MODEL = "mistral-small-latest"
    SYSTEM = """You are a helpful assistant. Give minimal answers. The least you talk the better. 
    You will be prompted with the result of your work and must explain it briefly.
    The user is not stupid, you don't have to be give very specific questions unless prompted.
    """
    MEMORY = f"The global user request is : {args.prompt}\n Here follows the historical context of your actions"

    tasks = [args.prompt]
    root_task = True

    while len(tasks):
        task = tasks[0]

        if task.lower() == "terminate" and not is_global_task_done(MODEL,MEMORY):
            break

        prompt = f"{MEMORY}, currently doing the subtask : {task}"

        if not root_task and not is_task_relevant(MODEL,prompt):
            tasks = tasks[1:]
            if not len(tasks) and not is_global_task_done(MODEL,MEMORY):
                tasks = build_plan(MODEL,MEMORY)
            continue

        agentic_log(task)
        
        atomic_task = not needs_planning(MODEL,prompt)
        
        if not atomic_task:
            new_tasks = build_plan(MODEL,prompt)

            if len(new_tasks) == 1:
                atomic_task = True

            tasks = new_tasks + tasks[1:]
            # new_tasks_as_string= "\n-".join(new_tasks)
            # prompt = f"{MEMORY}, you just broke this task : {task} into {len(new_tasks)} subtasks : {new_tasks_as_string}"
        
        if atomic_task:
            if not needs_user_feedback(MODEL,prompt):
                command = build_bash_command(MODEL,prompt)

                ret_code,output = bash(command)

                summary = f"purpose:\n```\n{task}\n```\ncommand:\n```\n{command}\n```\n\noutput:\n```\n{output}\n```\n\nreturn code: {ret_code}"
                # prompt = f"{MEMORY}\nYou tried to resolve the subtask : {task} \nwith this action :\n{summary}"
                MEMORY = f"{MEMORY}\n{summary}"

                if is_current_task_done(MODEL,summary):
                    tasks = tasks[1:]
                else:
                    tasks = build_plan(MODEL,f"{MEMORY}\nThe previous attempt of this task failed : {task}\nFind a solution to pursue this task.") + tasks[1:]

            else:
                with LLM.send(MODEL,f"{prompt}\nIf you can't follow the request, don't talk to the user but explain what you need to do as an inner though",SYSTEM,True) as response:
                    # MEMORY = f"{MEMORY}\nYou previously explained to the user:{LLM.printResponseStream(response)}"
                    LLM.printResponseStream(response)

                tasks = tasks[1:]
            
            if not len(tasks) and not is_global_task_done(MODEL,MEMORY):
                tasks = build_plan(MODEL,MEMORY)

        root_task = False
        print(MEMORY)

if __name__ == "__main__":
    main()
    # MODEL = "ministral-3b-latest"
    # with LLM.send(MODEL,"Hello !","You are a helpful assistant",False) as response:
    #     print(response.choices[0].message.content)
    #     LLM.printResponseStream(response)