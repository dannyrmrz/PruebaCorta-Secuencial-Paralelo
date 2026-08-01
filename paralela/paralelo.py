"""Punto de entrada de la versión paralela."""

import argparse
import os
import time
from pathlib import Path

from .word_counter.archivo import (
    EmptyFileError,
    EncodingError,
    FileOpenError,
    leer_archivo,
)
from .word_counter.bloques import (
    InvalidProcessCountError,
    dividir_en_bloques,
)
from .word_counter.paralelismo import (
    WorkerExecutionError,
    contar_palabras_paralelo,
)
from .word_counter.salida import (
    formatear_resultados,
    fusionar_diccionarios,
    guardar_resultados,
)

RUTA_RESULTADO = Path(__file__).with_name("resultados_paralelo.txt")


def crear_argumentos() -> argparse.ArgumentParser:
    """Construye la interfaz de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Conteo paralelo de frecuencia de palabras",
    )
    parser.add_argument(
        "--file",
        required=True,
        type=Path,
        help="Archivo de texto que se procesará",
    )
    parser.add_argument(
        "--processes",
        "--procesos",
        dest="procesos",
        type=int,
        default=os.cpu_count() or 1,
        help="Cantidad solicitada de procesos",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Mostrar únicamente las N palabras más frecuentes",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=RUTA_RESULTADO,
        help="Archivo donde se guardará el resultado completo",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
    )
    return parser


def main() -> int:
    """Ejecuta el flujo paralelo completo."""
    argumentos = crear_argumentos().parse_args()

    try:
        texto = leer_archivo(argumentos.file, argumentos.encoding)
        bloques = dividir_en_bloques(texto, argumentos.procesos)

        inicio = time.perf_counter()
        diccionarios_locales = contar_palabras_paralelo(texto, bloques)
        resultado = fusionar_diccionarios(diccionarios_locales)
        duracion = time.perf_counter() - inicio

        if not resultado:
            print("No se encontraron palabras en el archivo.")
        else:
            print(
                formatear_resultados(
                    resultado,
                    duracion,
                    len(bloques),
                    argumentos.top,
                )
            )

        guardar_resultados(resultado, argumentos.output)
        print(f"\nResultado completo guardado en: {argumentos.output}")
        return 0

    except EmptyFileError as error:
        print(error)
    except (FileOpenError, EncodingError) as error:
        print(f"No fue posible abrir el archivo: {error}")
    except (
        InvalidProcessCountError,
        WorkerExecutionError,
        OSError,
    ) as error:
        print(f"Error: {error}")

    return 1


# ProcessPoolExecutor necesita esta protección en macOS y Windows.
if __name__ == "__main__":
    raise SystemExit(main())
