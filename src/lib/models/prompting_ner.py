import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils.select_enviroment import select_enviroment

select_enviroment("default")

from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from langchain_core.pydantic_v1 import BaseModel, Field

# from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate

empty_result = {
    "adverse_drug_reactions": [],
    "diseases_or_medical_conditions": [],
    "medications": [],
    "clinical_findings": [],
    "symptoms_experienced_by_patients": [],
}


# Define models for each entity type
class AdverseDrugReaction(BaseModel):
    name: str
    start_position: int
    end_position: int


class DiseaseOrMedicalCondition(BaseModel):
    name: str
    start_position: int
    end_position: int


class Medication(BaseModel):
    name: str
    start_position: int
    end_position: int


class ClinicalFinding(BaseModel):
    name: str
    start_position: int
    end_position: int


class SymptomExperiencedByPatient(BaseModel):
    name: str
    start_position: int
    end_position: int


# Define the Pydantic model for structured output
class MedicalNEROutput(BaseModel):
    adverse_drug_reactions: Optional[List[AdverseDrugReaction]] = Field(
        ...,
        description="List of tuples with adverse drug reaction name, start position, and end position",
    )
    diseases_or_medical_conditions: Optional[List[DiseaseOrMedicalCondition]] = Field(
        ...,
        description="List of tuples with disease or medical condition name, start position, and end position",
    )
    medications: Optional[List[Medication]] = Field(
        ...,
        description="List of tuples with medication name, start position, and end position",
    )
    clinical_findings: Optional[List[ClinicalFinding]] = Field(
        ...,
        description="List of tuples with clinical finding name, start position, and end position",
    )
    symptoms_experienced_by_patients: Optional[List[SymptomExperiencedByPatient]] = (
        Field(
            ...,
            description="List of tuples with symptom experienced by patient name, start position, and end position",
        )
    )


def get_prompt():
    template = """
    "messages": [
        {{
            "role": "system",
            "content": "Given a medical related string, provide the following fields in a JSON dict, where applicable: 'adverse_drug_reactions' (list of tuples with adverse drug reaction name, start position, and end position), 'diseases_or_medical_conditions' (list of tuples with disease or medical condition name, start position, and end position), 'medications' (list of tuples with medication name, start position, and end position), 'clinical_findings' (list of tuples with clinical finding name, start position, and end position), 'symptoms_experienced_by_patients' (list of tuples with symptom experienced by patient name, start position, and end position). 

            Do not confuse 'symptoms_experienced_by_patients' with 'adverse_drug_reactions'. For example, do not do the following:

            Expected output sample 1: {{'adverse_drug_reactions': {{'adverse_drug_reactions': [{{'name': 'Nagging muscle pain', 'start_position': 0, 'end_position': 19}}, {{'name': 'persistent fatigue', 'start_position': 63, 'end_position': 81}}, {{'name': 'moderate insomnia', 'start_position': 83, 'end_position': 100}}, {{'name': 'unable to focus', 'start_position': 115, 'end_position': 130}}], 'diseases_or_medical_conditions': [], 'medications': [], 'clinical_findings': [], 'symptoms_experienced_by_patients': []}}
            Output sample 1: {{'adverse_drug_reactions': [], 'diseases_or_medical_conditions': [], 'medications': [], 'clinical_findings': [], 'symptoms_experienced_by_patients': [{{'name': 'Nagging muscle pain', 'start_position': 0, 'end_position': 19}}, {{'name': 'persistent fatigue', 'start_position': 63, 'end_position': 81}}, {{'name': 'moderate insomnia', 'start_position': 83, 'end_position': 100}}, {{'name': 'unable to focus or stay', 'start_position': 115, 'end_position': 130}}]}}

            In general, entities are 'adverse_drug_reactions' rather than 'symptoms_experienced_by_patients'. But it DEPENDS ON THE CONTEXT OF THE SENTENCE. An example to ilustrate the difference and importance of the context is: {{"role": "user", "content": "It helps relieve chronic pain but over time, causes intestinal pain and bleeding.\nI had symptoms similar to diverticulitis: blood in stool, pain.\nI would be cautious about paying attention to cramping, intestinal/stomach pain which can lead to very serious conditions.\n"}}, {{"role": "assistant", "content": "{{'adverse_drug_reactions': [('intestinal pain', 52, 67), ('bleeding', 72, 80), ('blood in stool', 124, 138), ('pain', 140, 144), ('intestinal/stomach pain', 202, 225), ('cramping', 192, 200)], 'diseases_or_medical_conditions': [('diverticulitis', 108, 122)], 'medications': [], 'clinical_findings': [], 'symptoms_experienced_by_patients': [('chronic pain', 17, 29)]}}"}}
            
            Additionally, ensure that an entity is not classified in more than one category. For example:

            Expected output sample 0: {{'adverse_drug_reactions': [('dry mouth', 0, 19)], 'diseases_or_medical_conditions': [], 'medications': [], 'clinical_findings': [], 'symptoms_experienced_by_patients': []}}
            Output sample 0: {{'adverse_drug_reactions': [{{'name': 'dry mouth', 'start_position': 9, 'end_position': 18}}], 'diseases_or_medical_conditions': [], 'medications': [], 'clinical_findings': [], 'symptoms_experienced_by_patients': [{{'name': 'dry mouth', 'start_position': 9, 'end_position': 18}}]}}

            Avoid these errors when providing the categorized entities."
        }},
        {{"role": "user", "content": "{text}"}}
    ]
    """
    prompt = PromptTemplate(
        input_variables=["text"],
        template=template,
    )
    return prompt


def apply_ner_to_text_openai(text, model_id):
    try:
        llm = ChatOpenAI(model_name=model_id)
        prompt = get_prompt()
        structured_llm = llm.with_structured_output(MedicalNEROutput, include_raw=True)

        sequence = prompt | structured_llm
        response = sequence.invoke({"text": text})
        structured_response = response["raw"].additional_kwargs["tool_calls"][0][
            "function"
        ]["arguments"]
        return structured_response
    except Exception as e:
        print(f"Error apply_ner_to_text_gpt_4o(): {e}")
        return empty_result


def apply_ner_to_text_anthropic(text, model_id):
    try:
        llm = ChatAnthropic(model=model_id)
        prompt = get_prompt()
        structured_llm = llm.with_structured_output(MedicalNEROutput, include_raw=True)

        sequence = prompt | structured_llm
        response = sequence.invoke({"text": text})
        structured_response = response["raw"].content[0]["input"]
        return structured_response
    except Exception as e:
        print(f"Error apply_ner_to_text_sonnet_35(): {e}")
        return empty_result


"""
# Example usage
text = "Hunger pangs.\nBrilliant, I have a new lease of life, I walk up & down steps properly, no longer sideways like a toddler, hip pain has gone other than if I jar it.\n"
response_gpt_4o = apply_ner_to_text_gpt_4o(text)
response_sonnet_35 = apply_ner_to_text_sonnet_35(text)

print(response_gpt_4o)
print(response_sonnet_35)
"""
