# NLP Capstone — Clasificación de noticias AG News

Proyecto incremental del curso **Data Science III: NLP & Deep Learning aplicado a Ciencia de Datos** (Coderhouse). Un solo corpus (AG News, 4 clases: World, Sports, Business, Sci_Tech) atraviesa los cuatro módulos: pipeline PyTorch → preprocesamiento y EDA → baseline TF-IDF → fine-tuning eficiente con LoRA.

## Estructura

```
├── data/
│   ├── ag_news/             # CSVs provistos por la cátedra (8.000 train / 2.000 test)
│   ├── cargar_dataset.py    # loader provisto por la cátedra
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

Los CSVs de la cátedra ya están versionados en `data/ag_news/`. Correr los notebooks en orden. Semilla global `SEED = 42` (`src/config.py`). El notebook 04 requiere GPU (Google Colab).

## Resultados por módulo

### Módulo 1 — Pipeline PyTorch
PyTorch 2.14.0 · Adam con `learning_rate = 1e-3` · 6 épocas · MLP de una capa oculta (256, ReLU, dropout 0.3) sobre TF-IDF. La pérdida de entrenamiento cae 1.31 → 0.15 y la de validación 1.14 → 0.28, ambas monótonas: convergencia en ~3 épocas, sobreajuste incipiente contenido por el dropout. F1 (weighted) final en validación: **0.9122**. Interpretación completa en el notebook 01.

### Módulo 2 — Preprocesamiento y EDA
Pipeline Regex + SpaCy (`en_core_web_sm`): minúsculas, **decodificación de entidades HTML** (el corpus trae tags codificados como `&lt;A HREF=...&gt;` y entidades truncadas tipo `quot;`), remoción de tags completos y del boilerplate de Reuters, URLs, lematización y filtro de stop-words conservando tokens cortos de dominio ("us", "uk", "eu"). El EDA obligó a iterar el pipeline dos veces (primero cazó las entidades en el top 50; luego, las tripas de tags en los n-gramas). p95 de longitud del texto limpio: **33 tokens**. Clases perfectamente balanceadas (2.000 por categoría).

### Módulo 3 — Baseline TF-IDF
Tres configuraciones evaluadas contra validación; gana por margen mínimo la **B** (`max_features=50000`, unigramas+bigramas, `min_df=2`, `sublinear_tf`): 25.507 features efectivos y 102.032 parámetros, entrena en 0.2 s. **Test: accuracy 0.8955 · F1 weighted 0.8955 · F1 macro 0.8955** — en línea con la referencia de la cátedra (≈0.90). Mayor confusión: Business ↔ Sci_Tech.

### Módulo 4 — Fine-tuning con LoRA
Notebook 04, ejecutado en Google Colab (GPU). DistilBERT + adaptadores LoRA (`r=8`, `alpha=16`, módulos `q_lin`/`v_lin`); `max_len` = p95 de subword tokens medido con el tokenizador del modelo sobre texto crudo. Resultados y tabla comparativa contra el baseline en `reports/metrics/`.
