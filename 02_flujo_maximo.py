# -*- coding: utf-8 -*-
"""
PROGRAMA: FLUJO MÁXIMO
Propósito: Calcular la máxima cantidad de flujo que puede circular desde el primer nodo
          hasta el último nodo en una red con capacidades.
Autor: Javier Ayala
"""

from collections import deque

def edmonds_karp(capacidad, fuente, sumidero):
    """
    Implementación del algoritmo de Edmonds-Karp (BFS) para flujo máximo.
    capacidad: matriz de capacidades (n x n)
    fuente: índice del nodo fuente (0)
    sumidero: índice del nodo sumidero (n-1)
    Retorna el valor del flujo máximo.
    """
    n = len(capacidad)
    flujo = 0
    # Mientras haya un camino aumentante
    while True:
        # BFS para encontrar el camino más corto en la red residual
        padre = [-1] * n
        padre[fuente] = fuente
        cola = deque([fuente])
        while cola and padre[sumidero] == -1:
            u = cola.popleft()
            for v in range(n):
                if padre[v] == -1 and capacidad[u][v] > 0:
                    padre[v] = u
                    cola.append(v)
        # Si no se llegó al sumidero, terminamos
        if padre[sumidero] == -1:
            break
        # Encontrar la capacidad mínima en el camino encontrado (cuello de botella)
        cuello = float('inf')
        v = sumidero
        while v != fuente:
            u = padre[v]
            cuello = min(cuello, capacidad[u][v])
            v = u
        # Actualizar las capacidades residuales (restar en dirección directa, sumar en inversa)
        v = sumidero
        while v != fuente:
            u = padre[v]
            capacidad[u][v] -= cuello
            capacidad[v][u] += cuello
            v = u
        flujo += cuello
    return flujo


def main():
    print("=" * 80)
    print("                           CALCULADORA DE FLUJO MÁXIMO")
    print("                           (Algoritmo de Edmonds‑Karp)")
    print("=" * 80)
    print("   Desarrollado por: Javier Ayala | https://github.com/ayalapjavier | 2026")
    print("=" * 80)
    print("Este programa calcula la máxima cantidad de flujo")
    print("que puede circular desde el primer nodo (A)")
    print("hasta el último nodo, respetando las capacidades de cada arco.\n")

    # Solicitar número de nodos
    while True:
        try:
            n = int(input("Número de nodos (máx. 26): "))
            if 1 <= n <= 26:
                break
            else:
                print("Por favor, ingrese un número entre 1 y 26.")
        except ValueError:
            print("Debe ingresar un número entero.")

    # Generar letras (A, B, C, ...)
    letras = [chr(ord('A') + i) for i in range(n)]
    print(f"\nLos nodos disponibles son: {', '.join(letras)}\n")

    # Inicializar matriz de capacidades (n x n) con ceros
    capacidad = [[0] * n for _ in range(n)]

    # Ingreso de arcos
    print("Ingrese cada arco (conexión) con su capacidad.")
    print("Formato: Origen Destino Capacidad")
    print("Ejemplo: A B 15  (significa que de A a B pueden pasar 15 vehículos por hora)")
    print("Escriba 'fin' para terminar.\n")

    while True:
        entrada = input("Arco: ").strip()
        if entrada.lower() == "fin":
            break

        partes = entrada.split()
        if len(partes) != 3:
            print("Formato incorrecto. Use: Origen Destino Capacidad")
            continue

        o, d, c = partes[0].upper(), partes[1].upper(), partes[2]

        # Validar nodos
        if o not in letras:
            print(f"El nodo {o} no existe. Válidos: {', '.join(letras)}")
            continue
        if d not in letras:
            print(f"El nodo {d} no existe. Válidos: {', '.join(letras)}")
            continue

        # Validar capacidad (entero positivo)
        try:
            cap = int(c)
            if cap < 0:
                print("La capacidad debe ser un número entero no negativo.")
                continue
        except ValueError:
            print("La capacidad debe ser un número entero.")
            continue

        # Guardar en la matriz
        i = letras.index(o)
        j = letras.index(d)
        capacidad[i][j] = cap
        print(f"Arco guardado: {o} -> {d} con capacidad {cap}")

    # Definir fuente (primer nodo) y sumidero (último nodo)
    fuente = 0          # nodo A
    sumidero = n - 1    # último nodo (por ejemplo, si n=4, sería D)

    # Hacemos una copia de la matriz porque el algoritmo la modifica
    from copy import deepcopy
    capacidad_respaldo = deepcopy(capacidad)

    # Calcular flujo máximo
    flujo_max = edmonds_karp(capacidad, fuente, sumidero)

    # Mostrar resultado
    print("\n" + "=" * 80)
    print(f"El flujo máximo desde el nodo A hasta el nodo {letras[-1]} es: {flujo_max}")
    print("=" * 80)

    input("\nPresione Enter para salir...")


if __name__ == "__main__":
    main()