from manumini.llm import LLM
import argparse
from manumini.agents.retrievers.web import WebRetriever
from manumini.agents.retrievers.file import FileRetriever
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt",type=str)
    args = parser.parse_args(sys.argv[1:])

    MODEL = "qwen2.5-coder:1.5b"
    SYSTEM = "You are a helpful assistant. Give minimal answers. The least you talk the better"
    
    retriever = FileRetriever(MODEL)
    file_search_data = retriever.RetriveFromPrompt(args.prompt,True)
    if file_search_data == None:
        print("Could not locate any files")
        exit()
    prompt = f"Answer according to the following data : {file_search_data}\n{args.prompt}."
    with LLM.send(MODEL,prompt,SYSTEM,True) as response:
        LLM.printResponseStream(response)
            


if __name__ == "__main__":
    main()