from typing import List
from re import sub

from manumini.llm import LLM
from manumini.log import agentic_log

SYSTEM = """
You must only answer with bash commands to execute the selected task. Nothing else is accepted. Strict constraint.
# **available** programs

## find
to list all files recursively.
usage: 
```
find . -type f
```

## grep
to search for a string in a file

## cat
to read file
usage:  
```
cat <real_path_to_file>
```

## echo
to write in stdout or in a file

# unavailable tools to avoid
    - list, list is not installed.
    - ls, is deprecated as it is not recursive

"""

def build_bash_command(model : str, prompt : str,verbose : bool = True) ->List[str]:
    rich_prompt = prompt
    # with LLM.send(model,rich_prompt,SYSTEM,False) as response:
        #text = response.json().get("response","").lower()
    response = LLM.send(model,rich_prompt,SYSTEM,False)
    text = response.choices[0].message.content.lower()
    
    text = sub("^```bash","",text)
    text = sub("^```","",text)
    text = sub("```$","",text)

    if verbose:
        agentic_log(f"Bash `{text}`")
        
    return text