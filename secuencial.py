"""
Conteo de frecuencia de palabras - VERSION SECUENCIAL
Computacion Paralela y Distribuida, Seccion 10 
Daniela Ramirez (23053) - Bryan Martinez (23542) - Adriana Placios (23044)

Implementacion del diagrama de flujo secuencial
"""

import argparse
import os
import sys
import time

# Tamaño del buffer de lectura. El algoritmo sigue procesando caracter por
# caracter; el buffer solo evita una llamada al sistema operativo por caracter.
TAMANIO_BUFFER = 65536


def es_separador(caracter):
    """Devuelve True si el caracter NO forma parte de una palabra.

    Separadores: espacios, saltos de linea, tabulaciones y cualquier signo de
    puntuacion. Se consideran parte de una palabra las letras y los digitos.
    """
    return not caracter.isalnum()


def registrar_palabra(libro_palabras, palabra):
    """Decision '¿es nueva?' del diagrama, con sus dos ramas."""
    if palabra in libro_palabras:          # la palabra NO es nueva
        libro_palabras[palabra] += 1       # acceder a la llave y sumar 1
    else:                                  # la palabra SI es nueva
        libro_palabras[palabra] = 1        # agregar al diccionario con valor 1


def contar_frecuencias(ruta_archivo):
    """Recorre el archivo caracter por caracter y devuelve palabra - frecuencia."""
    libro_palabras = {}       # diccionario de frecuencias (salida del algoritmo)
    palabra_actual = ""       # palabra que se esta construyendo
    total_palabras = 0        # contador auxiliar para el resumen

    with open(ruta_archivo, "r", encoding="utf-8", errors="replace") as archivo:
        while True:
            bloque = archivo.read(TAMANIO_BUFFER)
            if bloque == "":
                break                       # ¿es EOF? -> SI

            for caracter_actual in bloque:
                if es_separador(caracter_actual):
                    # Fin de una palabra: solo se registra si no esta vacia
                    # (asi se ignoran los separadores consecutivos).
                    if palabra_actual != "":
                        registrar_palabra(libro_palabras, palabra_actual)
                        total_palabras += 1
                        palabra_actual = ""   # resetear palabraActual
                else:
                    # Appendear el caracter, normalizado a minusculas para que
                    # "TEXTO", "Texto" y "texto" cuenten como la misma palabra.
                    palabra_actual += caracter_actual.lower()

    # CORRECCION respecto al diagrama original: si el archivo no termina en un
    # separador, la ultima palabra quedaria sin registrarse.
    if palabra_actual != "":
        registrar_palabra(libro_palabras, palabra_actual)
        total_palabras += 1

    return libro_palabras, total_palabras


def ordenar_resultados(libro_palabras):
    """Orden determinista: frecuencia descendente y, a igual frecuencia, alfabetico.
    Es necesario para poder comparar la salida con la de la version paralela.
    """
    return sorted(libro_palabras.items(), key=lambda par: (-par[1], par[0]))


def formatear_resultados(resultados, total_palabras, duracion, limite=None):
    lineas = []
    lineas.append("FRECUENCIA DE PALABRAS - VERSION SECUENCIAL")
    lineas.append("=" * 46)
    mostradas = resultados if limite is None else resultados[:limite]
    for palabra, frecuencia in mostradas:
        lineas.append("{:<28} {:>6}".format(palabra, frecuencia))
    if limite is not None and len(resultados) > limite:
        lineas.append("... ({} palabras distintas mas)".format(len(resultados) - limite))
    lineas.append("=" * 46)
    lineas.append("Palabras totales    : {}".format(total_palabras))
    lineas.append("Palabras distintas  : {}".format(len(resultados)))
    lineas.append("Tiempo de ejecucion : {:.4f} s".format(duracion))
    return "\n".join(lineas)


def main():
    analizador = argparse.ArgumentParser(
        description="Conteo secuencial de frecuencia de palabras en un archivo de texto.")
    analizador.add_argument("archivo", help="Ruta del archivo .txt a procesar")
    analizador.add_argument("--top", type=int, default=None,
                            help="Mostrar solo las N palabras mas frecuentes")
    analizador.add_argument("--salida", default=None,
                            help="Guardar el resultado completo en un archivo de texto")
    argumentos = analizador.parse_args()

    # Validacion 1: el archivo se puede abrir
    if not os.path.isfile(argumentos.archivo):
        print("No fue posible abrir el archivo: {}".format(argumentos.archivo))
        sys.exit(1)

    # Validacion 2: el archivo no esta vacio
    if os.path.getsize(argumentos.archivo) == 0:
        print("El archivo esta vacio; no hay palabras que contar.")
        sys.exit(0)

    inicio = time.perf_counter()
    libro_palabras, total_palabras = contar_frecuencias(argumentos.archivo)
    duracion = time.perf_counter() - inicio

    if not libro_palabras:
        print("No se encontraron palabras en el archivo.")
        sys.exit(0)

    resultados = ordenar_resultados(libro_palabras)
    print(formatear_resultados(resultados, total_palabras, duracion, argumentos.top))

    if argumentos.salida:
        # El archivo de salida siempre lleva la lista completa, para poder
        # compararla linea por linea con la de la version paralela.
        with open(argumentos.salida, "w", encoding="utf-8") as salida:
            for palabra, frecuencia in resultados:
                salida.write("{}\t{}\n".format(palabra, frecuencia))
        print("\nResultado completo guardado en: {}".format(argumentos.salida))


if __name__ == "__main__":
    main()
