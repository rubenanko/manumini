import subprocess
from typing import Tuple

# def bash(command: str)->Tuple[int,str]:
#     pipe = os.popen(command,"r")
#     buffer = pipe._stream.read()
#     return_code = pipe.close()

#     return return_code,buffer

def bash(command: str) ->Tuple[int,str]:
    # Run the command and capture both streams as text strings
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    return result.returncode,result.stdout + result.stderr