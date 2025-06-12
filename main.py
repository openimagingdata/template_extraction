import os, sys
import pathlib

from dotenv import load_dotenv
import pydantic_ai
import pydantic
from pydantic_ai.models.openai import OpenAIModel
from pathlib import Path

TEMPLATES_DIR = pathlib.Path(__file__).parent / "templates"
model = OpenAIModel("gpt-4o-mini")

class ResponseModel(pydantic.BaseModel):
    "for structured output of response on clinical txt report with metadata"
    response: str
    clinical_indication: str
    # previous_info_exists: bool
    follow_up_required: bool
    impression: str = pydantic.Field(description="clinical report impression")
    patient_personal_info: str = pydantic.Field(serialization_alias="patient") #should be used to anonymize patient identifiers ideally

def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    


    agent = pydantic_ai.Agent(
        model=model,
        output_type= ResponseModel, #determines tructured output of response
        # deps_type=None, #this would ideally be for the input sturctuing, unique to pydanticAI
        system_prompt="""You are a helpful assistant to a radiologist. Answer the user's questions and do it in a structured response as indicated.""", #dont feed txt file here, just basic instructions
    )

    with open(os.path.join(TEMPLATES_DIR, "AAST Kidney Injury Grade.txt"), 'r') as f:
        txt_info = f.read()
        response = agent.run_sync(f"Extract relevant info from this text {txt_info}?")
    print(response.output)
    print(response.output.model_dump_json(by_alias=True, indent=2))
    # print(response.all_messages())
    # print(response.usage())

    response2 = agent.run_sync(
        user_prompt= "what was my previous question?",
        message_history= response.new_messages(),
    )
    print(response2.output)
if __name__ == "__main__":
    main()
