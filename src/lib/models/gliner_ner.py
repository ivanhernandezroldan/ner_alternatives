from gliner import GLiNER


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


def apply_ner_to_text(text):
    entities = model.predict_entities(text, LABELS, threshold=0.5)
    ner_text = ""
    for entity in entities:
        ner_text += f"{entity['text']} => {entity['label']}\n"
    return ner_text
