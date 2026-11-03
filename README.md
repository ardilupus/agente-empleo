# Agente orquestador de búsqueda de empleo

Bot en Python que revisa LinkedIn (público y con sesión), Elempleo, Magneto y Computrabajo en intervalos aleatorios, filtra las ofertas por palabras clave en español e inglés, les da un puntaje, descarta duplicados del mes y envía las mejores por Telegram, cada perfil a su propio bot.

## Cómo usarlo

1. `pip install -r requirements.txt`
2. Copia `.env.example` como `.env` y escribe ahí tus tokens y chat IDs de Telegram (los creas con @BotFather).
3. `python agente_empleo.py`

El archivo `.env` y el historial `ofertas_enviadas.txt` no se suben al repositorio.

## Siguiente versión

- Guardar todas las ofertas en MongoDB como documentos JSON.
- Comparar cada oferta con la hoja de vida usando embeddings (LangChain).
- Las ofertas con coincidencia de 80% o más pasan a un agente que sugiere qué ajustar en la hoja de vida y las envía por Telegram.

Autor: Andrés Ardila · [ardilupus.github.io](https://ardilupus.github.io)
