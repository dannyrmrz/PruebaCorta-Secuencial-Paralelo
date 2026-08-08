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

from utils.diccionarios import ordenar_por_frecuencia, registrar_palabra
from utils.separadores import es_separador

# Tamaño del buffer de lectura. El algoritmo sigue procesando caracter por
# caracter; el buffer solo evita una llamada al sistema operativo por caracter.
TAMANIO_BUFFER = 65536

def contar_frecuencias(ruta_archivo):
    """Recorre el archivo caracter por caracter y devuelve palabra - frecuencia."""
    libro_palabras = {}
    palabra_actual = ""
    total_palabras = 0
    tiempo_conteo = 0.0

    with open(ruta_archivo, "r", encoding="utf-8", errors="replace") as archivo:
        while True:
            bloque = archivo.read(TAMANIO_BUFFER)
            if bloque == "":
                break

            inicio_bloque = time.perf_counter()
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
            tiempo_conteo += time.perf_counter() - inicio_bloque

    # CORRECCION respecto al diagrama original: si el archivo no termina en un
    # separador, la ultima palabra quedaria sin registrarse.
    inicio_ultima_palabra = time.perf_counter()
    if palabra_actual != "":
        registrar_palabra(libro_palabras, palabra_actual)
        total_palabras += 1
    tiempo_conteo += time.perf_counter() - inicio_ultima_palabra

    return libro_palabras, total_palabras, tiempo_conteo


def formatear_resultados(
    resultados,
    total_palabras,
    tiempo_conteo,
    tiempo_total,
    limite=None,
):
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
    lineas.append(
        "Tiempo de conteo   : {:.6f} s".format(tiempo_conteo)
    )
    lineas.append(
        "Tiempo total       : {:.6f} s".format(tiempo_total)
    )
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
    inicio_total = time.perf_counter()

    # Validacion 1: el archivo se puede abrir
    if not os.path.isfile(argumentos.archivo):
        print("No fue posible abrir el archivo: {}".format(argumentos.archivo))
        sys.exit(1)

    # Validacion 2: el archivo no esta vacio
    if os.path.getsize(argumentos.archivo) == 0:
        print("El archivo esta vacio; no hay palabras que contar.")
        sys.exit(0)

    libro_palabras, total_palabras, tiempo_conteo = contar_frecuencias(
        argumentos.archivo
    )
    tiempo_total = time.perf_counter() - inicio_total

    if not libro_palabras:
        print("No se encontraron palabras en el archivo.")
        sys.exit(0)

    resultados = ordenar_por_frecuencia(libro_palabras)
    print(
        formatear_resultados(
            resultados,
            total_palabras,
            tiempo_conteo,
            tiempo_total,
            argumentos.top,
        )
    )

    if argumentos.salida:
        # El archivo de salida siempre lleva la lista completa, para poder
        # compararla linea por linea con la de la version paralela.
        with open(argumentos.salida, "w", encoding="utf-8") as salida:
            for palabra, frecuencia in resultados:
                salida.write("{}\t{}\n".format(palabra, frecuencia))
        print("\nResultado completo guardado en: {}".format(argumentos.salida))

main()
