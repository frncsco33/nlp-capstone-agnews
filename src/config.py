"""Configuración global del proyecto: semillas, rutas y dispositivo."""
import random
from pathlib import Path

import numpy as np
import torch

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
FIGURES_DIR = ROOT / "reports" / "figures"
METRICS_DIR = ROOT / "reports" / "metrics"

TRAIN_CSV = DATA_DIR / "ag_news_train.csv"
TEST_CSV = DATA_DIR / "ag_news_test.csv"

LABEL_NAMES = ["World", "Sports", "Business", "Sci_Tech"]
N_CLASSES = len(LABEL_NAMES)


def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


DEVICE = get_device()

if __name__ == "__main__":
    print(f"PyTorch {torch.__version__} | device: {DEVICE}")
