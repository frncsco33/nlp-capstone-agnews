"""Genera NLP_Capstone_Salgado_Francisco.pdf — informe final del proyecto."""
import json
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
MET = REPO / "reports/metrics"
OUT = Path.home() / "Downloads/NLP_Capstone_Salgado_Francisco.pdf"
REPO_URL = "https://github.com/frncsco33/nlp-capstone-agnews"

base = json.load(open(MET / "baseline_tfidf.json"))
lora = json.load(open(MET / "lora_transformer.json"))
run = json.load(open(MET / "capstone_run.json"))
la = json.load(open(MET / "capstone_local_analysis.json"))
ra, rb = base["classification_report"], lora["classification_report"]
pa = lora["parametros"]
mc = run["mcnemar"]

ss = getSampleStyleSheet()
S = {
    "body": ParagraphStyle("body", parent=ss["Normal"], fontSize=10, leading=14.8,
                           alignment=4, spaceAfter=8),
    "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontSize=15, leading=19,
                         spaceBefore=18, spaceAfter=8, textColor=colors.HexColor("#1a1a2e")),
    "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12, leading=15,
                         spaceBefore=12, spaceAfter=5, textColor=colors.HexColor("#16324f")),
    "cap": ParagraphStyle("cap", parent=ss["Normal"], fontSize=8.5, leading=11,
                          alignment=1, textColor=colors.HexColor("#555555"),
                          spaceBefore=3, spaceAfter=11),
    "ref": ParagraphStyle("ref", parent=ss["Normal"], fontSize=9, leading=13,
                          alignment=0, leftIndent=14, firstLineIndent=-14, spaceAfter=4),
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
    w, h = PILImage.open(FIG / name).size
    return Image(str(FIG / name), width=width_cm * cm, height=width_cm * cm * h / w)

def f4(x):
    return f"{x:.4f}"

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawString(2 * cm, 1.2 * cm, "Salgado Francisco · Proyecto Final NLP · Comisión 90500")
    canvas.drawRightString(letter[0] - 2 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()

doc = BaseDocTemplate(str(OUT), pagesize=letter,
                      leftMargin=2 * cm, rightMargin=2 * cm,
                      topMargin=2 * cm, bottomMargin=2 * cm,
                      title="NLP Capstone — Clasificación de noticias con TF-IDF y LoRA",
                      author="Francisco Salgado")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="cover", frames=[frame]),
                      PageTemplate(id="page", frames=[frame], onPage=footer)])

story = []

# ================= PORTADA =================
story.append(Spacer(1, 3.2 * cm))
story.append(Paragraph("Data Science III: NLP &amp; Deep Learning aplicado a la Ciencia de Datos",
                       ParagraphStyle("c0", fontSize=11, alignment=1,
                                      textColor=colors.HexColor("#666666"))))
story.append(Spacer(1, 1.6 * cm))
story.append(Paragraph("Proyecto Final",
                       ParagraphStyle("c1", fontSize=30, leading=34, alignment=1,
                                      fontName="Helvetica-Bold",
                                      textColor=colors.HexColor("#16324f"))))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("Clasificación de noticias:<br/>del TF-IDF a los Transformers con LoRA",
                       ParagraphStyle("c2", fontSize=17, leading=23, alignment=1,
                                      fontName="Helvetica-Bold")))
story.append(Spacer(1, 0.7 * cm))
story.append(Paragraph("Informe técnico consolidado del proyecto capstone",
                       ParagraphStyle("c3", fontSize=12, alignment=1,
                                      textColor=colors.HexColor("#444444"))))
story.append(Spacer(1, 4.2 * cm))
meta = Table([
    ["Alumno", "Francisco Salgado"],
    ["Comisión", "90500"],
    ["Fecha", "Septiembre de 2026"],
    ["Código y evidencia", REPO_URL],
], colWidths=[3.8 * cm, 11 * cm])
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

# ================= 1. PROBLEMA =================
story.append(P("1. El problema y el dataset", "h1"))
story.append(P(
    "Este proyecto responde una pregunta que me acompañó durante todo el curso: cuando ya "
    "tienes un clasificador clásico que funciona bien, ¿cuánto vale realmente dar el salto a "
    "un Transformer? No en abstracto, sino con números sobre la mesa: cuántos puntos de F1 "
    "compra el salto, cuánto cómputo cuesta, y en qué tipo de documentos se nota la "
    "diferencia."))
story.append(P(
    "El terreno de juego es <b>AG News</b>, el corpus provisto por la cátedra: 8.000 noticias "
    "de entrenamiento y 2.000 de test, repartidas en cuatro secciones (World, Sports, Business "
    "y Sci_Tech) con balance perfecto de 2.000 y 500 documentos por clase. Son noticias "
    "cortas, de agencia, con título y primer párrafo. El problema es el de un ruteador "
    "editorial automático: leer la nota y decidir a qué sección pertenece. Un caso de negocio "
    "directo sería la clasificación automática de contenido en un agregador de noticias, donde "
    "cada error manda una nota de tecnología a la sección de finanzas."))
story.append(P(
    "Sobre este corpus construí las dos soluciones que el informe compara de punta a punta: un "
    "baseline de TF-IDF con Regresión Logística (Módulo 3) y un DistilBERT ajustado con "
    "adaptadores LoRA (Módulo 4). Todo el proyecto corre con semilla 42, el split de "
    "validación es el mismo para ambos modelos (10% del train, estratificado) y el test de "
    "2.000 documentos se evaluó una sola vez por modelo. Aunque el balance perfecto del corpus "
    "hace que accuracy sea interpretable, todas las decisiones se tomaron sobre F1 ponderado, "
    "y reporto también el macro."))

# ================= 2. PIPELINE =================
story.append(P("2. Pipeline de preprocesamiento: dos monedas distintas", "h1"))
story.append(P(
    "Una de las cosas que más me ordenó la cabeza en este proyecto fue aceptar que los dos "
    "modelos no comen lo mismo. El clásico necesita un texto destilado a lemas informativos; "
    "el Transformer quiere el texto crudo, porque su tokenizador subword y sus embeddings "
    "preentrenados ya saben lidiar con flexiones, stop-words y palabras raras. Preprocesar "
    "igual para ambos habría sido cómodo, pero subóptimo para los dos."))
story.append(P("2.1 La rama clásica: limpieza estructural y lematización", "h2"))
story.append(P(
    "Para TF-IDF armé un pipeline con SpaCy (en_core_web_sm) que normaliza a minúsculas, "
    "limpia estructura, lematiza y filtra stop-words. La limpieza me costó dos iteraciones, y "
    "las dos las detectó el propio EDA. En la primera pasada, el top 50 de palabras traía "
    "'lt', 'gt' y 'quot': entidades HTML, muchas truncadas sin ampersand ('quot;'), que mi "
    "regex no cubría. Las borré y el problema cambió de lugar: en los n-gramas aparecieron "
    "'href target' y 'font face verdana'. Resulta que el corpus trae tags completos "
    "codificados como entidades, y al borrar solo los delimitadores dejé las tripas del tag "
    "como si fueran texto. La solución fue invertir el orden: primero decodificar las "
    "entidades a sus caracteres, y entonces sí remover el tag entero con sus atributos, junto "
    "con el boilerplate bursátil de Reuters y las URLs. Ese ciclo de detectar, corregir y "
    "verificar es, visto en retrospectiva, el mejor argumento a favor de hacer un EDA técnico "
    "en serio."))
story.append(P(
    "Dos decisiones finas del filtro léxico: conservé los tokens de dos letras porque 'us', "
    "'uk' y 'eu' son marcadores directos de la clase World, y acepté como artefacto documentado "
    "las firmas de agencia ('ap', 'reuters', 'afp'), que son texto legítimo y transversal a las "
    "clases. Tras la limpieza, el 95% de los documentos quedó en 33 tokens o menos, y de las 50 "
    "palabras más frecuentes solo 2 son stop-words residuales ('say' y 'take', que se cuelan "
    "porque el filtro evalúa la forma superficial y no el lema)."))
story.append(P("2.2 La rama Transformer: subword sobre texto crudo", "h2"))
story.append(P(
    "DistilBERT usa el tokenizador WordPiece de BERT: descompone cualquier palabra en subword "
    "tokens de un vocabulario de ~30.000 piezas, agrega los tokens especiales [CLS] al inicio "
    "(cuyo embedding final alimenta la cabeza de clasificación) y [SEP] al cierre, y el "
    "padding se aplica dinámicamente por batch hasta la secuencia más larga del lote "
    "(DataCollatorWithPadding), con truncado en max_len."))
story.append(P(
    "Aquí hay una trampa en la que casi caigo y que vale la pena dejar escrita. El percentil "
    "95 de longitud que calculé en el EDA (33 tokens) describe el texto limpio y lematizado. "
    "El Transformer tokeniza el texto crudo, donde las stop-words vuelven y las palabras se "
    "parten en piezas. Medido con el propio tokenizador de DistilBERT, el p95 real es de "
    f"<b>{lora['max_len_p95_subword']} subword tokens</b>: 2.5 veces el número del EDA. Si "
    "hubiera usado 33 como max_len habría truncado mucho más del 5% de los documentos sin "
    "enterarme. La moraleja: cada representación se mide con su propia regla."))

# ================= 3. BASELINE =================
story.append(P("3. El baseline: TF-IDF + Regresión Logística", "h1"))
story.append(P(
    "Probé tres configuraciones del vectorizador contra el split de validación, con el fit "
    "siempre restringido al train para no filtrar información del test (el clásico data "
    "leakage que la consigna advierte):"))
exp = base["experimentos_validacion"]
rows = [["Config", "max_features", "ngram_range", "F1 weighted (validación)"]]
for k in ["A", "B", "C"]:
    e = exp[k]
    rows.append([k, f"{e['max_features']:,}", str(tuple(e["ngram_range"])), f4(e["f1_val_weighted"])])
t = Table(rows, colWidths=[2.2 * cm, 4 * cm, 4 * cm, 4.8 * cm])
t.setStyle(TBL)
story.append(t)
story.append(P(
    "Ganó la B por poco: los bigramas aportan una señal chica pero real una vez que el texto "
    "está limpio. La C empata exactamente con la B porque el vocabulario efectivo con min_df=2 "
    "no llega al tope de 50.000 features, así que subir el límite no cambia nada. El modelo "
    "final usa 25.507 features y 102.032 parámetros, y entrena en 0.2 segundos en CPU."))
story.append(P(
    "Elegí Regresión Logística sobre Naive Bayes y SVM por una razón práctica: maneja bien "
    "matrices dispersas de alta dimensión, expone probabilidades, y sus coeficientes se leen "
    "por clase. Esa interpretabilidad no es decorativa; la tabla siguiente muestra qué aprendió "
    "el modelo, y es un retrato bastante fiel del vocabulario de cada sección:"))
tops = la["top_features_por_clase"]
rows = [["Clase", "Features con mayor peso (coeficientes de la Regresión Logística)"]]
for name in ["World", "Sports", "Business", "Sci_Tech"]:
    rows.append([name, ", ".join(tops[name][:10])])
t = Table(rows, colWidths=[2.8 * cm, 13.2 * cm])
t.setStyle(TBL)
t.setStyle(TableStyle([("ALIGN", (1, 0), (1, -1), "LEFT"), ("FONTSIZE", (1, 1), (1, -1), 8.5)]))
story.append(t)
story.append(P(
    f"Sobre el test, evaluado una única vez: <b>accuracy {f4(ra['accuracy'])}, F1 ponderado "
    f"{f4(ra['weighted avg']['f1-score'])}, F1 macro {f4(ra['macro avg']['f1-score'])}</b>, en "
    "línea con la referencia que la propia cátedra reporta para este corpus (~0.90). Un "
    "baseline serio, que es justo lo que uno quiere antes de justificar un Transformer."))

# ================= 4. SOLUCIÓN AVANZADA =================
story.append(P("4. La solución avanzada: DistilBERT con adaptadores LoRA", "h1"))
story.append(P("4.1 Modelo base y mecánica del ajuste", "h2"))
story.append(P(
    "Elegí <b>distilbert-base-uncased</b> por las dos variables que importaban: el corpus está "
    "en inglés y el modelo está preentrenado en inglés, y con ~67M de parámetros entrena en "
    "minutos en la GPU gratuita de Colab (una Tesla T4), donde un BERT base duplica el costo "
    "sin garantía de mejora en documentos tan cortos."))
story.append(P(
    "En lugar de ajustar los 67 millones de parámetros, LoRA congela el modelo completo "
    "(embeddings, las 6 capas de atención con sus 12 attention heads cada una, y las capas "
    "feed-forward) e inyecta en las proyecciones de query y value de cada capa un par de "
    "matrices de <b>rango 8</b>: una de 768×8 y otra de 8×768. Durante el entrenamiento, la "
    "backpropagation solo fluye gradientes hacia esos adaptadores y hacia la cabeza de "
    "clasificación, que se inicializa desde cero para las 4 clases. El factor de escala "
    "lora_alpha=16 fija una relación alpha/r de 2, lo bastante conservadora para que los "
    "adaptadores corrijan la atención sin pisar lo que el modelo ya sabe del idioma."))
rows = [["Componente", "Parámetros"],
        ["Modelo completo (congelado + entrenable)", f"{pa['totales']:,}"],
        ["Entrenables en total", f"{pa['entrenables']:,}"],
        ["   · Adaptadores LoRA (q_lin y v_lin, 6 capas)", f"{pa['lora']:,}"],
        ["   · Cabeza de clasificación", f"{pa['cabeza']:,}"],
        ["Fracción entrenable", f"{pa['porcentaje_entrenable']:.2f}%"]]
t = Table(rows, colWidths=[10.5 * cm, 5 * cm])
t.setStyle(TBL)
t.setStyle(TableStyle([("ALIGN", (0, 0), (0, -1), "LEFT"),
                       ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold")]))
story.append(t)
story.append(P("4.2 Ciclo de entrenamiento", "h2"))
story.append(P(
    "El entrenamiento corre en PyTorch a través del Trainer de Hugging Face: optimizador AdamW "
    "con learning rate 2e-4 (LoRA tolera tasas más altas que un fine-tuning completo, porque "
    "los pesos preentrenados no se mueven), batch de 32, 3 épocas, precisión mixta fp16 y "
    "validación al cierre de cada época contra el split del 10%, nunca contra el test. La "
    f"corrida completa tomó <b>{lora['tiempo_entrenamiento_seg']:.1f} segundos</b> en la T4."))
log = lora["log_history"]
tl = {e["epoch"]: e["loss"] for e in log if "loss" in e}
vl = {e["epoch"]: (e["eval_loss"], e.get("eval_f1_weighted")) for e in log if "eval_loss" in e}
rows = [["Época", "Loss train", "Loss validación", "F1 weighted (val)"]]
for ep in sorted(tl):
    rows.append([f"{ep:.0f}", f4(tl[ep]), f4(vl[ep][0]), f4(vl[ep][1])])
t = Table(rows, colWidths=[2.5 * cm, 4 * cm, 4 * cm, 4.5 * cm])
t.setStyle(TBL)
story.append(t)
story.append(Spacer(1, 6))
story.append(img("m4_loss_curve.png", 11.5))
story.append(P("Figura 1. Pérdida de entrenamiento y validación del ajuste con LoRA.", "cap"))
story.append(P(
    "Las dos curvas bajan juntas y la de validación cierra por debajo de la de entrenamiento "
    "(0.237 contra 0.253), señal de que el dropout de los adaptadores y el congelamiento del "
    "resto del modelo mantienen el sobreajuste a raya. El F1 de validación ronda 0.92 desde la "
    "primera época: con la mayor parte del conocimiento ya preentrenado, al modelo le basta "
    "muy poco para re-especializar su atención a esta tarea."))
story.append(P(
    "Para el análisis de interpretabilidad de la sección 6 reentrené el modelo con la misma "
    "semilla y configuración, y el F1 de test reprodujo el de la corrida original casi al "
    f"diezmilésimo ({f4(run['f1_weighted_test'])} contra {f4(rb['weighted avg']['f1-score'])}). "
    "Que el experimento se repita y dé lo mismo era un requisito que me impuse desde el "
    "Módulo 1, y aquí rindió frutos."))

# ================= 5. EVALUACIÓN COMPARATIVA =================
story.append(P("5. Evaluación comparativa", "h1"))
story.append(P(
    "Los dos modelos se evaluaron sobre el mismo ag_news_test.csv de 2.000 documentos, cada "
    "uno con su entrada idiomática: el baseline sobre el texto preprocesado y el Transformer "
    "sobre el crudo. Mismo test, misma única evaluación final."))

def row(metric, a, b):
    return [metric, f4(a), f4(b), f"{b - a:+.4f}"]

rows = [["Métrica", "TF-IDF + LogReg", "DistilBERT + LoRA", "Diferencia"],
        row("Accuracy", ra["accuracy"], rb["accuracy"]),
        row("Precision (weighted)", ra["weighted avg"]["precision"], rb["weighted avg"]["precision"]),
        row("Recall (weighted)", ra["weighted avg"]["recall"], rb["weighted avg"]["recall"]),
        row("F1 (weighted)", ra["weighted avg"]["f1-score"], rb["weighted avg"]["f1-score"]),
        row("F1 (macro)", ra["macro avg"]["f1-score"], rb["macro avg"]["f1-score"]),
        ["Parámetros entrenables", f"{base['parametros_entrenables']:,}", f"{pa['entrenables']:,}",
         f"{pa['entrenables'] / base['parametros_entrenables']:.0f}×"],
        ["Tiempo de entrenamiento", f"{base['tiempo_entrenamiento_seg']:.1f} s (CPU)",
         f"{lora['tiempo_entrenamiento_seg']:.1f} s (GPU T4)",
         f"{lora['tiempo_entrenamiento_seg'] / base['tiempo_entrenamiento_seg']:.0f}×"]]
t = Table(rows, colWidths=[4.6 * cm, 4.3 * cm, 4.6 * cm, 2.4 * cm])
t.setStyle(TBL)
t.setStyle(TableStyle([("ALIGN", (0, 0), (0, -1), "LEFT"),
                       ("FONTNAME", (0, 4), (-1, 4), "Helvetica-Bold")]))
story.append(t)
story.append(Spacer(1, 4))
rows = [["Clase", "F1 · TF-IDF", "F1 · LoRA", "Diferencia"]]
for c in ["World", "Sports", "Business", "Sci_Tech"]:
    rows.append(row(c, ra[c]["f1-score"], rb[c]["f1-score"]))
t = Table(rows, colWidths=[3.5 * cm, 4.2 * cm, 4.2 * cm, 2.8 * cm])
t.setStyle(TBL)
t.setStyle(TableStyle([("ALIGN", (0, 0), (0, -1), "LEFT")]))
story.append(t)
story.append(Spacer(1, 8))
tt = Table([[img("m3_confusion.png", 7.9), img("m4_confusion.png", 7.9)]],
           colWidths=[8.2 * cm, 8.2 * cm])
tt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
story.append(tt)
story.append(P("Figura 2. Matrices de confusión sobre el mismo test: TF-IDF (izquierda) y "
               "DistilBERT + LoRA (derecha).", "cap"))
story.append(P("5.1 ¿La diferencia es real? Prueba de McNemar", "h2"))
story.append(P(
    "Con una mejora de 1.5 puntos, la pregunta obligada es si no será ruido de muestreo. Para "
    "responderla crucé las predicciones de ambos modelos documento por documento:"))
rows = [["", "LoRA acierta", "LoRA falla"],
        ["TF-IDF acierta", f"{mc['ambos_aciertan']:,}", f"{mc['solo_tfidf']}"],
        ["TF-IDF falla", f"{mc['solo_lora']}", f"{mc['ambos_fallan']}"]]
t = Table(rows, colWidths=[4 * cm, 4 * cm, 4 * cm])
t.setStyle(TBL)
t.setStyle(TableStyle([("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                       ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#16324f")),
                       ("TEXTCOLOR", (0, 1), (0, -1), colors.white)]))
story.append(t)
story.append(P(
    f"En los {mc['solo_tfidf'] + mc['solo_lora']} documentos donde los modelos discrepan, LoRA "
    f"gana {mc['solo_lora']} a {mc['solo_tfidf']}. La prueba exacta de McNemar sobre esos "
    "desacuerdos da <b>p = 0.022</b>: la ventaja del Transformer es estadísticamente "
    "significativa al 5%, no un accidente de este test set. Igual de informativo es el otro "
    f"rincón de la tabla: {mc['ambos_fallan']} documentos donde fallan los dos, un piso de "
    "error compartido sobre el que vuelvo en la sección 6."))
story.append(P("5.2 Eficiencia: qué compra el costo", "h2"))
story.append(P(
    f"La mejora cuesta {pa['entrenables'] / base['parametros_entrenables']:.0f} veces más "
    f"parámetros entrenables, {lora['tiempo_entrenamiento_seg'] / base['tiempo_entrenamiento_seg']:.0f} "
    "veces más tiempo de entrenamiento y una GPU. Dicho así suena caro; en términos absolutos "
    "son 75 segundos en una GPU gratuita, y ese costo tan contenido es mérito de LoRA: el "
    "98.9% del modelo está congelado. Un fine-tuning completo habría movido los 67 millones de "
    "parámetros, con más memoria, más tiempo y riesgo real de catastrophic forgetting con "
    "apenas 7.200 ejemplos. La aportación de PEFT no es ganar más puntos, es volver asequible "
    "el punto que el enfoque clásico no alcanza."))

# ================= 6. EL PORQUÉ =================
story.append(P("6. El porqué: cobertura, ambigüedad y lo que vio la atención", "h1"))
story.append(P(
    "Hasta aquí los números dicen qué modelo gana. Esta sección es mi intento de explicar por "
    "qué, y el camino tuvo una sorpresa: la explicación que yo traía en la cabeza resultó "
    "falsa."))
story.append(P("6.1 La cobertura de vocabulario no es la explicación", "h2"))
story.append(P(
    "Mi hipótesis inicial era de libro de texto: TF-IDF falla porque su vocabulario es "
    "cerrado, y las palabras del test que no vio en el train lo dejan ciego, mientras que el "
    "subword del Transformer cubre todo. Medirlo la desmontó. Solo el 7.6% de los tokens del "
    "test queda fuera del vocabulario del TF-IDF, y la tasa de fuera-de-vocabulario es "
    "prácticamente idéntica en los documentos que el baseline acierta (7.8%) y en los que "
    "falla (7.8%). La cobertura no distingue a los errores. En este corpus, con noticias del "
    "mismo dominio en train y test, el problema del baseline no es el vocabulario que le "
    "falta: es el vocabulario que las clases comparten."))
story.append(img("cap_jaccard_pares.png", 12.5))
story.append(P("Figura 3. Solapamiento del vocabulario dominante (top-300 de frecuencia) "
               "entre pares de clases.", "cap"))
story.append(P(
    "El par Business–Sci_Tech comparte el 35% de su vocabulario dominante, casi el doble que "
    "cualquier otro par. Y ahí es exactamente donde viven los errores: es el mayor cruce de la "
    "matriz de confusión en ambos modelos (83 errores cruzados en cada uno), y cuando desglosé "
    f"los {mc['solo_lora']} documentos que solo LoRA acierta, el bloque más grande (23) son "
    "notas de Sci_Tech que el TF-IDF mandó a Business. Una bolsa de palabras sabe con qué "
    "palabras está escrita la nota, pero no de qué habla; cuando dos secciones escriben con "
    "las mismas palabras, ese modelo se queda sin herramientas. La semántica de la secuencia, "
    "el orden y el contexto que la atención sí procesa, es la información que desempata."))
story.append(P(
    "La longitud cuenta una historia complementaria: el baseline falla más en los documentos "
    "muy cortos (13.8% de error en el primer cuartil, donde hay poca evidencia léxica) y en "
    "los muy largos (12.1%, donde se mezclan temas), con su mejor zona en el medio."))
story.append(img("cap_error_longitud.png", 10.5))
story.append(P("Figura 4. Tasa de error del baseline por cuartil de longitud del documento.", "cap"))
story.append(P("6.2 Interpretabilidad: tres documentos vistos por dentro", "h2"))
story.append(P(
    "Para abrir la caja negra tomé los documentos donde TF-IDF falla y LoRA acierta, y extraje "
    "la atención que el token [CLS] (el que decide la clase) reparte sobre el texto en la "
    "última capa, promediando las 12 cabezas. En las figuras, el fondo más intenso marca los "
    "tokens más atendidos. Dos notas de honestidad metodológica: la puntuación y los "
    "separadores absorben parte de la atención (un fenómeno conocido de los Transformers), así "
    "que la lectura útil está en los tokens con contenido; y en algunos textos se asoman "
    "restos de HTML ('lt', '#39'), porque el Transformer trabaja sobre el texto crudo, como "
    "quedó dicho en la sección 2, y aun con ese ruido a cuestas resuelve la clase."))
story.append(P(
    "<b>Caso 1: la sonda que quebró.</b> El titular dice 'Money woes foiled Beagle 2': un "
    "reporte culpa al gobierno británico de no financiar a tiempo la sonda marciana Beagle 2. "
    "Para el TF-IDF, 'money', 'funds' y 'loss' son features con peso en Business y ahí la "
    "mandó, con una confianza tibia de 0.35. La etiqueta real es Sci_Tech y LoRA la acertó con "
    "0.91. En su mapa de atención conviven las dos lecturas: pesa 'funds' y 'money', pero "
    "también 'mars', 'probe' y 'blames', y la representación conjunta resuelve que el dinero "
    "es la circunstancia, no el tema."))
story.append(img("cap_att_beagle.png", 15.5))
story.append(P("Figura 5. Atención del [CLS] (última capa, promedio de cabezas). Real: "
               "Sci_Tech · TF-IDF: Business (conf. 0.35) · LoRA: Sci_Tech (conf. 0.91).", "cap"))
story.append(P(
    "<b>Caso 2: la confusión también corre al revés.</b> Una nota sobre el programa de "
    "colegiaturas prepagadas de Florida es Business, pero el TF-IDF la clasificó Sci_Tech. Al "
    "revisar por qué, encontré algo mejor que una intuición: las dos palabras que definen la "
    "nota, 'tuition' y 'prepaid', ni siquiera existen en el vocabulario del TF-IDF (aparecen "
    "tan poco en el train que el min_df las poda), así que el modelo decidió con lo que "
    "tenía, y lo que tenía empuja a Sci_Tech: 'program' pesa +0.92 hacia esa clase en los "
    "coeficientes, contra -0.67 hacia Business. La atención de LoRA, que sí puede leer "
    "'tuition' y 'prepaid' gracias al subword, se concentra justo ahí y devuelve la nota a "
    "Business. Es el matiz que le faltaba a la sección 6.1: la cobertura no explica el patrón "
    "agregado de errores, pero en casos puntuales como este sí puso su parte."))
story.append(img("cap_att_tuition.png", 15.5))
story.append(P("Figura 6. Real: Business · TF-IDF: Sci_Tech (conf. 0.47) · LoRA: Business (conf. 0.80).", "cap"))
story.append(P(
    "<b>Caso 3: palabras de nota roja en la sección de deportes.</b> 'Hundreds mourn loss of "
    "student killed by police during Red Sox celebrations'. El léxico grita World: 'killed', "
    "'police', 'mourn'. El TF-IDF obedeció al léxico. La nota es de Sports (el contexto es la "
    "celebración del título de los Red Sox) y la atención de LoRA lo delata: 'sox', 'red', "
    "'college' y el nombre propio de la estudiante pesan junto a las palabras trágicas, y el "
    "modelo lee el evento, no solo el tono."))
story.append(img("cap_att_redsox.png", 15.5))
story.append(P("Figura 7. Real: Sports · TF-IDF: World (conf. 0.45) · LoRA: Sports (conf. 0.99).", "cap"))
story.append(P(
    "Un patrón cuantitativo respalda estos tres retratos: en los 90 documentos que solo LoRA "
    "acierta, la confianza media del TF-IDF al fallar era de 0.45 (dudaba entre clases), "
    "mientras que LoRA los resolvió con 0.75. El clásico no se equivocaba con seguridad: se "
    "quedaba sin evidencia léxica para decidir. Justo el hueco que el contexto llena."))

# ================= 7. CONCLUSIONES =================
story.append(P("7. Conclusiones, limitaciones y líneas futuras", "h1"))
story.append(P("7.1 Conclusiones", "h2"))
story.append(P(
    "La pregunta del proyecto tiene respuesta con números. El Transformer con LoRA supera al "
    f"baseline en {(rb['weighted avg']['f1-score'] - ra['weighted avg']['f1-score']) * 100:.1f} "
    "puntos de F1 ponderado (0.9101 contra 0.8955), la ventaja es estadísticamente "
    "significativa (McNemar, p = 0.022), y se concentra donde la teoría predice: en la "
    "frontera léxicamente ambigua entre Business y Sci_Tech, en documentos donde el baseline "
    "dudaba. Y la gana con el 1.09% de los parámetros entrenables y 75 segundos de GPU, que es "
    "el argumento central de los métodos PEFT."))
story.append(P(
    "¿Se justifica siempre? No. El baseline entrena en 0.2 segundos en CPU, se sirve barato, "
    "sus coeficientes se auditan a simple vista, y para un prototipo o un clasificador interno "
    "de bajo riesgo sigue siendo una elección defendible. Si cada punto de F1 importa, si el "
    "volumen amortiza la GPU, o si el dominio está lleno de casos como los de la sección 6.2, "
    "el salto está pagado. Lo que este proyecto me deja es la disciplina de tomar esa decisión "
    "con evidencia y no con moda."))
story.append(P("7.2 Limitaciones", "h2"))
story.append(P(
    "Primera: parte del error es irreducible con estas etiquetas. De los 119 documentos donde "
    "fallan ambos modelos, varios tienen etiquetas discutibles; mi ejemplo favorito es un "
    "'World briefs' fechado en Londres, con un ataque con machete a guardias de seguridad, "
    "etiquetado Business. Los dos modelos leyeron World, y la atención muestra por qué: no hay "
    "señal de negocios que atender. Ese piso compartido de ~6% incluye ruido de etiquetado y "
    "ambigüedad genuina, y ningún modelo lo va a bajar solo con más capacidad."))
story.append(img("cap_att_worldbriefs.png", 15.5))
story.append(P("Figura 8. Documento etiquetado Business que ambos modelos clasifican World. "
               "La atención no encuentra señal de negocios que mirar.", "cap"))
story.append(P(
    "Segunda: todo corre con una sola semilla; el McNemar respalda la comparación central, "
    "pero las diferencias chicas entre configuraciones (los 0.001 entre vectorizadores, por "
    "ejemplo) no tienen intervalos. Tercera: el corpus es un subconjunto de 8.000 noticias "
    "cortas de 2004; las conclusiones de eficiencia no viajan a documentos largos, donde el "
    "costo cuadrático de la atención con la longitud cambia la aritmética. Cuarta: no barrí "
    "alternativas de rango ni de modelo base; r=8 y DistilBERT se argumentaron a priori y "
    "cumplieron, pero un barrido corto habría cuantificado la sensibilidad."))
story.append(P("7.3 Líneas futuras", "h2"))
story.append(P(
    "Tres caminos concretos. Probar RoBERTa-base con la misma receta, que suele rendir 1 o 2 "
    "puntos más en clasificación a cambio del doble de cómputo. Explotar la tabla de McNemar "
    "en producción: un sistema híbrido que sirva el TF-IDF (barato) y escale al Transformer "
    "solo los documentos donde el clásico duda, usando su confianza como umbral; con los "
    "números de este proyecto, eso captura la mayor parte de la mejora a una fracción del "
    "costo. Y auditar las etiquetas de la zona Business–Sci_Tech, porque parte del techo no "
    "está en los modelos sino en el dato."))
story.append(P("7.4 Referencias", "h2"))
for ref in [
    "Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L. y Chen, W. "
    "(2021). LoRA: Low-Rank Adaptation of Large Language Models. arXiv:2106.09685.",
    "Sanh, V., Debut, L., Chaumond, J. y Wolf, T. (2019). DistilBERT, a distilled version of "
    "BERT: smaller, faster, cheaper and lighter. arXiv:1910.01108.",
    "Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L. "
    "y Polosukhin, I. (2017). Attention Is All You Need. NeurIPS 2017.",
    "Zhang, X., Zhao, J. y LeCun, Y. (2015). Character-level Convolutional Networks for Text "
    "Classification. NeurIPS 2015 (origen del corpus AG News).",
    "Devlin, J., Chang, M.-W., Lee, K. y Toutanova, K. (2019). BERT: Pre-training of Deep "
    "Bidirectional Transformers for Language Understanding. NAACL 2019.",
    "Wolf, T. et al. (2020). Transformers: State-of-the-Art Natural Language Processing. "
    "EMNLP 2020 (librería Hugging Face).",
    "Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12.",
]:
    story.append(P(ref, "ref"))
story.append(Spacer(1, 8))
story.append(P(
    "<i>Nota de reproducibilidad: el código completo del proyecto (notebooks ejecutados, "
    "pipeline, métricas en JSON y figuras) está versionado en " + REPO_URL + ", como material "
    "complementario de este informe. Semilla global 42; versiones: torch "
    f"{lora['versiones']['torch']}, transformers {lora['versiones']['transformers']}, peft "
    f"{lora['versiones']['peft']}, scikit-learn 1.9, spacy 3.8.</i>", "body"))

doc.build(story)
print(f"OK -> {OUT}  ({OUT.stat().st_size / 1e6:.2f} MB)")
