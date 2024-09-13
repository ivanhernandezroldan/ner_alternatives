import os
import sys

import streamlit as st
import concurrent.futures

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from lib.models.fine_tuning_ner import apply_ner_to_text_fine_tuned
from lib.models.prompting_ner import (
    apply_ner_to_text_openai,
    apply_ner_to_text_anthropic,
)
from lib.models.gliner_ner import apply_ner_to_text_gliner

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
results = {
    "fine_tuned_gpt_4o_v2": "",
    "fine_tuned_gpt_4o": "",
    "gpt_4o": "",
    "fine_tuned_gpt_4o_mini_v2": "",
    "fine_tuned_gpt_4o_mini": "",
    "gpt_4o_mini": "",
    "sonnet_35": "",
    "gliner": "",
}


# Crear un contenedor vacío para el mensaje de ejecución
message_placeholder = st.empty()


# Función para procesar NER con diferentes métodos
def process_ner(method, input_text):
    if method == "fine_tuned_gpt_4o_v2":
        return apply_ner_to_text_fine_tuned(
            input_text, "ft:gpt-4o-2024-08-06:personal:1000-sample-gpt-4o:A3S2iooJ"
        )
    elif method == "fine_tuned_gpt_4o":
        return apply_ner_to_text_fine_tuned(
            input_text, "ft:gpt-4o-2024-08-06:personal:150-sample-gpt-4o:A34xm7HX"
        )
    elif method == "gpt_4o":
        return apply_ner_to_text_openai(input_text, "gpt-4o-2024-08-06")
    elif method == "fine_tuned_gpt_4o_mini_v2":
        return apply_ner_to_text_fine_tuned(
            input_text,
            "ft:gpt-4o-mini-2024-07-18:personal:1000-sample-gpt-4o-mini:A3sZemiq",
        )
    elif method == "fine_tuned_gpt_4o_mini":
        return apply_ner_to_text_fine_tuned(
            input_text,
            "ft:gpt-4o-mini-2024-07-18:personal:100-sample-gpt-4o-mini:A34sYctP",
        )
    elif method == "gpt_4o_mini":
        return apply_ner_to_text_openai(input_text, "gpt-4o-mini")
    elif method == "sonnet_35":
        return apply_ner_to_text_anthropic(input_text, "claude-3-5-sonnet-20240620")
    elif method == "gliner":
        return apply_ner_to_text_gliner(input_text, None)


# Lista de métodos
methods = [
    "fine_tuned_gpt_4o_v2",
    "fine_tuned_gpt_4o",
    "gpt_4o",
    "fine_tuned_gpt_4o_mini_v2",
    "fine_tuned_gpt_4o_mini",
    "gpt_4o_mini",
    "sonnet_35",
    "gliner",
]


if st.button("Execute"):
    # Mostrar el mensaje de ejecución
    message_placeholder = st.empty()
    message_placeholder.text("Ejecutando NER en las alternativas...")

    # Ejecutar las funciones en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Enviar cada tarea al pool de threads
        future_to_method = {
            executor.submit(process_ner, method, input_text): method
            for method in methods
        }

        # Recoger los resultados a medida que estén disponibles
        for future in concurrent.futures.as_completed(future_to_method):
            method = future_to_method[future]
            try:
                result = future.result()
                results[method] = result
            except Exception as e:
                results[method] = f"Error: {e}"

    # Borrar el mensaje después de la ejecución
    message_placeholder.empty()


col1, col2, col3 = st.columns(3)

with col1:
    st.header("Fine-tuned GPT-4o Large")
    st.text_area(
        "",
        value=results["fine_tuned_gpt_4o_v2"],
        height=150,
        key="fine_tuned_gpt_4o_v2",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )

with col2:
    st.header("Fine-tuned GPT-4o Small")
    st.text_area(
        "",
        value=results["fine_tuned_gpt_4o"],
        height=150,
        key="fine_tuned_gpt_4o",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )

with col3:
    st.header("GPT-4o")
    st.text_area(
        "",
        value=results["gpt_4o"],
        height=150,
        key="gpt_4o",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.header("Fine-tuned GPT-4o Mini Large")
    st.text_area(
        "",
        value=results["fine_tuned_gpt_4o_mini_v2"],
        height=150,
        key="fine_tuned_gpt_4o_mini_v2",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )

with col5:
    st.header("Fine-tuned GPT-4o Mini Small")
    st.text_area(
        "",
        value=results["fine_tuned_gpt_4o_mini"],
        height=150,
        key="fine_tuned_gpt_4o_mini",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )

with col6:
    st.header("GPT-4o Mini")
    st.text_area(
        "",
        value=results["gpt_4o_mini"],
        height=150,
        key="gpt_4o_mini",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )

col7, col8 = st.columns(2)


with col7:
    st.header("Sonnet 3.5")
    st.text_area(
        "",
        value=results["sonnet_35"],
        height=150,
        key="sonnet_35",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )

with col8:
    st.header("GLiNER")
    st.text_area(
        "",
        value=results["gliner"],
        height=150,
        key="gliner",
        disabled=True,  # Bloquear el área de texto para que sea solo lectura
    )

# streamlit run src/app/app.py
