def seleccionar_literal(B):
    """
    Selecciona un literal de la fórmula (no determinístico).

    Args:
        B: fórmula booleana en forma clausal (lista de listas de enteros).

    Returns:
        Un literal de la fórmula o None si no hay literales.
    """
    for clausula in B:
        if clausula:  # cláusula no vacía
            return next(iter(clausula))
    return None


def simplificar(B, L):
    """
    Paso auxiliar: Simplificación de la fórmula B al asumir L = verdadero.
    - Elimina todas las cláusulas que contienen L (ya están satisfechas).
    - Elimina la negación de L en las demás cláusulas.

    Args:
        B: fórmula booleana en forma clausal (lista de listas de enteros).
        L: literal a asumir como verdadero.

    Returns:
        Nueva fórmula simplificada.
    """
    Bp = []
    for clausula in B:
        if L in clausula:
            continue  # cláusula satisfecha → se descarta
        if -L in clausula:
            nueva = clausula.copy()
            nueva.remove(-L)  # quitamos ¬L porque L es verdadero
            Bp.append(nueva)
        else:
            Bp.append(clausula.copy())
    return Bp


def DPLL(B, I):
    """
    Algoritmo DPLL recursivo.

    Args:
        B: fórmula booleana en forma clausal (lista de listas de enteros).
        I: asignación parcial (diccionario literal -> valor booleano).
    
    Returns:
        (bool, dict) donde el bool indica si la fórmula es satisfacible y 
        el dict es la asignación encontrada.
    """
    # Paso 1: Si B es vacía, entonces regresar True e I
    if not B:
        return True, I

    # Paso 2: Si hay alguna disyunción vacía en B, entonces regresar False y asignación vacía/nula
    for clausula in B:
        if not clausula:
            return False, {}

    # Paso 3: Seleccionar un literal L (en forma positiva si es posible)
    L = seleccionar_literal(B)
    if L is None:
        return True, I  # No hay literales → se considera satisfecha

    # Paso 4: Construir B' eliminando cláusulas con L y ¬L en otras
    # e intentar con L = verdadero
    Bp = simplificar(B, L)
    I_true = I.copy()
    I_true[abs(L)] = (L > 0)  # agregamos a la asignación: L es verdadero
    # Llamada recursiva
    res, I1 = DPLL(Bp, I_true)
    # Paso 5: Si resultado fue verdadero, regresar True e I1
    if res:
        return True, I1

    # Paso 6: Construir B' ahora asumiendo L = falso (equivalente a asumir ¬L verdadero)
    Bp = simplificar(B, -L)
    I_false = I.copy()
    I_false[abs(L)] = (L < 0)  # agregamos a la asignación: L es falso
    # Llamada recursiva
    res, I2 = DPLL(Bp, I_false)
    # Paso 7: Si resultado fue verdadero, regresar True e I2
    if res:
        return True, I2

    # Paso 8: Si ninguna asignación funcionó, regresar False y asignación vacía/nula
    return False, {}
