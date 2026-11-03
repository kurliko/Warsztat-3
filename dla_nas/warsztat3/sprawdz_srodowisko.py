"""Sprawdza instalację przed zajęciami: wersje bibliotek, model, zdjęcia i czas detekcji."""

import platform
import sys
import time
from pathlib import Path

import cv2
import matplotlib
import numpy as np
import torch
import ultralytics
from ultralytics import YOLO

from yolo_utils import TARGET_CLASS, detect, load_samples, read_image


HERE = Path(__file__).resolve().parent


def main() -> None:
    print(f"System:      {platform.system()} {platform.machine()}")
    print(f"Python:      {platform.python_version()}")
    print(f"ultralytics: {ultralytics.__version__}")
    print(f"torch:       {torch.__version__}")
    print(f"opencv:      {cv2.__version__}")
    print(f"numpy:       {np.__version__}")
    print(f"matplotlib:  {matplotlib.__version__}")

    model = YOLO(str(HERE / "yolo11n.pt"))
    if TARGET_CLASS not in model.names.values():
        sys.exit(f"BŁĄD: model nie zna klasy {TARGET_CLASS}.")

    samples = load_samples(HERE / "data" / "labels.csv")
    if len(samples) != 12:
        sys.exit(f"BŁĄD: oczekiwano 12 zdjęć, znaleziono {len(samples)}.")

    start = time.perf_counter()
    for sample in samples:
        detect(model, read_image(sample.path))
    elapsed = time.perf_counter() - start

    print(f"Detekcja na {len(samples)} zdjęciach: {elapsed:.1f} s (urządzenie: {model.device})")
    print("OK: środowisko jest gotowe.")


if __name__ == "__main__":
    main()
