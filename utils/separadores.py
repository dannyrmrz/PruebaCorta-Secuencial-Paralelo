def es_separador(caracter: str) -> bool:
    """Indica si un carácter no pertenece a una palabra.

    Las letras y los dígitos forman palabras. Los espacios, saltos de
    línea, tabulaciones, puntuación y demás símbolos son separadores.
    """
    return not caracter.isalnum()
