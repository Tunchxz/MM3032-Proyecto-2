from sympy import symbols
from sympy.logic.boolalg import to_cnf
import re

def leer_formulas(path, lineas=None):
    """
    Lee un archivo y extrae fórmulas en forma clausal.

    Args:
        path: Ruta del archivo que contiene las fórmulas.
        lineas: Lista de números de línea a leer (opcional).
        
    Returns:
        Lista de fórmulas en forma clausal.
    """
    with open(path, "r", encoding="utf-8") as f:
        todas = [line.strip() for line in f if line.strip()]

    # Filtrar líneas si se especifica
    if lineas is not None:
        formulas = [todas[i] for i in lineas]
    else:
        formulas = todas

    return [a_forma_clausal(expr) for expr in formulas]


def a_forma_clausal(expr_str):
    """
    Convierte una fórmula lógica proposicional en string a forma clausal.
    Ejemplo: "p ∧ (¬p ∨ q)" → [[1], [-1, 2]]

    Args:
        expr_str: La expresión lógica en forma de string.

    Returns:
        Una fórmula en forma clausal (lista de listas de enteros).
    """
    # Sustituciones para que Sympy entienda los operadores
    expr_str = expr_str.replace("∧", "&").replace("∨", "|").replace("¬", "~")

    # Detectar símbolos proposicionales (letras) en orden de aparición
    variables = []
    for v in re.findall(r"[a-zA-Z]\w*", expr_str):
        if v not in variables:
            variables.append(v)
    simbolos = {v: symbols(v) for v in variables}

    # Convertir a CNF usando sympy
    expr = eval(expr_str, simbolos)
    cnf = to_cnf(expr, simplify=True)

    # Si sympy devuelve True o False, procesar la expresión original manualmente
    if str(cnf) == "True" or str(cnf) == "False":
        return obtener_clausulas_desde_texto(expr_str, variables)
    # Convertir CNF de sympy a lista de listas de enteros, respetando el orden de aparición
    return obtener_clausulas_desde_texto(expr_str, variables)


def obtener_clausulas_desde_texto(expr_str, variables):
    """
    Extrae las cláusulas y literales en el orden de aparición en el texto original.
    
    Args:
        expr_str: La expresión lógica en forma de string.
        variables: Lista de variables proposicionales en la fórmula original.

    Returns:
        Una fórmula en forma clausal (lista de listas de enteros).
    """
    # Normalizar operadores
    expr_str = expr_str.replace("∧", "&").replace("∨", "|").replace("¬", "~")
    # Separar cláusulas por &
    clausulas_raw = re.split(r"\s*&\s*", expr_str)
    var_index = {v: i+1 for i, v in enumerate(variables)}
    resultado = []
    for cl in clausulas_raw:
        # Extraer literales en orden
        literales = []
        # Buscar todos los literales (negados o no)
        for match in re.finditer(r"(~)?([a-zA-Z]\w*)", cl):
            neg, var = match.groups()
            idx = var_index[var]
            if neg:
                literales.append(-idx)
            else:
                literales.append(idx)
        if literales:
            resultado.append(literales)
    return resultado
