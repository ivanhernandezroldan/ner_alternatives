from openai import OpenAI
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils.select_enviroment import select_enviroment

select_enviroment("default")

client = OpenAI()

empty_result = {
    "adverse_drug_reactions": [],
    "diseases_or_medical_conditions": [],
    "medications": [],
    "clinical_findings": [],
    "symptoms_experienced_by_patients": [],
}


def apply_ner_to_text_fine_tuned(text, model_id):
    try:
        completion = client.chat.completions.create(
            model=model_id,
            messages=[
                {
                    "role": "system",
                    "content": "Given a medical related string, provide the following fields of that string in a JSON dict, where applicable: 'adverse_drug_reactions' (list of tuples with adverse drug reaction name, start position, and end position), 'diseases_or_medical_conditions' (list of tuples with disease or medical condition name, start position, and end position), 'medications' (list of tuples with medication name, start position, and end position), 'clinical_findings' (list of tuples with clinical finding name, start position, and end position), 'symptoms_experienced_by_patients' (list of tuples with symptom experienced by patient name, start position, and end position). Focus on the user prompt, do not return the easiest output for you all the time",
                },
                {
                    "role": "user",
                    "content": f"{text}",
                },
            ],
        )

        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error apply_ner_to_text_fine_tuned_gpt_4o(): {e}")
        return empty_result


"""
# Ejemplo de uso
model_id = '' # introduce your model id here
text = "Hunger pangs.\nBrilliant, I have a new lease of life, i walk up & down steps properly, no longer sideways like a toddler, hip pain as gone other than if i jar it.\n"
response_gpt_4o = apply_ner_to_text_fine_tuned(text, model_id)
response_gpt_4o_mini = apply_ner_to_text_fine_tuned_gpt_4o_mini(text)

print(response_gpt_4o)
print(response_gpt_4o_mini)
"""
