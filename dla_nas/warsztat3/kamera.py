"""Rozszerzenie warsztatu: minigra z kamerą. Uruchamianie opisuje README.md."""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import cv2
from ultralytics import YOLO

from yolo_utils import TARGET_CLASS, Detection, detect, draw_decision


HERE = Path(__file__).resolve().parent
REQUIRED_FRAMES = 3  # tyle kolejnych klatek z butelką w strefie daje punkt
EXIT_FRAMES = 3      # tyle kolejnych klatek bez butelki oznacza opuszczenie strefy


@dataclass
class GameState:
    score: int = 0        # liczba zdobytych punktów
    streak: int = 0       # kolejne klatki z butelką w strefie
    missing: int = 0      # kolejne klatki bez butelki w strefie
    locked: bool = False  # True: punkt przyznany, czekamy na opuszczenie strefy


def read_detections(result):
    # TODO: Wklej swoją funkcję read_detections z notatnika.
    detections = []
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        detections.append(Detection(result.names[int(box.cls[0])], float(box.conf[0]), x1, y1, x2, y2))
    return detections


def bottle_in_zone(detections, zone, threshold):
    # TODO: Wklej logikę swojej funkcji reward_decision z notatnika.
    for detection in detections:
        center = (detection.x1 + detection.x2) / 2
        if detection.class_name == TARGET_CLASS and detection.confidence > threshold and zone[0] <= center <= zone[1]:
            return True
    return False


def update_game(state, in_zone):
    if in_zone:
        # TODO: Zwiększ streak i wyzeruj missing.
        state.streak += 1
        state.missing = 0

        # TODO: Przyznaj punkt i zablokuj grę, gdy streak osiągnął REQUIRED_FRAMES, a gra nie jest zablokowana.
        if state.streak >= REQUIRED_FRAMES and not state.locked:
            state.score += 1
            state.locked = True
    else:
        # TODO: Wyzeruj streak i zwiększ missing.
        state.streak = 0
        state.missing += 1

        # TODO: Odblokuj grę, gdy missing osiągnął EXIT_FRAMES.
        if state.missing >= EXIT_FRAMES:
            state.locked = False


def run_logic_test() -> None:
    """Sprawdza update_game bez kamery: 1 to klatka z butelką w strefie, 0 to klatka bez niej."""
    cases = [
        ("dwie klatki to za mało", [1, 1], 0),
        ("trzy klatki dają punkt", [1, 1, 1], 1),
        ("nieruchoma butelka daje jeden punkt", [1] * 20, 1),
        ("przerwana seria nie daje punktu", [1, 1, 0, 1, 1], 0),
        ("jedna klatka przerwy nie odblokowuje", [1, 1, 1, 0, 1, 1, 1], 1),
        ("po wyjściu ze strefy można zdobyć kolejny punkt", [1, 1, 1, 0, 0, 0, 1, 1, 1], 2),
    ]
    failed = 0
    for description, frames, expected in cases:
        state = GameState()
        for frame in frames:
            update_game(state, bool(frame))
        passed = state.score == expected
        failed += not passed
        print(f"{'OK ' if passed else 'BŁĄD'} {description}: punkty {state.score}, oczekiwano {expected}")
    sys.exit(1 if failed else 0)


def open_source(source: str) -> cv2.VideoCapture:
    """Przyjmuje numer kamery albo ścieżkę do filmu. Zwraca otwarte źródło obrazu."""
    if source.isdigit():
        # Na Windowsie backend DirectShow zwykle otwiera kamerę szybciej.
        backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY
        capture = cv2.VideoCapture(int(source), backend)
    else:
        capture = cv2.VideoCapture(source)

    if not capture.isOpened():
        sys.exit(
            f"Nie można otworzyć źródła obrazu: {source}. Sprawdź, czy kamera nie jest zajęta "
            "i czy system pozwala terminalowi na dostęp do niej."
        )
    return capture


def main() -> None:
    parser = argparse.ArgumentParser(description="Minigra: pokaż butelkę w strefie.")
    parser.add_argument("--threshold", type=float, default=0.60, help="próg ufności")
    parser.add_argument("--source", default="0", help="numer kamery albo ścieżka do filmu")
    parser.add_argument("--no-window", action="store_true", help="nie otwieraj okna, wypisz tylko wynik")
    parser.add_argument("--test", action="store_true", help="sprawdź logikę punktów bez kamery")
    args = parser.parse_args()

    if args.test:
        run_logic_test()

    model = YOLO(str(HERE / "yolo11n.pt"))
    capture = open_source(args.source)
    state = GameState()

    while True:
        success, frame = capture.read()
        if not success:
            break

        width = frame.shape[1]
        zone = (width / 3, 2 * width / 3)
        detections = read_detections(detect(model, frame))
        in_zone = bottle_in_zone(detections, zone, args.threshold)
        update_game(state, in_zone)

        if args.no_window:
            continue

        canvas = draw_decision(frame, detections, zone, args.threshold, in_zone)
        text = f"PUNKTY: {state.score}  SERIA: {state.streak}  BLOKADA: {'tak' if state.locked else 'nie'}"
        cv2.putText(canvas, text, (8, canvas.shape[0] - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Minigra z butelka (q konczy)", canvas)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()
    print(f"Koniec gry. Punkty: {state.score}")


if __name__ == "__main__":
    main()
