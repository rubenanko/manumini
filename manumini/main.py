from manumini.llm import LLM
import argparse
import json
from manumini.agents.retriever import Retriever
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt",type=str)
    args = parser.parse_args(sys.argv[1:])

    MODEL = "qwen2.5-coder:1.5b"
    
    retriever = Retriever(MODEL)
    retriever.RetriveFromPrompt(args.prompt)
            


if __name__ == "__main__":
    main()