from gliner import GLiNER
from tenacity import retry, stop_after_attempt, wait_exponential


# Initialize GLiNER
def initialize_gliner():
    return GLiNER.from_pretrained("urchade/gliner_multiv2.1")


model = initialize_gliner()

# Labels for entity prediction
LABELS = [
    "Adverse drug reactions",
    "Diseases or medical conditions",
    "Medications",
    "Clinical findings",
    "Symptoms experienced by patients",
]

empty_result = {
    "adverse_drug_reactions": [],
    "diseases_or_medical_conditions": [],
    "medications": [],
    "clinical_findings": [],
    "symptoms_experienced_by_patients": [],
}


def transform_to_structured_output(entities):
    # Inicializamos el diccionario estructurado
    structured_output = {
        "adverse_drug_reactions": [],
        "diseases_or_medical_conditions": [],
        "medications": [],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }

    # Mapeo de etiquetas a las claves del diccionario estructurado
    label_to_key = {
        "Adverse drug reactions": "adverse_drug_reactions",
        "Diseases or medical conditions": "diseases_or_medical_conditions",
        "Medications": "medications",
        "Clinical findings": "clinical_findings",
        "Symptoms experienced by patients": "symptoms_experienced_by_patients",
    }

    # Iteramos sobre cada entidad y la agregamos a la clave correspondiente
    for entity in entities:
        key = label_to_key.get(entity["label"])
        if key:
            structured_output[key].append(
                (entity["text"], entity["start"], entity["end"])
            )

    return structured_output


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def apply_ner_to_text_gliner(text, model_id):
    entities = model.predict_entities(text, LABELS, threshold=0.5)
    return transform_to_structured_output(entities)
    print(f"Error apply_ner_to_text_gliner(): {e}")
    return empty_result


"""
# Example usage
text = "Hunger pangs.\nBrilliant, I have a new lease of life, I walk up & down steps properly, no longer sideways like a toddler, hip pain has gone other than if I jar it.\n"
response_gliner = apply_ner_to_text_gliner(text)

print(response_gliner)
"""
