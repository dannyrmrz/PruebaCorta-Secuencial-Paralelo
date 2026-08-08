# Conteo de frecuencia de palabras

## Video de Explicación

https://youtu.be/SmI1zYr-pL4

## Estructura del proyecto

### `secuencial/`

Contiene la implementación secuencial del algoritmo y el archivo
`resultados_secuencial.txt` generado al procesar el documento de prueba.

### `paralela/`

Contiene la implementación paralela basada en procesos independientes.
El texto se divide en bloques seguros para evitar que una palabra quede
cortada entre dos procesos. También contiene
`resultados_paralelo.txt`, generado por la ejecución paralela.

### `utils/`

Contiene funciones utilizadas por ambas implementaciones, como la
identificación de separadores, el registro de palabras y el
ordenamiento de los diccionarios de frecuencias.

### `texto_prueba.txt`

Documento utilizado para ejecutar y comparar las versiones secuencial
y paralela. Ambas implementaciones deben producir las mismas palabras
y frecuencias.

### `Paralelización.pdf`

Documento que contiene el enlace al diagrama de flujo del algoritmo,
junto con parte del análisis realizado para diseñar su paralelización.

## Ejecución

Desde la raíz del proyecto:

```bash
python3 -m secuencial.secuencial texto_prueba.txt
```

```bash
python3 -m paralela.paralelo \
  --file texto_prueba.txt \
  --processes 4
```
