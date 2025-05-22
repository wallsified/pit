# Pit: Python Information Tracker

Git-alike, hecho en Python.

## Comandos de Inicio

* `pit init` - Crea un nuevo repositorio pit en el directorio actual.
* `pit add [archivo]` - Agrega un nuevo archivo al repositorio pit.
* `pit remove [archivo]` - Elimina un archivo del repositorio pit.
* `pit status` - Muestra el estado actual del repositorio pit.
* `pit commit` - Realiza un commit de los cambios en el repositorio pit.
* `pit --help` - Muestra el menú de ayuda con todos los comandos disponibles.

## ¿Cómo modificar pit?

Para modificar pit, es necesario tener instalado `uv` y `pre-commit` en tu sistema.
Para instalar `uv` en tu sistema, es mejor referirse a la [documentación oficial](https://docs.astral.sh/uv/)
Luego es necesario instalar las configuraciones de `pre-commit` para que se ejecuten automáticamente al hacer un commit.
Para ello, basta con ejecutar el siguiente comando:

```bash

 pre-commit install

```


El proyecto usa PyCharm como IDE, por lo que es necesario tenerlo instalado para interactuar con el proyecto de manera
efectiva.

Para instalar PyCharm, es mejor referirse a la [documentación oficial](https://www.jetbrains.com/pycharm/download/).
Luego para poder trabajar con `uv`, es necesario configurar el IDE para que use el entorno virtual creado por `uv`.
La información necesaria para configurar el IDE se encuentra en
la [documentación oficial de uv](https://www.jetbrains.com/help/pycharm/uv.html).
