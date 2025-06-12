import os
import pathlib

from dotenv import load_dotenv
import pydantic_ai
from pydantic_ai.models.openai import OpenAIModel
from pathlib import Path

TEMPLATES_DIR = pathlib.Path(__file__).parent / "templates"
model = OpenAIModel("gpt-4o-mini")

def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    agent = pydantic_ai.Agent(
        model=model,
        system_prompt="""You are a helpful assistant. Answer the user's questions to the best of your ability.""",
    )
    response = agent.run_sync("Where did the phrase Hello World come from?")
    print(response.output)
    # print(response.all_messages())
    # print(response.usage())

if __name__ == "__main__":
    main()
