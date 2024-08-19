import os


TEXTS_DIR = os.path.join(os.getcwd(), "..", "ner_dataset", "text")


def filter_annotations(input_string):
    # Dividir el string en líneas individuales
    lines = input_string.strip().split("\n")

    # Filtrar solo las líneas que comienzan con 'T' seguidas de un número
    result_lines = []
    for line in lines:
        if line.startswith("T") and "AnnotatorNotes" not in line:
            # Remover el prefijo (T1, T2, etc.)
            parts = line.split("\t", 1)
            if len(parts) > 1:
                result_lines.append(parts[1])

    # Unir las líneas filtradas en un solo string
    return "\n".join(result_lines)
