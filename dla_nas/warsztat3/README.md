# Warsztat 3 — instrukcja uruchomienia

Wymagany Python 3.11 lub nowszy. Wystarczy CPU. Uruchom terminal w tym folderze.

**Zainstaluj wszystko przed zajęciami.** PyTorch waży kilkaset MB, a pobieranie przez wszystkie zespoły naraz na sali może potrwać zbyt długo.

## 1. Środowisko

```bash
python -m venv .venv
```
Windows PowerShell: `.venv\Scripts\Activate.ps1`

macOS/Linux: `source .venv/bin/activate`

## 2. Biblioteki

**Tylko Linux:** najpierw zainstaluj PyTorcha w wersji na CPU, bo domyślna wersja pobiera dodatkowo kilka GB paczek dla kart graficznych.

```bash
python -m pip install torch==2.15.0 torchvision==0.29.2 --index-url https://download.pytorch.org/whl/cpu
```

**Wszystkie systemy:**

```bash
python -m pip install -r requirements.txt
```

## 3. Sprawdzenie instalacji

```bash
python sprawdz_srodowisko.py
```
Na końcu powinien pojawić się napis `OK: środowisko jest gotowe.`

## 4. Praca

```bash
python -m notebook
```
Otwórz `warsztat3.ipynb` i uzupełniaj TODO po kolei. Wyniki wpisuj na bieżąco do `sprawozdanie_szablon.md`.

## Dla chętnych: kamera

Otwórz `kamera.py` i uzupełnij TODO. Logikę punktów sprawdzisz bez kamery:

```bash
python kamera.py --test
```

Grę uruchomisz tak (klawisz `q` kończy program):

```bash
python kamera.py --threshold 0.6
```

Jeśli masz kilka kamer, wybierz inną opcją `--source 1`. Na macOS przy pierwszym uruchomieniu trzeba pozwolić terminalowi na dostęp do kamery (Ustawienia systemowe → Prywatność i ochrona → Kamera).

## Rozwiązywanie problemów

- **Windows, błąd aktywacji środowiska w PowerShell:** uruchom `Set-ExecutionPolicy -Scope Process RemoteSigned` i spróbuj ponownie.
- **Brak modelu:** plik `yolo11n.pt` musi leżeć w tym folderze. Terminal i notatnik też muszą być uruchomione w tym folderze.
- **Mac z procesorem Intel:** biblioteka PyTorch w tej wersji nie jest dostępna, więc poproś przewodnika o pomoc.
