import os
import pathlib

from dotenv import load_dotenv
import pydantic_ai
import pydantic
from pydantic_ai.models.openai import OpenAIModel
from pathlib import Path

TEMPLATES_DIR = pathlib.Path(__file__).parent / "templates"
model = OpenAIModel("gpt-4o-mini")

class ResponseModel(pydantic_ai.BaseModel):
    "for structured output of response with metadata"
    response: str
    clinical_indication: str
    previous_info_exists: bool
    follow_up_required: bool
    impression: str = pydantic.Field(description="clinical report impression")
def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    


    agent = pydantic_ai.Agent(
        model=model,
        output_type= ResponseModel,
        system_prompt="""You are a helpful assistant to a radiologist. Answer the user's questions given txt file info you are provided in a structured response.""",
    )
    response = agent.run_sync("Where did the phrase Hello World come from?")
    print(response.output)
    # print(response.all_messages())
    # print(response.usage())

    response2 = agent.run_sync(
        user_prompt= "what was my previous question?",
        message_history= response.new_messages(),
    )
    print(response2.output)
if __name__ == "__main__":
    main()
