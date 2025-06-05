import os
import pathlib

from dotenv import load_dotenv
import pydantic_ai

TEMPLATES_DIR = pathlib.Path(__file__).parent / "templates"

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
