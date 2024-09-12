def get_assistant_content(messages_dict):
    # Buscar el mensaje con el rol "assistant"
    for message in messages_dict["messages"]:
        if message["role"] == "assistant":
            # Extraer y devolver el contenido del asistente
            return message["content"]


def get_user_content(messages_dict):
    # Buscar el mensaje con el rol "user"
    for message in messages_dict["messages"]:
        if message["role"] == "user":
            # Extraer y devolver el contenido del usuario
            return message["content"]


def evaluate_model_output(expected_output, model_output):
    try:
        verif1_pass = True
        verif2_pass = True
        verif3_pass = True
        verif4_pass = True

        # Coleccionar todas las entidades esperadas y predichas independientemente de la categoría
        ref_texts_all = set(
            entity[0]
            for category in expected_output
            for entity in expected_output[category]
        )

        # Recoger todas las entidades predichas, manejando diccionarios y listas/tuplas
        model_texts_all = set(
            entity["name"] if isinstance(entity, dict) else entity[0]
            for category in model_output
            for entity in model_output[category]
        )

        # Verificación 4: Identifica todas las entidades esperadas sin errores
        if ref_texts_all != model_texts_all:
            verif4_pass = False

        if verif4_pass:  # Solo evaluar si verif4_pass no ha fallado aún
            for category in expected_output:
                ref_entities = expected_output[category]

                # Manejo de entidades en el formato de diccionario o tupla
                model_entities = [
                    (
                        (
                            entity["name"],
                            entity["start_position"],
                            entity["end_position"],
                        )
                        if isinstance(entity, dict)
                        else tuple(entity)
                    )
                    for entity in model_output.get(category, [])
                ]

                # Verificación 3: Clasifica correctamente dichas entidades
                if verif3_pass:  # Solo evaluar si verif3_pass no ha fallado aún
                    ref_set = {(entity[0], category) for entity in ref_entities}
                    model_set = {(entity[0], category) for entity in model_entities}
                    if ref_set != model_set:
                        verif3_pass = False
                else:
                    verif2_pass = False
                    verif1_pass = False

                # Verificación 2: Las ubica bien dentro del texto con un margen de error de +-2
                if verif2_pass:  # Solo evaluar si verif2_pass no ha fallado aún
                    for ref_entity in ref_entities:
                        ref_text, ref_start, ref_end = ref_entity
                        matched = False
                        for model_entity in model_entities:
                            model_text, model_start, model_end = model_entity
                            if (
                                ref_text == model_text
                                and abs(ref_start - model_start) <= 2
                                and abs(ref_end - model_end) <= 2
                            ):
                                matched = True
                                break
                        if not matched:
                            verif2_pass = False
                            break
                else:
                    verif1_pass = False

                # Verificación 1: Las ubica bien dentro del texto
                if verif1_pass:  # Solo evaluar si verif1_pass no ha fallado aún
                    ref_set = set(ref_entities)
                    model_set = set(model_entities)
                    if ref_set != model_set:
                        verif1_pass = False
        else:
            verif3_pass = False
            verif2_pass = False
            verif1_pass = False

        return verif1_pass, verif2_pass, verif3_pass, verif4_pass

    except Exception as e:
        print(f"Error evaluate_model_output(): {e}")
        return False, False, False, False


def evaluate_model_output_entities(expected_output, output):
    expected_entities = []
    model_entities = []

    # Recoger todas las entidades esperadas (solo los nombres)
    for category in expected_output:
        for entity in expected_output[category]:
            expected_entities.append(
                entity[0].lower()
            )  # Solo el nombre, ignorando las posiciones

    # Recoger todas las entidades del modelo (maneja diccionarios y listas/tuplas, solo los nombres)
    for category in output:
        for entity in output[category]:
            if isinstance(entity, dict):
                model_entities.append(entity["name"].lower())  # Solo el nombre
            else:
                model_entities.append(entity[0].lower())  # Solo el nombre

    # 1. Número de entidades esperadas
    num_expected_entities = len(expected_entities)

    # 2. Número de entidades detectadas correctamente (independientemente de la categoría)
    num_correct_entities = 0
    for expected_entity in expected_entities:
        for model_entity in model_entities:
            if expected_entity == model_entity:
                num_correct_entities += 1
                model_entities.remove(model_entity)  # Evitar contar duplicados
                break

    # 3. Número de entidades detectadas correctamente y clasificadas correctamente
    num_correct_and_classified_entities = 0
    for category in expected_output:
        expected_entity_names = [
            entity[0].lower() for entity in expected_output[category]
        ]
        model_entity_names = [
            entity["name"].lower() if isinstance(entity, dict) else entity[0].lower()
            for entity in output.get(category, [])
        ]
        # Contar cada coincidencia individualmente
        for expected_entity in expected_entity_names:
            if expected_entity in model_entity_names:
                num_correct_and_classified_entities += 1
                model_entity_names.remove(expected_entity)  # Evitar contar duplicados

    return (
        num_expected_entities,
        num_correct_entities,
        num_correct_and_classified_entities,
    )


def evaluate_model_output_start_positions(expected_output, output):
    expected_positions = []
    model_positions = []

    # Recoger todas las posiciones iniciales de las entidades esperadas (independientemente de la categoría)
    for category in expected_output:
        for entity in expected_output[category]:
            expected_positions.append(
                (entity[0].lower(), entity[1])
            )  # (nombre_entidad, start_position)

    # Recoger todas las posiciones iniciales de las entidades del modelo (maneja diccionarios y listas/tuplas)
    for category in output:
        for entity in output[category]:
            if isinstance(entity, dict):
                model_positions.append(
                    (entity["name"].lower(), entity["start_position"])
                )
            else:
                model_positions.append((entity[0].lower(), entity[1]))

    # Número de posiciones iniciales acertadas con exactitud
    exact_matches = 0
    within_2_matches = 0
    within_5_matches = 0
    within_10_matches = 0

    for expected_entity, expected_start in expected_positions:
        for model_entity, model_start in model_positions:
            if expected_entity == model_entity:
                expected_start_int = int(expected_start)
                model_start_int = int(model_start)
                # Comprobar coincidencia exacta
                if expected_start_int == model_start_int:
                    exact_matches += 1
                    break  # Evitar contar duplicados
                # Comprobar margen de +-2
                elif abs(expected_start_int - model_start_int) <= 2:
                    within_2_matches += 1
                    break  # Evitar contar duplicados
                # Comprobar margen de +-5
                elif abs(expected_start_int - model_start_int) <= 5:
                    within_5_matches += 1
                    break  # Evitar contar duplicados
                # Comprobar margen de +-10
                elif abs(expected_start_int - model_start_int) <= 10:
                    within_10_matches += 1
                    break  # Evitar contar duplicados

    # Añadir los márgenes mayores a los márgenes menores (por ejemplo, si está dentro de +-2, también cuenta dentro de +-5 y +-10)
    within_2_matches += exact_matches
    within_5_matches += within_2_matches
    within_10_matches += within_5_matches

    return (exact_matches, within_2_matches, within_5_matches, within_10_matches)


def evaluate_model_output_end_positions(expected_output, output):
    expected_positions = []
    model_positions = []

    # Recoger todas las posiciones finales de las entidades esperadas (independientemente de la categoría)
    for category in expected_output:
        for entity in expected_output[category]:
            expected_positions.append(
                (entity[0].lower(), entity[2])
            )  # (nombre_entidad, end_position)

    # Recoger todas las posiciones finales de las entidades del modelo (maneja diccionarios y listas/tuplas)
    for category in output:
        for entity in output[category]:
            if isinstance(entity, dict):
                model_positions.append((entity["name"].lower(), entity["end_position"]))
            else:
                # Verificar que la entidad tenga al menos 3 elementos. Puede suceder que el modelo solo devuelva el nombre y la posición inicial. Es muy inusual, pero ya se han observado casos así.
                if len(entity) >= 3:
                    model_positions.append((entity[0].lower(), entity[2]))

    # Número de posiciones finales acertadas con exactitud
    exact_matches = 0
    within_2_matches = 0
    within_5_matches = 0
    within_10_matches = 0

    for expected_entity, expected_end in expected_positions:
        for model_entity, model_end in model_positions:
            if expected_entity == model_entity:
                expected_end_int = int(expected_end)
                model_end_int = int(model_end)
                # Comprobar coincidencia exacta
                if expected_end_int == model_end_int:
                    exact_matches += 1
                    break  # Evitar contar duplicados
                # Comprobar margen de +-2
                elif abs(expected_end_int - model_end_int) <= 2:
                    within_2_matches += 1
                    break  # Evitar contar duplicados
                # Comprobar margen de +-5
                elif abs(expected_end_int - model_end_int) <= 5:
                    within_5_matches += 1
                    break  # Evitar contar duplicados
                # Comprobar margen de +-10
                elif abs(expected_end_int - model_end_int) <= 10:
                    within_10_matches += 1
                    break  # Evitar contar duplicados

    # Añadir los márgenes mayores a los márgenes menores (por ejemplo, si está dentro de +-2, también cuenta dentro de +-5 y +-10)
    within_2_matches += exact_matches
    within_5_matches += within_2_matches
    within_10_matches += within_5_matches

    return (exact_matches, within_2_matches, within_5_matches, within_10_matches)
