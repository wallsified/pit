# pit

pit significa _"Python Information Tracker"_. Git-alike, hecho en Python.

# Instalación

El proyecto usa como manager de dependencias/entorno virtual `uv` y como IDE PyCharm, por lo que es
necesario tener ambos instalados para interactuar con el proyecto de manera efectiva.

## Instalación de `uv` y otras dependencias
Para instalar `uv` en tu sistema, es mejor referirse a la [documentación oficial](https://docs.astral.sh/uv/)
Posteriormente, basta con ejecutar el siguiente comando para sincronizar el entorno virtual con las dependencias del proyecto:

```bash
uv sync
```

Luego es necesario instalar las configuraciones  de `pre-commit` para que se ejecuten automáticamente al hacer un commit.
Para ello, basta con ejecutar el siguiente comando:

```bash
pre-commit install
```

## Instalación y Configuración de PyCharm
Para instalar PyCharm, es mejor referirse a la [documentación oficial](https://www.jetbrains.com/pycharm/download/).
Luego para poder trabajar con `uv`, es necesario configurar el IDE para que use el entorno virtual creado por `uv`.
La información necesaria para configurar el IDE se encuentra en la [documentación oficial de uv](https://www.jetbrains.com/help/pycharm/uv.html).
