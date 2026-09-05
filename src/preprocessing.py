"""Pipeline de preprocesamiento: limpieza Regex + normalización + lematización SpaCy."""
import html
import re

import spacy

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# El corpus trae tags HTML codificados como entidades (&lt;A HREF="..."&gt;) y también
# entidades truncadas sin ampersand ("quot;", "#39;"). El orden importa: primero se
# DECODIFICAN las entidades a sus caracteres para que el tag quede completo (<a ...>)
# y la remoción de tags se lleve también sus atributos (href, target, font face...).
# Quitar las entidades sin decodificar deja las tripas del tag como texto — lo detectó
# el EDA del Módulo 2 cuando "href target" y "font face verdana" aparecieron en el
# top de n-gramas.
RE_BARE_LT = re.compile(r"\blt;")
RE_BARE_GT = re.compile(r"\bgt;")
RE_BARE_AMP = re.compile(r"\bamp;")
RE_BARE_ENTITY = re.compile(r"\b(?:quot|apos|nbsp);|#\d+;")
RE_HTML = re.compile(r"<[^>]*>")
RE_HTML_OPEN = re.compile(r"<[^>]*$")          # tag sin cerrar en docs truncados
RE_REUTERS = re.compile(r"\([a-z0-9.,&; ]*:\s*quote,\s*profile,\s*research\s*\)")
RE_URL = re.compile(r"http\S+|www\.\S+")
RE_NOISE = re.compile(r"[^a-z\s]")
RE_WS = re.compile(r"\s+")

# El umbral es > 1 y no > 2: en AG News los tokens de 2 letras "us", "uk" y "eu"
# concentran señal de la clase World y filtrarlos borra vocabulario del dominio.
MIN_LEMMA_LEN = 1


def clean(text: str) -> str:
    text = text.lower()
    text = html.unescape(text)              # &lt; -> <, &#39; -> ', &amp; -> &
    text = RE_BARE_LT.sub("<", text)        # formas truncadas sin ampersand
    text = RE_BARE_GT.sub(">", text)
    text = RE_BARE_AMP.sub("&", text)
    text = RE_BARE_ENTITY.sub(" ", text)
    text = RE_HTML.sub(" ", text)
    text = RE_HTML_OPEN.sub(" ", text)
    text = RE_REUTERS.sub(" ", text)        # boilerplate "(xyz.n: quote, profile, research)"
    text = RE_URL.sub(" ", text)
    text = RE_NOISE.sub(" ", text)
    return RE_WS.sub(" ", text).strip()


def _keep(tok) -> bool:
    return not tok.is_stop and not tok.is_punct and len(tok.lemma_) > MIN_LEMMA_LEN


def preprocess_text(text: str) -> str:
    doc = nlp(clean(text))
    return " ".join(tok.lemma_ for tok in doc if _keep(tok))


def preprocess_corpus(texts, batch_size=256, n_process=2):
    cleaned = (clean(t) for t in texts)
    out = []
    for doc in nlp.pipe(cleaned, batch_size=batch_size, n_process=n_process):
        out.append(" ".join(tok.lemma_ for tok in doc if _keep(tok)))
    return out
