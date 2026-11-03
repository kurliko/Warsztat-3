# Warsztat 3 — YOLO jako czujnik w minigrze

Materiały zespołu liderskiego. Program występuje w dwóch wersjach.

| Folder | Dla kogo | Co zawiera |
|---|---|---|
| `dla_nas/warsztat3` | **my**, do testów i zapoznania | kompletny, działający program z zapisanymi wynikami |
| `dla_studentow/warsztat3` | **studenci**, na warsztat | ten sam program z lukami `...` i komentarzami `# TODO` |
| `dla_studentow/starterpack_warsztat3.zip` | **studenci** | spakowany folder powyżej, do wysłania na Teams |

Obie wersje mają te same nazwy plików. Różnią się tylko `warsztat3.ipynb` i `kamera.py`, więc łatwo je porównać.

## Pozostałe pliki

| Plik | Co zawiera | Dla studentów? |
|---|---|---|
| `Prezentacja_warsztat3.pdf` | 8 slajdów na około 10 minut | tak |
| `prezentacja_zrodlo/` | źródło slajdów w HTML | nie |
| `konspekt.md` | opis zadania i plan 90 minut | tak |
| `dla_nas/notatki_do_prezentacji.md` | co powiedzieć na każdym slajdzie, z czasem | nie |
| `dla_nas/wyniki_referencyjne.md` | **odpowiedzi**, przyczyny pomyłek, typowe trudności | **nie** |
| `zrodla_zdjec.csv` | źródło każdego zdjęcia w COCO | po dodaniu licencji |

## Zmiana slajdów, np. wpisanie składu zespołu

1. Wpiszcie zmianę w `prezentacja_zrodlo/prezentacja.html`. Skład zespołu jest w linii z napisem `Autorzy:`.
2. Otwórzcie ten plik w Edge lub Chrome i wybierzcie drukowanie (Ctrl+P).
3. Ustawcie: miejsce docelowe „Zapisz jako PDF”, marginesy „Brak”, grafika tła włączona, nagłówki i stopki wyłączone.
4. Zapiszcie jako `Prezentacja_warsztat3.pdf`, zastępując stary plik.

## Szybki start

Pełna instrukcja jest w `dla_nas/warsztat3/README.md`. Uruchomcie terminal w folderze `dla_nas/warsztat3`, a potem zainstalujcie biblioteki i otwórzcie notatnik zgodnie z tą instrukcją.

## Przed finalną wersją

- [ ] Dodać licencje zdjęć na podstawie `zrodla_zdjec.csv` (kolumna `coco_license_id`).
- [ ] Uzupełnić skład zespołu w prezentacji oraz skład, datę i przydział przewodników w `konspekt.md`.
- [ ] Sprawdzić instalację na Linuksie i macOS.
- [ ] Przeprowadzić próbę z pomiarem czasu i wpisać wynik do `dla_nas/wyniki_referencyjne.md`.
- [ ] Sprawdzić scenariusz punktów w `kamera.py` z prawdziwą kamerą.
- [ ] Po każdej zmianie w `dla_studentow/warsztat3` spakować folder ponownie do zipa.
