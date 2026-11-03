"""Narzędzia pomocnicze do minigry z butelką. Współrzędne ramek w pikselach obrazu."""

import csv
from dataclasses import dataclass
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes


TARGET_CLASS = "bottle"  # klasa COCO, której szuka minigra
REWARD = "nagroda"
NO_REWARD = "brak nagrody"

CORRECT_REWARD = "poprawna nagroda"
WRONG_REWARD = "błędna nagroda"
MISSED_REWARD = "pominięta nagroda"
CORRECT_REFUSAL = "poprawna odmowa"
OUTCOMES = [CORRECT_REWARD, WRONG_REWARD, MISSED_REWARD, CORRECT_REFUSAL]

IMAGE_SIZE = 640  # rozmiar wejścia modelu
DETECTION_CONF = 0.10  # niski próg modelu, progi gry 0,25 i 0,60 nakładamy dopiero w kodzie


@dataclass(frozen=True)
class Sample:
    """Jedno zdjęcie testowe z etykietą referencyjną."""

    name: str    # nazwa pliku
    path: Path   # ścieżka do pliku
    group: str   # w_strefie, poza_strefa lub bez_butelki
    label: str   # REWARD lub NO_REWARD


@dataclass(frozen=True)
class Detection:
    """Jedna ramka wykryta przez model."""

    class_name: str    # nazwa klasy, np. "bottle"
    confidence: float  # wynik ufności od 0 do 1
    x1: float          # lewa krawędź ramki
    y1: float          # górna krawędź ramki
    x2: float          # prawa krawędź ramki
    y2: float          # dolna krawędź ramki


@dataclass(frozen=True)
class TestRow:
    """Wynik testu jednego zdjęcia przy jednym progu."""

    name: str      # nazwa pliku
    group: str     # grupa zdjęcia
    label: str     # etykieta referencyjna
    reward: bool   # decyzja minigry
    outcome: str   # jedna z wartości OUTCOMES


def load_samples(path: str | Path = "data/labels.csv") -> list[Sample]:
    """Przyjmuje ścieżkę CSV. Zwraca listę próbek; zdjęcia leżą w podfolderze images."""
    path = Path(path)
    with open(path, encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    return [
        Sample(
            name=row["file"],
            path=path.parent / "images" / row["file"],
            group=row["group"],
            label=row["label"],
        )
        for row in rows
    ]


def read_image(path: str | Path) -> np.ndarray:
    """Przyjmuje ścieżkę. Zwraca obraz BGR; działa też dla ścieżek z polskimi znakami."""
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Nie można wczytać obrazu: {path}")
    return image


def detect(model, image: np.ndarray):
    """Przyjmuje model i obraz BGR. Zwraca wynik modelu dla tego obrazu (obiekt Results)."""
    return model.predict(image, conf=DETECTION_CONF, imgsz=IMAGE_SIZE, verbose=False)[0]


def draw_detections(
    image: np.ndarray, detections: list[Detection], only_target: bool = False
) -> np.ndarray:
    """Przyjmuje obraz i detekcje. Zwraca kopię obrazu z ramkami; butelki są czerwone."""
    canvas = image.copy()

    for det in detections:
        is_target = det.class_name == TARGET_CLASS
        if only_target and not is_target:
            continue

        color = (0, 0, 255) if is_target else (170, 170, 170)
        thickness = 2 if is_target else 1
        corner_1 = (int(det.x1), int(det.y1))
        corner_2 = (int(det.x2), int(det.y2))
        cv2.rectangle(canvas, corner_1, corner_2, color, thickness)
        _put_label(canvas, f"{det.class_name} {det.confidence:.2f}", corner_1, color)

    return canvas


def draw_decision(
    image: np.ndarray,
    detections: list[Detection],
    zone: tuple[float, float],
    threshold: float,
    reward: bool,
) -> np.ndarray:
    """Rysuje strefę, butelki i decyzję. Zielona ramka przekracza próg, pomarańczowa nie."""
    canvas = image.copy()
    height = canvas.shape[0]
    left, right = int(zone[0]), int(zone[1])

    overlay = canvas.copy()
    cv2.rectangle(overlay, (left, 0), (right, height), (0, 255, 255), -1)
    canvas = cv2.addWeighted(overlay, 0.15, canvas, 0.85, 0)
    cv2.line(canvas, (left, 0), (left, height), (0, 200, 255), 2)
    cv2.line(canvas, (right, 0), (right, height), (0, 200, 255), 2)

    for det in detections:
        if det.class_name != TARGET_CLASS:
            continue

        color = (0, 200, 0) if det.confidence > threshold else (0, 140, 255)
        corner_1 = (int(det.x1), int(det.y1))
        corner_2 = (int(det.x2), int(det.y2))
        center = (int((det.x1 + det.x2) / 2), int((det.y1 + det.y2) / 2))
        cv2.rectangle(canvas, corner_1, corner_2, color, 2)
        cv2.circle(canvas, center, 4, color, -1)
        _put_label(canvas, f"{det.confidence:.2f}", corner_1, color)

    # cv2.putText nie obsługuje polskich znaków, dlatego napisy są bez nich.
    text = f"NAGRODA (prog {threshold:.2f})" if reward else f"BRAK NAGRODY (prog {threshold:.2f})"
    banner = (0, 150, 0) if reward else (0, 0, 180)
    canvas = cv2.copyMakeBorder(canvas, 30, 0, 0, 0, cv2.BORDER_CONSTANT, value=banner)
    cv2.putText(canvas, text, (8, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    return canvas


def _put_label(canvas: np.ndarray, text: str, corner: tuple[int, int], color: tuple[int, int, int]) -> None:
    """Dopisuje podpis nad ramką, a przy górnej krawędzi obrazu pod jej górnym bokiem."""
    x, y = corner
    (text_width, _), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
    x = max(min(x + 2, canvas.shape[1] - text_width - 2), 0)  # podpis nie wychodzi poza obraz
    position = (x, y - 5) if y > 18 else (x, y + 16)
    cv2.putText(canvas, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)


def show_image(image: np.ndarray, title: str = "", ax: Axes | None = None) -> Axes:
    """Przyjmuje obraz BGR, tytuł i opcjonalne osie. Wyświetla obraz i zwraca osie."""
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax.set_title(title, fontsize=10)
    ax.axis("off")
    return ax


def show_samples(samples: list[Sample], columns: int = 4) -> None:
    """Przyjmuje listę próbek. Wyświetla je w siatce z nazwą pliku i grupą."""
    rows = (len(samples) + columns - 1) // columns
    _, axes = plt.subplots(rows, columns, figsize=(3.2 * columns, 2.7 * rows), squeeze=False)

    for ax in axes.flat:
        ax.axis("off")

    for sample, ax in zip(samples, axes.flat):
        show_image(read_image(sample.path), f"{sample.name}\n{sample.group}", ax=ax)

    plt.tight_layout()
    plt.show()


def print_detections(detections: list[Detection]) -> None:
    """Przyjmuje detekcje. Wypisuje je od największej ufności; nic nie zwraca."""
    print(f"{'KLASA':<16}{'UFNOŚĆ':>8}{'X1':>8}{'Y1':>8}{'X2':>8}{'Y2':>8}")
    for det in sorted(detections, key=lambda d: d.confidence, reverse=True):
        print(
            f"{det.class_name:<16}{det.confidence:>8.2f}"
            f"{det.x1:>8.0f}{det.y1:>8.0f}{det.x2:>8.0f}{det.y2:>8.0f}"
        )
    if not detections:
        print("Brak detekcji.")


def print_test_table(
    rows: list[TestRow], all_detections: dict[str, list[Detection]], threshold: float
) -> None:
    """Wypisuje wynik każdego zdjęcia przy danym progu oraz ufności wykrytych butelek."""
    print(f"Próg ufności: {threshold:.2f}")
    print(f"{'ZDJĘCIE':<11}{'GRUPA':<13}{'ETYKIETA':<14}{'DECYZJA':<9}{'WYNIK':<19}UFNOŚCI BUTELEK")
    for row in rows:
        bottles = [d.confidence for d in all_detections[row.name] if d.class_name == TARGET_CLASS]
        bottles_text = ", ".join(f"{value:.2f}" for value in sorted(bottles, reverse=True)) or "-"
        decision = "tak" if row.reward else "nie"
        print(f"{row.name:<11}{row.group:<13}{row.label:<14}{decision:<9}{row.outcome:<19}{bottles_text}")
    print()


def print_summary(counts_by_threshold: dict[float, dict[str, int]]) -> None:
    """Przyjmuje liczniki wyników dla każdego progu. Wypisuje tabelę zbiorczą."""
    thresholds = list(counts_by_threshold)
    print(f"{'WYNIK':<20}" + "".join(f"{f'próg {t:.2f}':>12}" for t in thresholds))
    for outcome in OUTCOMES:
        cells = "".join(f"{counts_by_threshold[t][outcome]:>12d}" for t in thresholds)
        print(f"{outcome:<20}{cells}")
