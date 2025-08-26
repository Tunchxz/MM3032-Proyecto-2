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

    # Detectar símbolos proposicionales (letras)
    variables = sorted(set(re.findall(r"[a-zA-Z]\w*", expr_str)))
    simbolos = {v: symbols(v) for v in variables}

    # Convertir a CNF usando sympy
    expr = eval(expr_str, simbolos)
    cnf = to_cnf(expr, simplify=True)

    # Convertir CNF de sympy a lista de listas de enteros
    return convertir_a_clausal(cnf, variables)


def convertir_a_clausal(cnf_expr, variables):
    """
    Convierte una expresión CNF de sympy a forma clausal tipo [[1,-2], [3]].

    Args:
        cnf_expr: La expresión CNF en forma de objeto sympy.
        variables: Lista de variables proposicionales en la fórmula original.

    Returns:
        Una fórmula en forma clausal (lista de listas de enteros).
    """
    var_index = {v: i+1 for i, v in enumerate(variables)}

    def literal_to_int(lit):
        if lit.is_Symbol:
            return var_index[str(lit)]
        elif lit.func.__name__ == "Not":
            return -var_index[str(lit.args[0])]
        else:
            raise ValueError("Literal no reconocido")

    if cnf_expr.func.__name__ == "And":
        clausulas = []
        for sub in cnf_expr.args:
            if sub.func.__name__ == "Or":
                clausulas.append([literal_to_int(l) for l in sub.args])
            else:
                clausulas.append([literal_to_int(sub)])
        return clausulas
    elif cnf_expr.func.__name__ == "Or":
        return [[literal_to_int(l) for l in cnf_expr.args]]
    else:  # literal único
        return [[literal_to_int(cnf_expr)]]
