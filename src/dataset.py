"""Carga del corpus AG News y splits reproducibles."""
import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import SEED, TRAIN_CSV, TEST_CSV, LABEL_NAMES

LABEL2ID = {name: i for i, name in enumerate(LABEL_NAMES)}
ID2LABEL = {i: name for name, i in LABEL2ID.items()}


def _normalize_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Garantiza `label` como entero 0..3 y conserva el nombre en `label_name`."""
    if df["label"].dtype == object:
        df["label_name"] = df["label"]
        df["label"] = df["label"].map(LABEL2ID)
    else:
        df["label"] = df["label"].astype(int)
        if df["label"].min() == 1:  # AG News clásico viene 1..4
            df["label"] = df["label"] - 1
        df["label_name"] = df["label"].map(ID2LABEL)
    if df["label"].isna().any():
        raise ValueError("Etiquetas fuera del mapeo esperado World/Sports/Business/Sci_Tech")
    return df


def load_raw():
    train = _normalize_labels(pd.read_csv(TRAIN_CSV))
    test = _normalize_labels(pd.read_csv(TEST_CSV))
    return train, test


def train_val_split(train: pd.DataFrame, val_size: float = 0.1):
    """Valida sobre un split propio; el test se toca una sola vez al final."""
    return train_test_split(
        train, test_size=val_size, random_state=SEED, stratify=train["label"]
    )
