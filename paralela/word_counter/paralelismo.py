"""Creación, ejecución y sincronización de procesos independientes."""

from concurrent.futures import ProcessPoolExecutor, as_completed

from .bloques import BlockRange
from .conteo import WorkerResult, procesar_bloque


class WorkerExecutionError(Exception):
    """Indica que un proceso no pudo terminar correctamente."""


def validar_resultados(
    identificadores_esperados: set[int],
    resultados: list[WorkerResult],
) -> None:
    """Comprueba que cada bloque entregue exactamente un resultado."""
    identificadores = [resultado.block_id for resultado in resultados]

    if len(resultados) != len(identificadores_esperados):
        raise WorkerExecutionError(
            "La cantidad de resultados no coincide con los bloques."
        )

    if len(identificadores) != len(set(identificadores)):
        raise WorkerExecutionError(
            "Se recibieron resultados duplicados."
        )

    if set(identificadores) != identificadores_esperados:
        raise WorkerExecutionError(
            "Falta el resultado de uno o más bloques."
        )


def contar_palabras_paralelo(
    texto: str,
    bloques: list[BlockRange],
) -> list[dict[str, int]]:
    """Procesa cada bloque mediante un proceso independiente."""
    if not bloques:
        return []

    resultados: list[WorkerResult] = []
    esperados = {bloque.block_id for bloque in bloques}

    with ProcessPoolExecutor(max_workers=len(bloques)) as executor:
        tareas = {
            executor.submit(
                procesar_bloque,
                bloque.block_id,
                texto[bloque.start:bloque.end],
                bloque.start,
                bloque.end,
            ): bloque.block_id
            for bloque in bloques
        }

        try:
            for tarea in as_completed(tareas):
                resultados.append(tarea.result())
        except Exception as error:
            bloque_fallido = tareas[tarea]

            for tarea_pendiente in tareas:
                tarea_pendiente.cancel()

            raise WorkerExecutionError(
                f"Falló el proceso del bloque {bloque_fallido}."
            ) from error

    validar_resultados(esperados, resultados)
    resultados.sort(key=lambda resultado: resultado.block_id)

    return [resultado.dictionary for resultado in resultados]
