"""Pipeline de preprocesamiento: limpieza Regex + normalización + lematización SpaCy."""
import re

import spacy

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

RE_HTML = re.compile(r"<[^>]+>")
RE_URL = re.compile(r"http\S+|www\.\S+")
RE_NOISE = re.compile(r"[^a-z\s]")
RE_WS = re.compile(r"\s+")

# El umbral es > 1 y no > 2: en AG News los tokens de 2 letras "us", "uk" y "eu"
# concentran señal de la clase World y filtrarlos borra vocabulario del dominio.
MIN_LEMMA_LEN = 1


def clean(text: str) -> str:
    text = text.lower()
    text = RE_HTML.sub(" ", text)
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
