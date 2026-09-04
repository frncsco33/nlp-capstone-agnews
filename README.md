# NLP Capstone — Clasificación de noticias AG News

Proyecto incremental del curso **Data Science III: NLP & Deep Learning aplicado a Ciencia de Datos** (Coderhouse). Un solo corpus (AG News, 4 clases: World, Sports, Business, Sci_Tech) atraviesa los cuatro módulos: pipeline PyTorch → preprocesamiento y EDA → baseline TF-IDF → fine-tuning eficiente con LoRA.

## Estructura

```
├── data/                    # ag_news_train.csv / ag_news_test.csv (no versionados)
│   └── processed/           # corpus limpio generado por el Módulo 2
├── notebooks/
│   ├── 01_pipeline_base_pytorch.ipynb    # Módulo 1
│   ├── 02_preprocesamiento_eda.ipynb     # Módulo 2
│   ├── 03_baseline_tfidf.ipynb           # Módulo 3
│   └── 04_finetuning_lora.ipynb          # Módulo 4 (correr en Colab con GPU)
├── src/                     # código compartido entre notebooks
└── reports/
    ├── figures/             # PNG de curvas, EDA y matrices de confusión
    └── metrics/             # JSON con métricas de baseline y LoRA
```

## Reproducibilidad

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Colocar `ag_news_train.csv` y `ag_news_test.csv` en `data/` y correr los notebooks en orden. Semilla global `SEED = 42` (`src/config.py`). El notebook 04 requiere GPU (Google Colab).

<!-- Secciones por completar al cierre de cada módulo: interpretación de la curva M1, decisiones del EDA, justificación del clasificador M3, resultados LoRA M4 -->
