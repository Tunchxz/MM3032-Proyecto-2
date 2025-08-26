import itertools

def evaluar_formula(formula, asignacion):
    """
    Evalúa la fórmula (en forma clausal) bajo la asignación dada.

    Args:
        formula: lista de cláusulas, cada cláusula es lista de literales (enteros).
        asignacion: diccionario {var -> valor booleano}.

    Returns:
        True si la fórmula es verdadera bajo la asignación, False en caso contrario.
    """
    for clausula in formula:
        valor_clausula = False
        for literal in clausula:
            var = abs(literal)
            if literal > 0:  # literal positivo
                valor_clausula |= asignacion[var]
            else:  # literal negativo
                valor_clausula |= not asignacion[var]
        if not valor_clausula:
            return False  # alguna cláusula no se satisface
    return True  # todas las cláusulas satisfechas


def fuerza_bruta(formula):
    """
    Algoritmo de fuerza bruta para satisfacibilidad.
    
    Args:
        formula: fórmula en forma clausal.

    Returns:
        (True, asignacion) si es satisfacible, (False, {}) si es insatisfacible.
    """
    # Paso 1: recolectar todas las variables presentes
    variables = sorted({abs(literal) for clausula in formula for literal in clausula})

    # Paso 2: generar todas las posibles asignaciones de verdad
    for valores in itertools.product([False, True], repeat=len(variables)):
        asignacion = {var: val for var, val in zip(variables, valores)}

        # Paso 3: evaluar la fórmula
        if evaluar_formula(formula, asignacion):
            return True, asignacion  # encontramos un modelo que satisface

    # Paso 4: si ninguna asignación satisface
    return False, {}
