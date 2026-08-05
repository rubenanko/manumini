from manumini.llm import LLM

SYSTEM = """
    You must only answer with true or false. Nothing else is accepted. Strict constraint.
"""


def needs_planning(model,prompt : str) -> bool:
    rich_prompt = f'Does the current task is complex and requires additional planning because it should be divided in sub tasks ? Take into account the log of the past tasks : {prompt}'
    # with LLM.send(model,rich_prompt,SYSTEM,False) as response:
        # text = response.json().get("response","").lower()
    response = LLM.send(model,rich_prompt,SYSTEM,False)
    text = response.choices[0].message.content.lower()
    
    return text == "true" or text == "yes"

def needs_bash(model,prompt : str) -> bool:
    rich_prompt = f'Is the current task talking dealing with a command or interaction with the system (bash commands are NOT appropriate for giving user feedback) ? : {prompt}'
    # with LLM.send(model,rich_prompt,SYSTEM,False) as response:
        # text = response.json().get("response","").lower()
    response = LLM.send(model,rich_prompt,SYSTEM,False)
    text = response.choices[0].message.content.lower()
    
    return text == "true" or text == "yes"

def needs_user_feedback(model,prompt : str) -> bool:
    rich_prompt = f'Is the current task explicitly needs talking to the user ? : {prompt}'
    # with LLM.send(model,rich_prompt,SYSTEM,False) as response:
        # text = response.json().get("response","").lower()
    response = LLM.send(model,rich_prompt,SYSTEM,False)
    text = response.choices[0].message.content.lower()

    return text == "true" or text == "yes"

def is_current_task_done(model : str, prompt : str) ->bool:
    rich_prompt = f'Does the command resolves the current task ? : {prompt} '
    # with LLM.send(model,rich_prompt,SYSTEM,False) as response:
        # text = response.json().get("response","").lower()
    response = LLM.send(model,rich_prompt,SYSTEM,False)
    text = response.choices[0].message.content.lower()

    return text == "true" or text == "yes"    

def is_global_task_done(model : str, prompt : str) ->bool:
    rich_prompt = f'Is the global task finished ? : {prompt} '
    # with LLM.send(model,rich_prompt,SYSTEM,False) as response:
        # text = response.json().get("response","").lower()
    response = LLM.send(model,rich_prompt,SYSTEM,False)
    text = response.choices[0].message.content.lower()

    return text == "true" or text == "yes"    

def is_task_relevant(model : str, prompt : str) ->bool:
    rich_prompt = f'Have you already done the current task in the past ? : {prompt} '
    # with LLM.send(model,rich_prompt,SYSTEM,False) as response:
        # text = response.json().get("response","").lower()
    response = LLM.send(model,rich_prompt,SYSTEM,False)
    text = response.choices[0].message.content.lower()
        
    return not (text == "true" or text == "yes")