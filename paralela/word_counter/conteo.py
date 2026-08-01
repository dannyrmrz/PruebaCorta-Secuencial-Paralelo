from dataclasses import dataclass

from utils.diccionarios import registrar_palabra
from utils.separadores import es_separador


@dataclass(frozen=True, slots=True)
class WorkerResult:
    """Resultado local producido por un proceso."""

    block_id: int
    dictionary: dict[str, int]


def contar_palabras_secuencial(texto_bloque: str) -> dict[str, int]:
    """Cuenta las palabras de un bloque carácter por carácter."""
    diccionario_local: dict[str, int] = {}
    palabra_actual = ""

    for caracter_actual in texto_bloque:
        if es_separador(caracter_actual):
            registrar_palabra(diccionario_local, palabra_actual)
            palabra_actual = ""
        else:
            palabra_actual += caracter_actual

    registrar_palabra(diccionario_local, palabra_actual)
    return diccionario_local


def procesar_bloque(
    block_id: int,
    texto_bloque: str,
    inicio: int,
    fin: int,
) -> WorkerResult:
    """Procesa un bloque aislado y retorna su diccionario local."""
    if inicio < 0 or fin < inicio:
        raise ValueError(f"Rango inválido para el bloque {block_id}.")

    return WorkerResult(
        block_id=block_id,
        dictionary=contar_palabras_secuencial(texto_bloque),
    )
