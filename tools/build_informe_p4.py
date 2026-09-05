"""Genera Salgado_Francisco_Checkpoint_NLP3.pdf — informe consolidado P4 + anexos P1/P2/P3."""
import json
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, NextPageTemplate,
)

REPO = Path.home() / "Documents/GitHub/nlp-capstone-agnews"
FIG = REPO / "reports/figures"
OUT = Path.home() / "Downloads/Salgado_Francisco_Checkpoint_NLP3.pdf"
REPO_URL = "https://github.com/frncsco33/nlp-capstone-agnews"
NB = f"{REPO_URL}/blob/main/notebooks"

# ---------- datos: siempre desde los JSON generados por los notebooks ----------
base = json.load(open(REPO / "reports/metrics/baseline_tfidf.json"))
lora = json.load(open(REPO / "reports/metrics/lora_transformer.json"))
ra, rb = base["classification_report"], lora["classification_report"]
pa = lora["parametros"]

# historial M1 desde los outputs del notebook 01
nb01 = json.load(open(REPO / "notebooks/01_pipeline_base_pytorch.ipynb"))
m1_hist = []
for cell in nb01["cells"]:
    for out in cell.get("outputs", []):
        for m in re.finditer(
            r"epoch (\d+): train ([\d.]+) \| val ([\d.]+) \| F1 ([\d.]+)",
            "".join(out.get("text", []))):
            m1_hist.append(tuple(m.groups()))

# ---------- estilos ----------
ss = getSampleStyleSheet()
S = {
    "body": ParagraphStyle("body", parent=ss["Normal"], fontSize=10, leading=14.5,
                           alignment=4, spaceAfter=7),
    "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontSize=15, leading=19,
                         spaceBefore=16, spaceAfter=8, textColor=colors.HexColor("#1a1a2e")),
    "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12, leading=15,
                         spaceBefore=12, spaceAfter=5, textColor=colors.HexColor("#16324f")),
    "cap": ParagraphStyle("cap", parent=ss["Normal"], fontSize=8.5, leading=11,
                          alignment=1, textColor=colors.HexColor("#555555"),
                          spaceBefore=3, spaceAfter=10),
    "note": ParagraphStyle("note", parent=ss["Normal"], fontSize=9.5, leading=14,
                           alignment=0, leftIndent=10, rightIndent=10,
                           borderPadding=8, backColor=colors.HexColor("#f4f6f8"),
                           spaceAfter=8),
    "mono": ParagraphStyle("mono", parent=ss["Code"], fontSize=8.5, leading=11.5),
}

TBL = TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16324f")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef2f5")]),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c4cc")),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
])

def P(txt, style="body"):
    return Paragraph(txt, S[style])

def img(name, width_cm):
    from PIL import Image as PILImage
    path = FIG / name
    w, h = PILImage.open(path).size
    return Image(str(path), width=width_cm * cm, height=width_cm * cm * h / w)

def f4(x):
    return f"{x:.4f}"

# ---------- documento ----------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawString(2 * cm, 1.2 * cm,
                      "Salgado Francisco · Pre-entrega 4 · Comisión 90500")
    canvas.drawRightString(letter[0] - 2 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()

doc = BaseDocTemplate(str(OUT), pagesize=letter,
                      leftMargin=2 * cm, rightMargin=2 * cm,
                      topMargin=2 * cm, bottomMargin=2 * cm,
                      title="Pre-entrega 4 — Clasificación con LoRA",
                      author="Francisco Salgado")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[frame]),
    PageTemplate(id="page", frames=[frame], onPage=footer),
])

story = []

# ================= PORTADA =================
story.append(Spacer(1, 3.2 * cm))
story.append(Paragraph("Data Science III: NLP &amp; Deep Learning aplicado a la Ciencia de Datos",
                       ParagraphStyle("c0", fontSize=11, alignment=1,
                                      textColor=colors.HexColor("#666666"))))
story.append(Spacer(1, 1.6 * cm))
story.append(Paragraph("Pre-entrega 4",
                       ParagraphStyle("c1", fontSize=30, leading=34, alignment=1,
                                      fontName="Helvetica-Bold",
                                      textColor=colors.HexColor("#16324f"))))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("Clasificación de noticias con fine-tuning<br/>eficiente mediante LoRA",
                       ParagraphStyle("c2", fontSize=17, leading=23, alignment=1,
                                      fontName="Helvetica-Bold")))
story.append(Spacer(1, 0.7 * cm))
story.append(Paragraph("Informe consolidado con evidencia de los Módulos 1, 2 y 3",
                       ParagraphStyle("c3", fontSize=12, alignment=1,
                                      textColor=colors.HexColor("#444444"))))
story.append(Spacer(1, 4.2 * cm))
meta = Table([
    ["Alumno", "Francisco Salgado"],
    ["Comisión", "90500"],
    ["Fecha", "8 de septiembre de 2026"],
    ["Repositorio", REPO_URL],
], colWidths=[3.2 * cm, 11 * cm])
meta.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 10.5),
    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#16324f")),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.HexColor("#dddddd")),
]))
story.append(meta)
story.append(NextPageTemplate("page"))
story.append(PageBreak())

# ================= NOTA AL CORRECTOR =================
story.append(P("Nota al corrector", "h1"))
story.append(P(
    "Este informe corresponde a la <b>Pre-entrega 4</b> (fine-tuning con LoRA). Dado que el "
    "proyecto es incremental y que las pre-entregas de los Módulos 1, 2 y 3 no fueron "
    "presentadas en sus ventanas correspondientes, se incluye al final la evidencia completa "
    "del trabajo de esos módulos, ejecutado sobre el mismo corpus (AG News provisto por la "
    "cátedra) y el mismo repositorio: el <b>Anexo A</b> contiene la Pre-entrega 2 completa "
    "(corpus preprocesado y EDA técnico, cuyo entregable original era un PDF), y los "
    "<b>Anexos B y C</b> contienen las ligas directas a los notebooks de las Pre-entregas 1 y 3 "
    "(cuyos slots piden URL de repositorio) junto con su evidencia mínima. El cuerpo principal "
    "del documento responde íntegramente a la consigna del Módulo 4; los anexos permiten "
    "verificar la cadena completa del proyecto y quedan a disposición del docente para la "
    "evaluación de los checkpoints previos si así lo considera. El repositorio público con todo "
    "el código, los notebooks ejecutados y las métricas en JSON está en: "
    f'<font color="#1155cc">{REPO_URL}</font>', "note"))

# ================= 1. RESUMEN DE ARQUITECTURA =================
story.append(P("1. Resumen de arquitectura", "h1"))
story.append(P("1.1 Problema, dataset y splits", "h2"))
story.append(P(
    "El proyecto clasifica noticias en 4 categorías (<b>World, Sports, Business, Sci_Tech</b>) "
    "sobre el corpus <b>AG News provisto por la cátedra</b>: 8.000 documentos de entrenamiento y "
    "2.000 de test, perfectamente balanceados (2.000 y 500 por clase respectivamente), sin nulos "
    "ni duplicados. Es el mismo corpus de toda la cadena del proyecto (Módulos 2, 3 y 4 y "
    "Proyecto Final), como exige la consigna."))
story.append(P(
    "<b>Protocolo de evaluación.</b> Del train se separa un 10% de validación estratificado "
    "(semilla 42), idéntico al usado en el Módulo 3. Toda decisión de configuración se toma "
    "contra validación; el <b>test set se evalúa una sola vez</b>, al final, en ambos modelos. "
    "La comparativa de la sección 3 usa por lo tanto el mismo <i>ag_news_test.csv</i> en las dos "
    "columnas."))
story.append(P("1.2 Modelo base elegido y justificación", "h2"))
story.append(P(
    "Se eligió <b>DistilBERT</b> (<i>distilbert-base-uncased</i>) por los dos criterios de la "
    "consigna: <b>idioma</b> — el corpus está en inglés y el modelo está preentrenado en inglés — "
    "y <b>límite de cómputo</b> — con ~67M de parámetros entrena en minutos en la GPU gratuita "
    "de Colab, mientras que un BERT base duplica el costo sin garantía de mejora en documentos "
    "cortos (el 95% de las noticias tiene 83 subword tokens o menos, ver §2.3)."))
story.append(P("1.3 Evidencia de entorno GPU", "h2"))
story.append(P(
    f"El fine-tuning se ejecutó en <b>Google Colab</b> sobre una GPU <b>{lora['gpu']}</b> "
    "(verificado con <i>torch.cuda.is_available()</i>). Versiones: "
    f"torch {lora['versiones']['torch']}, transformers {lora['versiones']['transformers']}, "
    f"peft {lora['versiones']['peft']}, datasets {lora['versiones']['datasets']}. "
    f"El notebook ejecutable está en el repositorio "
    f'(<font color="#1155cc">{NB}/04_finetuning_lora.ipynb</font>) y clona el propio repo para '
    "reproducir los datos y los splits."))

# ================= 2. CONFIGURACIÓN PEFT =================
story.append(P("2. Configuración PEFT (LoRA)", "h1"))
story.append(P("2.1 Parámetros de LoRA y argumentación", "h2"))
story.append(P(
    "<b>r = 8.</b> La tarea es una clasificación de tópicos con 4 clases y alta separabilidad "
    "léxica (el baseline clásico ya alcanza F1 0.896): no requiere adaptadores de gran "
    "capacidad. Con r = 8, cada proyección adaptada recibe dos matrices de rango bajo (768×8 y "
    "8×768) — capacidad suficiente para reorientar la atención sin re-aprender la lengua."))
story.append(P(
    "<b>lora_alpha = 16.</b> Fija una escala efectiva alpha/r = 2, valor conservador que evita "
    "que los adaptadores dominen sobre los pesos preentrenados congelados. "
    "<b>lora_dropout = 0.1</b> regulariza los adaptadores; con 7.200 ejemplos de entrenamiento "
    "el riesgo de sobreajuste existe pero es moderado, y la curva de §2.4 confirma que no se "
    "materializó."))
story.append(P("2.2 Módulos objetivo", "h2"))
story.append(P(
    "Los adaptadores se inyectaron únicamente en las proyecciones de <b>query</b> y <b>value</b> "
    "del mecanismo de atención — en DistilBERT, los módulos <b>q_lin</b> y <b>v_lin</b> de las 6 "
    "capas (en BERT/RoBERTa se llaman <i>query</i>/<i>value</i>). Es la configuración donde "
    "Hu et al. (2021) reportan el mejor ratio rendimiento/parámetros: adaptar <i>a qué "
    "atiende</i> el modelo (query) y <i>qué extrae</i> de ello (value) basta para re-especializar "
    "la atención a la tarea."))
story.append(P("2.3 Longitud máxima de secuencia medida con el tokenizador", "h2"))
story.append(P(
    "El percentil 95 de longitud calculado en el EDA del Módulo 2 (33 tokens) describe el texto "
    "<b>limpio y lematizado</b> — sin stop-words y con palabras completas. El Transformer "
    "consume el texto <b>crudo</b> en <b>subword tokens</b>: las stop-words vuelven y las "
    "palabras se parten. Por eso el max_len se recalculó con el propio tokenizador de "
    f"DistilBERT sobre el texto crudo de entrenamiento: <b>p95 = {lora['max_len_p95_subword']} "
    "subword tokens</b>, 2.5 veces el valor del EDA. Usar el número del Módulo 2 directamente "
    "habría truncado bastante más del 5% de los documentos."))
story.append(P("2.4 Análisis de parámetros: totales vs. entrenables", "h2"))
t = Table([
    ["Componente", "Parámetros"],
    ["Modelo completo (DistilBERT + cabeza)", f"{pa['totales']:,}"],
    ["Entrenables — total", f"{pa['entrenables']:,}"],
    ["   · Adaptadores LoRA (q_lin, v_lin × 6 capas)", f"{pa['lora']:,}"],
    ["   · Cabeza de clasificación (pre_classifier + classifier)", f"{pa['cabeza']:,}"],
    ["% entrenable", f"{pa['porcentaje_entrenable']:.2f}%  (criterio: < 3%)"],
], colWidths=[10.5 * cm, 5 * cm])
t.setStyle(TBL)
t.setStyle(TableStyle([("ALIGN", (0, 0), (0, -1), "LEFT"),
                       ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold")]))
story.append(t)
story.append(P(
    "El porcentaje entrenable (<b>1.09%</b>) incluye los adaptadores <b>y</b> la cabeza de "
    "clasificación, que PEFT marca entrenable con <i>TaskType.SEQ_CLS</i> porque se inicializa "
    "desde cero para las 4 clases del problema. El resto del modelo — embeddings, atención y "
    "feed-forward de las 6 capas — permanece congelado.", "body"))
story.append(P("2.5 Estadísticas de entrenamiento y tiempo", "h2"))
log = lora["log_history"]
tl = {e["epoch"]: e["loss"] for e in log if "loss" in e}
vl = {(e["epoch"]): (e["eval_loss"], e.get("eval_f1_weighted")) for e in log if "eval_loss" in e}
rows = [["Época", "Loss train", "Loss validación", "F1 weighted (val)"]]
for ep in sorted(tl):
    rows.append([f"{ep:.0f}", f4(tl[ep]), f4(vl[ep][0]), f4(vl[ep][1])])
t = Table(rows, colWidths=[2.5 * cm, 4 * cm, 4 * cm, 4.5 * cm])
t.setStyle(TBL)
story.append(t)
story.append(Spacer(1, 8))
story.append(img("m4_loss_curve.png", 12.5))
story.append(P("Figura 1 — Pérdida de entrenamiento vs. validación del fine-tuning con LoRA.", "cap"))
story.append(P(
    "Ambas pérdidas descienden de forma monótona y la de validación cierra por debajo de la de "
    "entrenamiento (0.237 vs. 0.253): en ningún punto se cruza hacia el sobreajuste — los "
    "adaptadores, con su dropout, regularizan lo suficiente. El F1 de validación es estable "
    "(~0.92) desde la primera "
    "época — coherente con una tarea de alta separabilidad léxica donde LoRA converge rápido. "
    f"<b>Tiempo total de entrenamiento: {lora['tiempo_entrenamiento_seg']:.1f} s "
    f"({lora['tiempo_entrenamiento_seg']/60:.1f} min)</b> para 3 épocas sobre 7.200 ejemplos en "
    "la T4."))

# ================= 3. RESULTADOS =================
story.append(P("3. Resultados y comparativa", "h1"))
story.append(P("3.1 Tabla comparativa: baseline clásico vs. Transformer + LoRA", "h2"))

def row(metric, a, b):
    return [metric, f4(a), f4(b), f"{b - a:+.4f}"]

rows = [["Métrica", "A · TF-IDF + LogReg (M3)", "B · DistilBERT + LoRA (M4)", "Delta"],
        row("Accuracy", ra["accuracy"], rb["accuracy"]),
        row("Precision (weighted)", ra["weighted avg"]["precision"], rb["weighted avg"]["precision"]),
        row("Recall (weighted)", ra["weighted avg"]["recall"], rb["weighted avg"]["recall"]),
        row("F1 (weighted)", ra["weighted avg"]["f1-score"], rb["weighted avg"]["f1-score"]),
        row("F1 (macro)", ra["macro avg"]["f1-score"], rb["macro avg"]["f1-score"]),
        ["Parámetros entrenables", f"{base['parametros_entrenables']:,}", f"{pa['entrenables']:,}",
         f"{pa['entrenables']/base['parametros_entrenables']:.0f}×"],
        ["Tiempo de entrenamiento", f"{base['tiempo_entrenamiento_seg']:.1f} s",
         f"{lora['tiempo_entrenamiento_seg']:.1f} s",
         f"{lora['tiempo_entrenamiento_seg']/base['tiempo_entrenamiento_seg']:.0f}×"]]
t = Table(rows, colWidths=[4.6 * cm, 4.2 * cm, 4.6 * cm, 2.1 * cm])
t.setStyle(TBL)
t.setStyle(TableStyle([("ALIGN", (0, 0), (0, -1), "LEFT"),
                       ("FONTNAME", (0, 4), (-1, 4), "Helvetica-Bold")]))
story.append(t)
story.append(P(
    "Ambas columnas se evaluaron sobre el mismo <i>ag_news_test.csv</i> (2.000 documentos, 500 "
    "por clase), cada modelo con su entrada idiomática: el baseline sobre el texto preprocesado "
    "del Módulo 2 (su representación óptima) y el Transformer sobre el texto crudo (su "
    "representación nativa). Al ser el corpus balanceado, F1 macro y weighted coinciden; se "
    "reportan ambos por criterio general.", "body"))

story.append(P("3.2 Métricas por clase y matrices de confusión", "h2"))
rows = [["Clase", "F1 · A (TF-IDF)", "F1 · B (LoRA)", "Delta"]]
for c in ["World", "Sports", "Business", "Sci_Tech"]:
    rows.append(row(c, ra[c]["f1-score"], rb[c]["f1-score"]))
t = Table(rows, colWidths=[3.5 * cm, 4.2 * cm, 4.2 * cm, 2.5 * cm])
t.setStyle(TBL)
t.setStyle(TableStyle([("ALIGN", (0, 0), (0, -1), "LEFT")]))
story.append(t)
story.append(Spacer(1, 8))
tt = Table([[img("m3_confusion.png", 7.9), img("m4_confusion.png", 7.9)]],
           colWidths=[8.2 * cm, 8.2 * cm])
tt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
story.append(tt)
story.append(P("Figura 2 — Matrices de confusión sobre el mismo test set: "
               "izquierda TF-IDF + LogReg (M3), derecha DistilBERT + LoRA (M4).", "cap"))
story.append(P(
    "La lectura conjunta muestra <b>dónde</b> gana el Transformer: Sci_Tech (+3.1 pp de F1, su "
    "recall pasa de 432/500 a 458/500), Sports (+1.9 pp, 489/500 aciertos) y World (+1.5 pp). "
    "El hallazgo honesto está en <b>Business</b>: su F1 <i>baja</i> ligeramente (−0.5 pp) y el "
    "cruce Business–Sci_Tech — el núcleo duro del problema — persiste intacto (83 errores "
    "cruzados en ambos modelos). El Transformer no eliminó esa frontera difusa; redistribuyó "
    "el resto del error. Es coherente con la naturaleza del corpus: una nota sobre resultados "
    "trimestrales de Microsoft es legítimamente ambigua entre Business y Sci_Tech incluso para "
    "un lector humano."))

story.append(P("3.3 Análisis de eficiencia: rendimiento vs. costo computacional", "h2"))
story.append(P(
    f"El Transformer con LoRA compra <b>+{(rb['weighted avg']['f1-score']-ra['weighted avg']['f1-score'])*100:.1f} "
    f"puntos porcentuales de F1</b> a cambio de "
    f"<b>{pa['entrenables']/base['parametros_entrenables']:.0f}× más parámetros entrenables</b> "
    f"({base['parametros_entrenables']:,} vs {pa['entrenables']:,}), "
    f"<b>~{lora['tiempo_entrenamiento_seg']/base['tiempo_entrenamiento_seg']:.0f}× más tiempo de "
    f"entrenamiento</b> ({base['tiempo_entrenamiento_seg']:.1f} s vs "
    f"{lora['tiempo_entrenamiento_seg']:.1f} s) y la dependencia de una GPU. En términos "
    "absolutos el costo sigue siendo bajo — 75 segundos en una GPU gratuita — precisamente "
    "porque LoRA congela el 98.9% del modelo: el mismo experimento con full fine-tuning "
    "entrenaría 67M de parámetros en lugar de 741K, con más memoria, más tiempo y riesgo de "
    "<i>catastrophic forgetting</i> con solo 7.200 ejemplos. La eficiencia de PEFT no está en "
    "ganar más puntos, sino en hacer asequible el punto que el enfoque clásico no alcanza."))

# ================= 4. CONCLUSIONES =================
story.append(P("4. Conclusiones", "h1"))
story.append(P("4.1 ¿Justifica el Transformer su costo frente al modelo clásico?", "h2"))
story.append(P(
    "<b>Depende del punto de operación, y este proyecto permite decirlo con números.</b> El "
    "baseline TF-IDF + Regresión Logística es un modelo excelente para este corpus: F1 0.896 "
    "entrenando en décimas de segundo en CPU, interpretable y barato de servir. El Transformer "
    "con LoRA lo supera con claridad (F1 0.910) y lo hace con un costo absoluto modesto gracias "
    "a PEFT. Si el caso de uso tolera ~1.5 pp menos de F1 — por ejemplo, un prototipo o un "
    "clasificador interno de bajo riesgo — el clásico sigue siendo defendible. Si cada punto de "
    "F1 importa (moderación, ruteo de contenido con volumen alto), LoRA entrega la mejora con "
    "una fracción despreciable del costo de un fine-tuning completo, que es exactamente el "
    "argumento de eficiencia del módulo."))
story.append(P("4.2 Limitaciones observadas", "h2"))
story.append(P(
    "(1) La frontera Business–Sci_Tech no se resolvió con atención contextual: probablemente "
    "requiera más datos de esa zona, etiquetas más finas o aceptar la ambigüedad inherente. "
    "(2) Todo el experimento corre con una sola semilla (42); las diferencias de décimas entre "
    "configuraciones no están acompañadas de intervalos. (3) Los documentos son cortos y el "
    "corpus es un subconjunto de 8.000 ejemplos: las conclusiones de eficiencia no se "
    "extrapolan a corpus largos (donde max_len y memoria dominan el costo). (4) No se exploró "
    "RoBERTa ni variantes de r/alpha; la configuración elegida se argumentó a priori y cumplió, "
    "pero un barrido corto habría cuantificado la sensibilidad."))

# ================= ANEXO A: P2 =================
story.append(PageBreak())
story.append(P("Anexo A — Pre-entrega 2: corpus preprocesado y EDA técnico", "h1"))
story.append(P(
    f'Contenido completo del Módulo 2. Notebook ejecutable: <font color="#1155cc">'
    f"{NB}/02_preprocesamiento_eda.ipynb</font>", "note"))
story.append(P("A.1 Pipeline de preprocesamiento", "h2"))
story.append(P(
    "La función <b>preprocess_text()</b> (módulo <i>src/preprocessing.py</i>) integra: "
    "(1) normalización a minúsculas; (2) <b>decodificación de entidades HTML</b> — el corpus "
    "trae tags codificados como «&amp;lt;A HREF=...&amp;gt;» y entidades <b>truncadas sin "
    "ampersand</b> («quot;», «#39;») —; (3) remoción Regex de los tags completos con sus "
    "atributos, del boilerplate bursátil de Reuters («(xyz.n: quote, profile, research)»), de "
    "URLs y de caracteres no alfabéticos; (4) lematización con SpaCy (<i>en_core_web_sm</i>, "
    "parser y NER deshabilitados); (5) filtro de stop-words y puntuación. El filtro de longitud "
    "conserva deliberadamente los tokens de 2 letras: en un corpus de noticias, «us», «uk» y "
    "«eu» son marcadores fuertes de la clase World, y eliminarlos sería el error de vocabulario "
    "de dominio que la consigna advierte."))
story.append(P(
    "<b>El EDA obligó a iterar el pipeline dos veces.</b> Primera pasada: el top 50 de "
    "palabras contenía «lt», «gt» y «quot» — entidades HTML sin limpiar. Segunda pasada: al "
    "borrar esas entidades quedaron expuestas las tripas de los tags en los n-gramas («href "
    "target», «font face verdana»), porque el corpus codifica tags completos. La solución fue "
    "decodificar primero y remover el tag entero. Este ciclo detectar-corregir-verificar es "
    "exactamente el propósito del EDA técnico."))
story.append(P("A.2 Longitud de documentos y percentil 95", "h2"))
story.append(img("m2_hist_tokens.png", 12.5))
story.append(P("Figura A1 — Distribución de tokens por documento (texto limpio); p95 = 33.", "cap"))
story.append(P(
    "El 95% de los documentos limpios tiene <b>33 tokens o menos</b>. Este número caracteriza "
    "el corpus para el modelado clásico; para el max_len del Módulo 4 se recalculó con el "
    "tokenizador subword del Transformer sobre texto crudo (p95 = 83, ver §2.3 del cuerpo)."))
story.append(P("A.3 N-gramas más frecuentes", "h2"))
story.append(img("m2_ngrams.png", 16))
story.append(P("Figura A2 — Top 20 bi-gramas y tri-gramas del corpus limpio.", "cap"))
story.append(P(
    "Los n-gramas confirman la calidad de la limpieza: «new york», «oil price», «united "
    "states», «prime minister» son unidades semánticas reales, sin restos de HTML. Lo que "
    "domina el conteo son los <b>datelines de agencia</b> («ap ap», «afp afp», «new york "
    "reuters», «canadian press canadian») — boilerplate de origen periodístico que es texto "
    "legítimo, transversal a las clases, y se documenta como artefacto aceptado en lugar de "
    "recortarse ad hoc."))
story.append(P("A.4 Top 50 palabras y control de stop-words", "h2"))
story.append(P(
    "De las 50 palabras más frecuentes del corpus limpio, solo <b>2 son stop-words</b> "
    "(«say», «take»). Se cuelan porque el filtro <i>is_stop</i> de SpaCy evalúa la forma "
    "superficial del token y no su lema («said» pasa el filtro y lematiza a «say»). Son "
    "frecuentes pero transversales a las clases, por lo que no comprometen el modelado. "
    "Persisten también las firmas de agencia («ap», «reuters»/«reuter») — la lematización no "
    "unifica nombres propios —, artefacto documentado y aceptado."))
story.append(P("A.5 Distribución de clases", "h2"))
story.append(img("m2_class_dist.png", 11))
story.append(P("Figura A3 — Documentos por categoría en train: balance perfecto (2.000 por clase).", "cap"))
story.append(P("A.6 Conclusión del EDA (300 palabras)", "h2"))
story.append(P(
    "El corpus son 8.000 noticias cortas: tras la limpieza, el 95% de los documentos tiene 33 "
    "tokens o menos. Esa brevedad es el principal desafío para el modelado — cada documento "
    "aporta poca evidencia léxica, así que conservar el vocabulario con carga semántica importa "
    "más que en corpus largos. Por eso el filtro de longitud conserva los tokens de 2 letras: "
    "«us», «uk» y «eu» son marcadores directos de la clase World. El EDA obligó a iterar el "
    "pipeline dos veces. Primera pasada: el top 50 de palabras contenía «lt», «gt» y «quot» — "
    "entidades HTML, muchas truncadas sin ampersand («quot;»). Segunda pasada: al borrar esas "
    "entidades quedaron expuestas las tripas de los tags en los n-gramas («href target», «font "
    "face verdana»), porque el corpus trae tags completos codificados. La solución fue "
    "decodificar primero y quitar el tag entero, más el boilerplate bursátil de Reuters. El top "
    "50 final quedó dominado por vocabulario de dominio («oil», «microsoft», «iraq», "
    "«president») con solo 2 stop-words residuales («say», «take»), que se cuelan porque "
    "is_stop evalúa la forma superficial y no el lema. Persisten las firmas de agencia («ap», "
    "«reuters»/«reuter», «afp») — la lematización no unifica nombres propios —, artefacto "
    "documentado, transversal a las clases y aceptado. La distribución de clases es "
    "perfectamente balanceada (2.000 documentos por categoría en train, 500 en test): accuracy "
    "es interpretable y F1 macro coincide con F1 weighted, aunque el proyecto reporta ambos. "
    "Los bi/tri-gramas más frecuentes («new york», «oil price», «prime minister») confirman "
    "unidades semánticas reales. Una decisión se difiere deliberadamente: el p95 aquí calculado "
    "(33) describe el texto limpio y lematizado; el max_len del Módulo 4 se recalculó con el "
    "tokenizador subword del Transformer sobre el texto crudo, porque son monedas distintas — "
    "las stop-words vuelven y las palabras se parten."))

# ================= ANEXO B: P1 =================
story.append(PageBreak())
story.append(P("Anexo B — Pre-entrega 1: pipeline de entrenamiento en PyTorch", "h1"))
story.append(P(
    f'<b>Liga para el slot de la Pre-entrega 1</b> (URL de repositorio): <font color="#1155cc">'
    f"{REPO_URL}</font><br/>Notebook directo: "
    f'<font color="#1155cc">{NB}/01_pipeline_base_pytorch.ipynb</font>', "note"))
story.append(P(
    "<b>Entorno:</b> PyTorch 2.14.0 · dispositivo con detección automática (cuda/mps/cpu; la "
    "corrida usó <i>mps</i>) · semillas fijas en random, numpy y torch (42) · Adam con "
    "<b>learning_rate = 1e-3</b> · 6 épocas. <b>Arquitectura:</b> MLP de una capa oculta (256 "
    "unidades, ReLU, dropout 0.3) sobre AG News vectorizado con TF-IDF de parámetros por "
    "defecto — la optimización del vectorizador es objeto del Módulo 3; usar el corpus real "
    "convierte esta entrega en el primer eslabón de la cadena. <b>Pipeline:</b> training loop "
    "explícito (forward → loss → backward → step) con <i>optimizer.zero_grad()</i> por "
    "iteración, y ciclo de validación separado bajo <i>model.eval()</i> + "
    "<i>torch.no_grad()</i>; el split de validación (10%, estratificado) sale del train y el "
    "test no se toca en este módulo."))
rows = [["Época", "Loss train", "Loss val", "F1 weighted (val)"]]
for ep, trl, vll, f1 in m1_hist:
    rows.append([ep, trl, vll, f1])
t = Table(rows, colWidths=[2.5 * cm, 4 * cm, 4 * cm, 4.5 * cm])
t.setStyle(TBL)
story.append(t)
story.append(Spacer(1, 8))
story.append(img("m1_loss_curve.png", 12.5))
story.append(P("Figura B1 — Curva de pérdida del Módulo 1 (train vs. validación).", "cap"))
story.append(P(
    "<b>Interpretación:</b> ambas curvas caen de forma monótona (train 1.31 → 0.15, validación "
    "1.14 → 0.28). Hasta la época 3 bajan juntas; después se abre una brecha creciente — "
    "sobreajuste incipiente que el dropout mantiene contenido, porque la pérdida de validación "
    "sigue bajando, no rebota. El F1 de validación se estabiliza en ~0.91 desde la tercera "
    "época y cierra en 0.9122: con este learning rate el modelo converge en ~3 épocas y "
    "entrenar más allá de 6 solo ensancharía la brecha sin ganancia real."))

# ================= ANEXO C: P3 =================
story.append(P("Anexo C — Pre-entrega 3: baseline supervisado con TF-IDF", "h1"))
story.append(P(
    f'<b>Liga para el slot de la Pre-entrega 3</b> (URL de repositorio): <font color="#1155cc">'
    f"{REPO_URL}</font><br/>Notebook directo: "
    f'<font color="#1155cc">{NB}/03_baseline_tfidf.ipynb</font>', "note"))
story.append(P(
    "El baseline reutiliza <i>preprocess_text()</i> del Módulo 2 sobre el mismo corpus. Se "
    "experimentaron tres configuraciones de <i>TfidfVectorizer</i> contra el split de "
    "validación (fit solo en train, transform en validación/test — sin data leakage):"))
exp = base["experimentos_validacion"]
rows = [["Config", "max_features", "ngram_range", "F1 weighted (val)"]]
for k in ["A", "B", "C"]:
    e = exp[k]
    rows.append([k, f"{e['max_features']:,}", str(tuple(e['ngram_range'])), f4(e["f1_val_weighted"])])
t = Table(rows, colWidths=[2.2 * cm, 4 * cm, 4 * cm, 4.8 * cm])
t.setStyle(TBL)
story.append(t)
story.append(P(
    "Ganó la configuración <b>B</b> por un margen mínimo (F1 0.9058 vs. 0.9046 de la A): con "
    "el texto ya limpio, los bigramas aportan una señal marginal pero real. C empata exactamente "
    "con B porque el vocabulario efectivo con min_df=2 (22.851 features en el split de "
    "experimentación) no llega al tope de 50.000 — subir max_features no agrega nada. El modelo "
    "final (B reentrenada sobre todo el train) usa <b>25.507 features, 102.032 parámetros y "
    "0.2 s de entrenamiento</b>. <b>Justificación del clasificador:</b> Regresión Logística "
    "maneja bien matrices dispersas de alta dimensión, expone probabilidades y coeficientes "
    "interpretables por clase, y es el baseline honesto contra el que medir al Transformer; "
    "Naive Bayes asume independencia entre features (falsa con n-gramas superpuestos) y una SVM "
    "lineal rinde parecido con más costo de ajuste."))
story.append(P(
    f"<b>Evaluación única en test:</b> accuracy {f4(ra['accuracy'])}, F1 weighted "
    f"{f4(ra['weighted avg']['f1-score'])}, F1 macro {f4(ra['macro avg']['f1-score'])} — en "
    "línea con la referencia verificada de la cátedra (F1 macro ~0.90 para AG News con "
    "LogisticRegression). Las categorías difíciles: <b>Business ↔ Sci_Tech</b> concentra el "
    "mayor cruce (38 + 45 = 83 errores: el léxico de resultados de empresas tecnológicas es "
    "ambiguo entre ambas), seguido de World ↔ Business (47: macroeconomía y geopolítica se "
    "solapan). Sports es casi limpia (F1 0.9534). La matriz de confusión del baseline está en "
    "la Figura 2 del cuerpo (izquierda) y el classification_report completo en "
    "<i>reports/metrics/baseline_tfidf.json</i>."))

# ================= ANEXO D =================
story.append(P("Anexo D — Repositorio y reproducibilidad", "h1"))
story.append(P(
    f'Repositorio público: <font color="#1155cc">{REPO_URL}</font>', "note"))
story.append(P(
    "El repositorio contiene los 4 notebooks ejecutados (con outputs visibles), el código "
    "compartido en <i>src/</i> (configuración y semillas, preprocesamiento, carga de datos y "
    "splits, training loop, métricas), los CSVs de la cátedra versionados, las figuras en "
    "<i>reports/figures/</i> y las métricas en JSON en <i>reports/metrics/</i>. El historial de "
    "commits sigue un mensaje por bloque (feat(m1)…feat(m4), docs)."))
story.append(P(
    "<b>Reproducción local</b> (Módulos 1–3): crear un entorno con Python ≥ 3.10, instalar "
    "<i>requirements.txt</i>, descargar el modelo de SpaCy (<i>python -m spacy download "
    "en_core_web_sm</i>) y correr los notebooks en orden. <b>Módulo 4:</b> abrir el notebook 04 "
    "en Google Colab con GPU y ejecutar todo; el notebook clona el repositorio, reproduce los "
    "splits (semilla 42) y exporta métricas y figuras. Librerías principales: torch ≥ 2.2, "
    "transformers ≥ 4.41, peft ≥ 0.10, datasets ≥ 2.19, scikit-learn ≥ 1.4, spacy ≥ 3.7 "
    "(versiones exactas de la corrida GPU en §1.3)."))

doc.build(story, )
size_mb = OUT.stat().st_size / 1e6
print(f"OK -> {OUT}  ({size_mb:.2f} MB)")
