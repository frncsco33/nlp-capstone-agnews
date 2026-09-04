"""Training loop y ciclo de validación del Módulo 1."""
import torch
from sklearn.metrics import f1_score

from src.config import DEVICE


def train_one_epoch(model, loader, criterion, optimizer):
    model.train()
    running = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(DEVICE), yb.to(DEVICE)
        optimizer.zero_grad()  # sin esto los gradientes se acumulan entre batches
        logits = model(xb)
        loss = criterion(logits, yb)
        loss.backward()
        optimizer.step()
        running += loss.item() * xb.size(0)
    return running / len(loader.dataset)


@torch.no_grad()
def validate(model, loader, criterion):
    model.eval()
    vloss, preds, trues = 0.0, [], []
    for xb, yb in loader:
        xb, yb = xb.to(DEVICE), yb.to(DEVICE)
        logits = model(xb)
        vloss += criterion(logits, yb).item() * xb.size(0)
        preds += logits.argmax(1).cpu().tolist()
        trues += yb.cpu().tolist()
    val_loss = vloss / len(loader.dataset)
    val_f1 = f1_score(trues, preds, average="weighted")
    return val_loss, val_f1


def fit(model, train_loader, val_loader, criterion, optimizer, epochs):
    history = {"train_loss": [], "val_loss": [], "val_f1": []}
    for epoch in range(epochs):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer)
        val_loss, val_f1 = validate(model, val_loader, criterion)
        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["val_f1"].append(val_f1)
        print(
            f"epoch {epoch + 1}: train {train_loss:.4f} | "
            f"val {val_loss:.4f} | F1 {val_f1:.4f}"
        )
    return history
