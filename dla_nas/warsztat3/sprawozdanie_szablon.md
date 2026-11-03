# Warsztat 3 — YOLO jako czujnik w minigrze

## 1. Temat i autorzy

**Temat:** YOLO jako czujnik w minigrze — wykrycie butelki w strefie obrazu jako warunek nagrody i wpływ progu ufności na błędne decyzje  
**Data:** _[uzupełnijcie]_  
**Numer/nazwa zespołu:** _[uzupełnijcie]_  
**Członkowie zespołu (imiona i nazwiska):** _[uzupełnijcie]_  
**Przewodnik z zespołu liderskiego (imię i nazwisko):** _[uzupełnijcie]_

## 2. Cel i wykonane zmiany

**Cel:** Połączyć wynik gotowej sieci neuronowej z regułą gry: butelka wykryta w środkowej jednej trzeciej obrazu odblokowuje nagrodę. Ocenić, jak próg ufności wpływa na błędne decyzje.

**Reguła gry:** nagroda przysługuje, gdy co najmniej jedna wykryta butelka przekracza próg ufności, a środek jej ramki leży w strefie. Jedno zdjęcie daje najwyżej jedną nagrodę.

**Uzupełnione lub zmienione elementy notatnika:**
- _[uzupełnijcie]_

**Ręczna ocena dwóch zdjęć przed uruchomieniem modelu (pierwsze 10 minut):**

| Zdjęcie | Co na nim widać | Oczekiwana decyzja gry | Decyzja po uruchomieniu modelu |
|---|---|---|---|
| _[uzupełnijcie]_ | — | — | — |
| _[uzupełnijcie]_ | — | — | — |

## 3. Eksperyment

**Dane:** `data/images` — 12 zdjęć: 4 z butelką w strefie, 4 z butelką poza strefą, 4 bez butelki. Etykiety referencyjne w `data/labels.csv`.  
**Strefa:** środkowa jedna trzecia szerokości obrazu, na całej wysokości.

| Parametr | Użyta wartość |
|---|---|
| Model | _[domyślnie yolo11n.pt]_ |
| Porównywane progi ufności | _[domyślnie 0,25 i 0,60]_ |
| Próg detekcji w `detect` | _[domyślnie 0,10]_ |
| Urządzenie | _[CPU]_ |
| Inne zmiany parametrów (jeśli były) | _[brak / opiszcie]_ |

**Jak przeprowadziliśmy test:** _[uzupełnijcie]_

### 3.1. Opcjonalne rozszerzenie
 _[uzupełnijcie lub usuńcie podsekcję]_

## 4. Wyniki

### 4.1. Zestawienie obu progów

| Wynik | Próg 0,25 | Próg 0,60 |
|---|---:|---:|
| Poprawne nagrody | — | — |
| Błędne nagrody | — | — |
| Pominięte nagrody | — | — |
| Poprawne odmowy | — | — |

### 4.2. Analiza pomyłek

> Wpiszcie wszystkie zdjęcia z błędną lub pominiętą nagrodą. Przyczyna to: brak detekcji, niepoprawna lokalizacja lub klasa albo sama reguła gry.

| Zdjęcie | Próg | Wynik | Co zwrócił model | Przyczyna |
|---|---:|---|---|---|
| _[uzupełnijcie]_ | — | — | — | — |
| _[uzupełnijcie]_ | — | — | — | — |

### 4.3. Przykłady działania

**Przykład poprawny:** _[wstawcie `przyklad_poprawny.png` i opiszcie decyzję]_.

**Przykład problematyczny:** _[wstawcie `przyklad_problem.png` i opiszcie decyzję]_.

**Nieudane próby lub problemy podczas pracy:** _[uzupełnijcie]_.

## 5. Wnioski i ograniczenia

**Porównanie progów i wybór do minigry:** _[uzupełnijcie]_.

**Koszt błędnej nagrody a koszt pominiętej nagrody:** _[uzupełnijcie]_.

**Ocena reguły środka ramki, np. gdy ramka zahacza o strefę:** _[uzupełnijcie]_.

**Ograniczenia eksperymentu (mały zestaw nie uzasadnia ogólnej oceny detektora):** _[uzupełnijcie]_.

**Stan rozwiązania na koniec 90 minut:** _[uzupełnijcie]_.

**Wkład członków zespołu:**

| Imię i nazwisko | Wykonane zadania podczas warsztatu |
|---|---|
| _[osoba 1]_ | _[uzupełnijcie]_ |
| _[osoba 2]_ | _[uzupełnijcie]_ |
| _[osoba 3]_ | _[uzupełnijcie]_ |
| _[osoba 4]_ | _[uzupełnijcie]_ |
| _[osoba 5, jeśli dotyczy]_ | _[uzupełnijcie]_ |
