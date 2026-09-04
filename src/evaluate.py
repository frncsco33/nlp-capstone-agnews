"""Métricas y visualizaciones compartidas por M3 (baseline) y M4 (LoRA)."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
    confusion_matrix,
)

from src.config import LABEL_NAMES, METRICS_DIR, FIGURES_DIR


def report(y_true, y_pred) -> dict:
    print(classification_report(y_true, y_pred, target_names=LABEL_NAMES, digits=4))
    return classification_report(
        y_true, y_pred, target_names=LABEL_NAMES, output_dict=True
    )


def save_metrics(rep: dict, name: str, extra: dict | None = None):
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"classification_report": rep, **(extra or {})}
    path = METRICS_DIR / f"{name}.json"
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path


def plot_confusion(y_true, y_pred, name: str, title: str) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    disp = ConfusionMatrixDisplay(
        confusion_matrix(y_true, y_pred), display_labels=LABEL_NAMES
    )
    disp.plot(xticks_rotation=45, cmap="Blues", colorbar=False)
    plt.title(title)
    plt.tight_layout()
    path = FIGURES_DIR / f"{name}.png"
    plt.savefig(path, dpi=150)
    plt.show()
    return path
