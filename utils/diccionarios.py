def registrar_palabra(
    diccionario: dict[str, int],
    palabra: str,
) -> None:
    """Normaliza y registra una palabra no vacía."""
    if not palabra:
        return

    palabra_normalizada = palabra.lower()
    diccionario[palabra_normalizada] = (
        diccionario.get(palabra_normalizada, 0) + 1
    )


def ordenar_por_frecuencia(
    diccionario: dict[str, int],
) -> list[tuple[str, int]]:
    """Ordena por frecuencia descendente y luego alfabéticamente."""
    return sorted(
        diccionario.items(),
        key=lambda elemento: (-elemento[1], elemento[0]),
    )
