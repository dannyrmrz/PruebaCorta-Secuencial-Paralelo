from dataclasses import dataclass

from utils.separadores import es_separador


class InvalidProcessCountError(Exception):
    """Indica que la cantidad solicitada de procesos no es válida."""


@dataclass(frozen=True, slots=True)
class BlockRange:
    """Representa el intervalo semiabierto ``[start, end)`` de un bloque."""

    block_id: int
    start: int
    end: int


def dividir_en_bloques(texto: str, cantidad_procesos: int) -> list[BlockRange]:
    """Divide el texto sin cortar palabras ni superponer rangos."""
    if cantidad_procesos <= 0:
        raise InvalidProcessCountError(
            "La cantidad de procesos debe ser mayor que cero."
        )
    if not texto:
        return []

    cantidad_real = min(cantidad_procesos, len(texto))
    tamano_aproximado = len(texto) // cantidad_real
    bloques: list[BlockRange] = []
    inicio = 0

    for indice in range(cantidad_real):
        if inicio >= len(texto):
            break

        if indice == cantidad_real - 1:
            fin = len(texto)
        else:
            fin = min(inicio + tamano_aproximado, len(texto))

            while fin < len(texto) and not es_separador(texto[fin]):
                fin += 1

            if fin < len(texto):
                fin += 1

        if fin > inicio:
            bloques.append(BlockRange(len(bloques), inicio, fin))
            inicio = fin

    if inicio < len(texto):
        bloques.append(BlockRange(len(bloques), inicio, len(texto)))

    validar_rangos(texto, bloques)
    return bloques


def validar_rangos(texto: str, bloques: list[BlockRange]) -> None:
    """Comprueba cobertura, continuidad y límites seguros."""
    if not bloques:
        if texto:
            raise ValueError("El texto no fue cubierto por ningún bloque.")
        return

    if bloques[0].start != 0:
        raise ValueError("El primer bloque no comienza en cero.")
    if bloques[-1].end != len(texto):
        raise ValueError("El último bloque no termina al final del texto.")

    for indice, bloque in enumerate(bloques):
        if bloque.start < 0 or bloque.start >= bloque.end:
            raise ValueError(f"El bloque {bloque.block_id} tiene un rango inválido.")

        if indice == len(bloques) - 1:
            continue

        siguiente = bloques[indice + 1]
        if bloque.end != siguiente.start:
            raise ValueError("Los bloques tienen espacios o superposiciones.")

        limite = bloque.end
        if (
            0 < limite < len(texto)
            and not es_separador(texto[limite - 1])
            and not es_separador(texto[limite])
        ):
            raise ValueError("Un límite interno corta una palabra.")
