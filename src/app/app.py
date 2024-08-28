import os
import sys

import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from lib.models.prompting_ner import apply_ner_to_text as apply_prompting_ner_to_text
from lib.models.fine_tuning_ner import (
    apply_ner_to_text as apply_fine_tuning_ner_to_text,
)
from lib.models.gliner_ner import apply_ner_to_text as apply_gliner_ner_to_text

# Inyectar CSS para cambiar el estilo del texto en las áreas de texto

# Título de la aplicación
st.title("NER ALTERNATIVES")

# Descripción de la tarea NER
st.markdown(
    """
    Enter the text you want to analyze. This text will be processed using different
    Named Entity Recognition (NER) techniques to identify the following entities:
    - **ADR**: Adverse drug reactions.
    - **Disease**: Diseases or medical conditions.
    - **Drug**: Medications.
    - **Finding**: Clinical findings.
    - **Symptom**: Symptoms experienced by patients.
    """
)

# Input text box principal
input_text = st.text_area("", placeholder="Enter text here...", height=150)

# Variables para almacenar el texto modificado
modified_text_prompting = ""
modified_text_fine_tuning = ""
modified_text_gliner = ""

# Crear un contenedor vacío para el mensaje de ejecución
message_placeholder = st.empty()

# Botón de ejecución
if st.button("Execute"):
    # Mostrar el mensaje de ejecución
    message_placeholder.text("Ejecutando NER en las alternativas...")

    # Procesar el texto con los diferentes métodos de NER
    modified_text_prompting = apply_prompting_ner_to_text(input_text)
    modified_text_fine_tuning = apply_fine_tuning_ner_to_text(input_text)
    modified_text_gliner = apply_gliner_ner_to_text(input_text)

    # Borrar el mensaje después de la ejecución
    message_placeholder.empty()

# Tres columnas para las diferentes alternativas de NER
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Prompting")
    st.text_area(
        "",
        value=modified_text_prompting,
        height=150,
        key="prompting_input",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )

with col2:
    st.header("Fine-tuning")
    st.text_area(
        "",
        value=modified_text_fine_tuning,
        height=150,
        key="fine_tuning_input",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )

with col3:
    st.header("GLiNER")
    st.text_area(
        "",
        value=modified_text_gliner,
        height=150,
        key="gliner_input",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )
