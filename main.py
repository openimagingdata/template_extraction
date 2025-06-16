import asyncio
import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
import pydantic_ai
from pydantic import BaseModel, Field, field_validator
from pydantic_ai.models.openai import OpenAIModel


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
TEMPLATES_DIR = Path(__file__).parent / "templates"
model = OpenAIModel("gpt-4o-mini")

class ResponseModel(BaseModel):
    "for structured output of response on clinical txt report with metadata"
    response: str
    clinical_indication: str
    # previous_info_exists: bool
    follow_up_required: bool
    impression: str = Field(description="clinical report impression")
    patient_personal_info: str = Field(serialization_alias="patient") #should be used to anonymize patient identifiers ideally

class FindingAttribute(BaseModel):
    name: str = Field(description="Name of the attribute")
    value_type: Literal["numeric", "choice"] = Field(description="Type of the attribute, whether a numeric value or a choice from a predefined set")
    unit: str | None = Field(default=None, description="Unit of the attribute, if applicable")
    choices: list[str] | None = Field(default=None, description="List of choices for the attribute, if applicable; must have more than one choice if provided")

    # Confirm that the choices list has more than one choice if it is provided
    @field_validator("choices")
    def validate_choices(cls, v, values):
        if v is not None and len(v) < 2:
            raise ValueError("choices must have more than one choice if provided")
        return v

class FindingDescription(BaseModel):
    name: str = Field(description="Name of the finding")
    synonyms: list[str] = Field(description="List of synonyms for the finding")
    description: str = Field(description="Brief summary of what the finding is is")
    attributes: list[FindingAttribute] = Field(description="List of attributes that might be used to characterize the finding")

SYSTEM_PROMPT = """
You are a medical informatics expert tasked with identifying and standardizing clinical findings from
the text of a clinical radiologist report.
"""

INSTRUCTIONS = """
Your goal is to identify the findings in the template report that's being provided to you and create
a structured description of each individual finding using the provided schema.

Please also provide additional information about the findings, including relevant attributes, synonyms,
and a brief description of each finding, even if those are not explicitly mentioned in the report.

The findings should be described in a way that is consistent with the provided schema, and you should
ensure that the attributes are well-defined and relevant to the findings. Any descriptions should be concise,
no more than two sentences.
"""

async def main(filename: str = "ABD_PEL CT.txt"):
    
    agent = pydantic_ai.Agent(
        model=model,
        output_type= list[FindingDescription], #determines tructured output of response
        system_prompt=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        retries=3
    )

    template = (TEMPLATES_DIR / filename).read_text()
    # Wrap the run call in a tqdm spinner
    response = await agent.run(template)
    if (findings := response.output):
        print(f"Found {len(findings)} findings:")
        for finding in findings:
            print(finding.model_dump_json(indent=2, exclude_none=True))

if __name__ == "__main__":

    asyncio.run(main())
    
