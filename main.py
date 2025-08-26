import time
import config
from parser_formula import leer_formulas
from algoritmos.fuerza_bruta import fuerza_bruta
from algoritmos.dpll import DPLL

def main():
    # Leer fórmulas desde archivo
    formulas = leer_formulas("formulas.txt", config.LINEAS_A_LEER)

    for i, formula in enumerate(formulas):
        print(f"\nFórmula {i+1}: {formula}")

        inicio = time.time()

        if config.ALGORITMO == "fuerza_bruta":
            resultado, asignacion = fuerza_bruta(formula)
        elif config.ALGORITMO == "dpll":
            resultado, asignacion = DPLL(formula, {})
        else:
            raise ValueError("Algoritmo no reconocido en config.py")

        fin = time.time()

        if resultado:
            print(f"Satisfacible con modelo: {asignacion}")
        else:
            print("Insatisfacible")

        if config.MOSTRAR_TIEMPOS:
            print(f"Tiempo: {fin - inicio:.6f} segundos")

if __name__ == "__main__":
    main()
