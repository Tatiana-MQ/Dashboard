# Plan de Estudios UNA — Web App

Dashboard académico para análisis del plan de estudios usando BFS, BST y grafos.

## Archivos

```
app.py            ← aplicación principal (Streamlit)
datos.py          ← grafo y nombres de materias
logica.py         ← BST e inversión del grafo
requirements.txt  ← dependencias
```

## Correr localmente

```bash
pip install streamlit
streamlit run app.py
```

## Subir a Streamlit Cloud (URL pública gratuita)

1. Subí estos 4 archivos a un repositorio GitHub (puede ser privado).
2. Entrá a https://share.streamlit.io
3. Conectá tu cuenta de GitHub.
4. Seleccioná el repositorio y el archivo `app.py`.
5. Clic en **Deploy** — en ~1 minuto tenés tu URL pública.

Tu URL tendrá el formato:
`https://tu-usuario-tu-repo-app-xxxx.streamlit.app`
