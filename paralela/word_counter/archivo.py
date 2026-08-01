from pathlib import Path


class FileOpenError(Exception):
    """Indica que un archivo no pudo abrirse."""


class EmptyFileError(Exception):
    """Indica que el archivo está vacío."""


class EncodingError(Exception):
    """Indica que el archivo no usa la codificación solicitada."""


def leer_archivo(ruta: Path, encoding: str = "utf-8") -> str:
    """Valida y lee completamente un archivo de texto."""
    if not ruta.exists():
        raise FileOpenError(f"La ruta no existe: {ruta}")
    if not ruta.is_file():
        raise FileOpenError(f"La ruta no corresponde a un archivo: {ruta}")

    try:
        with ruta.open("r", encoding=encoding) as archivo:
            texto = archivo.read()
    except UnicodeDecodeError as error:
        raise EncodingError(
            f"No fue posible decodificar el archivo usando {encoding}"
        ) from error
    except OSError as error:
        raise FileOpenError(str(error)) from error

    if texto == "":
        raise EmptyFileError(
            "El archivo está vacío; no hay palabras que contar."
        )

    return texto
