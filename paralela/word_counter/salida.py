"""Fusión, formato y almacenamiento del resultado paralelo."""

from pathlib import Path

from utils.diccionarios import ordenar_por_frecuencia


def fusionar_diccionarios(
    diccionarios_locales: list[dict[str, int]],
) -> dict[str, int]:
    """Fusiona secuencialmente los diccionarios locales."""
    diccionario_final: dict[str, int] = {}

    for diccionario_local in diccionarios_locales:
        for palabra, frecuencia_local in diccionario_local.items():
            diccionario_final[palabra] = (
                diccionario_final.get(palabra, 0) + frecuencia_local
            )

    return diccionario_final


def formatear_resultados(
    diccionario: dict[str, int],
    duracion: float,
    procesos_utilizados: int,
    limite: int | None = None,
) -> str:
    """Genera el resumen legible del conteo paralelo."""
    resultados = ordenar_por_frecuencia(diccionario)
    mostrados = resultados if limite is None else resultados[:limite]

    lineas = [
        "FRECUENCIA DE PALABRAS - VERSION PARALELA",
        "=" * 46,
    ]

    for palabra, frecuencia in mostrados:
        lineas.append(f"{palabra:<28} {frecuencia:>6}")

    if limite is not None and len(resultados) > limite:
        restantes = len(resultados) - limite
        lineas.append(f"... ({restantes} palabras distintas más)")

    lineas.extend([
        "=" * 46,
        f"Palabras totales encontradas : {sum(diccionario.values())}",
        f"Palabras únicas encontradas  : {len(diccionario)}",
        f"Procesos utilizados          : {procesos_utilizados}",
        f"Tiempo de ejecución          : {duracion:.4f} s",
    ])

    return "\n".join(lineas)


def guardar_resultados(
    diccionario: dict[str, int],
    ruta: Path,
) -> None:
    """Guarda todas las frecuencias en un archivo de texto."""
    resultados = ordenar_por_frecuencia(diccionario)

    with ruta.open("w", encoding="utf-8") as archivo:
        for palabra, frecuencia in resultados:
            archivo.write(f"{palabra}\t{frecuencia}\n")
