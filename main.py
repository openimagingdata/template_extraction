import os
import pathlib

from dotenv import load_dotenv
import pydantic_ai
from pathlib import Path

def read_in_txt(txtfile):
    health_file = Path(txtfile) #fill in text file
    contents =  health_file.read_txt()
    return contents
def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    agent = pydantic_ai.Agent(
        "openai:gpt4o-mini",
        system_prompt="""You are a helpful assistant. Answer the user's questions to the best of your ability.""",
    )

if __name__ == "__main__":
    main()
