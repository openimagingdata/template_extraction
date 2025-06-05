import os
import pathlib

from dotenv import load_dotenv
import pydantic_ai

def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    print(f"Hello from template-extraction--we have OPENAI_API_KEY set ({OPENAI_API_KEY[0:12]}).")


if __name__ == "__main__":
    main()
