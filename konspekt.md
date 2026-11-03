# Warsztat 3 — YOLO jako czujnik w minigrze: konspekt

**Zespół liderski:** _[uzupełnijcie skład]_  
**Data zajęć:** _[uzupełnijcie]_  
**Czas:** około 10 minut prezentacji, 90 minut pracy zespołów, po 5–6 minut demo na zespół

## Cel

Gracz pokazuje przedmiot przed kamerą, a wykrycie butelki w oznaczonej strefie obrazu odblokowuje nagrodę. Zespoły łączą wynik gotowej sieci neuronowej z regułą gry i oceniają, jak próg ufności wpływa na błędne decyzje. W podstawowym wariancie zamiast kamery używamy gotowych zdjęć. Modelu nie trenujemy.

## Dane wejściowe

- 12 małych zdjęć w `data/images`: po 4 z butelką w strefie, z butelką poza strefą i bez butelki.
- Etykiety referencyjne „nagroda” lub „brak nagrody” w `data/labels.csv`.
- Gotowy model detekcyjny `yolo11n.pt` (wytrenowany na COCO, zna klasę `bottle`). Działa na CPU, a wagi są w pakiecie.

## Reguła gry

- **Strefa:** środkowa jedna trzecia szerokości obrazu, na całej jego wysokości.
- **Nagroda:** co najmniej jedna wykryta butelka przekracza próg ufności, a środek jej ramki leży w strefie.
- **Limit:** jedno zdjęcie daje najwyżej jedną nagrodę.

## Oczekiwany rezultat

- Działający notatnik z regułą decyzyjną.
- Tabela czterech wyników dla progów 0,25 i 0,60: poprawne nagrody, błędne nagrody, pominięte nagrody, poprawne odmowy.
- Przyczyna każdej pomyłki: brak detekcji, niepoprawna lokalizacja lub klasa albo sama reguła gry.
- Zrzuty przykładu poprawnego i problematycznego.
- Sprawozdanie z nazwą modelu, wersjami bibliotek i wyjaśnieniem kosztu błędnej oraz pominiętej nagrody.

## Sposób sprawdzenia działania

- Notatnik zawiera komórki z `assert`, które sprawdzają strefę i regułę na ręcznie przygotowanych ramkach. Muszą przejść bez błędu.
- Decyzję na każdym zdjęciu można sprawdzić wzrokowo: `draw_decision` rysuje strefę, ramki butelek, ich środki i decyzję.
- Wyniki z 12 zdjęć porównujemy z etykietami referencyjnymi. Suma czterech wyników przy każdym progu musi wynosić 12.
- Rozszerzenie sprawdza polecenie `python kamera.py --test`, które nie wymaga kamery.

## Zakres

**Podstawowy:** notatnik `warsztat3.ipynb`, sekcje 1–8, oraz sprawozdanie.

**Dodatkowy, dla zespołów, które skończą wcześniej:** `kamera.py`. Punkt przyznajemy po trzech kolejnych klatkach z butelką w strefie, a następny odblokowujemy po opuszczeniu strefy, żeby nieruchomy przedmiot nie zdobywał punktu w każdej klatce. Rozszerzenie nie jest wymagane do oddania podstawy.

## Plan 90 minut pracy

| Czas | Etap | Co robi zespół | Sekcje notatnika |
|---|---|---|---|
| 0–10 min | Start | Podział ról, otwarcie sprawozdania, omówienie klasy, ramki i ufności, ręczna ocena dwóch zdjęć | 1–2 |
| 10–25 min | Detekcja | Wczytanie modelu, odczyt klasy, ufności i współrzędnych, wyznaczenie strefy | 3–5 |
| 25–55 min | Reguła gry | Środek ramki, warunek strefy, decyzja o nagrodzie, rysowanie decyzji | 6 |
| 55–75 min | Eksperyment | Test 12 zdjęć dla progów 0,25 i 0,60, zliczenie wyników, analiza przyczyn pomyłek | 7 |
| 75–90 min | Oddanie | Tabela, dwa przykłady, wnioski, przesłanie kodu i sprawozdania na Teams | 8 |

Sprawozdanie zespoły uzupełniają na bieżąco, nie dopiero pod koniec. Oddajemy także rozwiązanie częściowe, z opisem jego stanu.

## Demo na forum grupy

5–6 minut na zespół, po części roboczej, bez osobnych slajdów:

1. Decyzja minigry na dwóch zdjęciach.
2. Porównanie progów 0,25 i 0,60.
3. Omówienie jednego błędu detekcji lub przyznania nagrody.

## Co oddaje zespół

Przez MS Teams, do końca 90 minut pracy: uzupełniony notatnik, sprawozdanie (około 3 stron) i małe pliki wynikowe, czyli `przyklad_poprawny.png` i `przyklad_problem.png`.

## Rola przewodnika

Każdy zespół ma jednego przewodnika z zespołu liderskiego. Przewodnik wyjaśnia problem, pomaga rozpoznawać błędy i zadaje pytania, ale nie pisze kodu za zespół.

Pytania pomocnicze:

- Co dokładnie zwrócił model dla tego zdjęcia? Czy butelka jest na liście detekcji?
- Czy problem pojawia się już w detekcji, czy dopiero w regule?
- Co zmienia się na tym zdjęciu po podniesieniu progu?
- Co zrobi gra, jeśli ramka zahacza o strefę, ale środek leży poza nią? Czy to uczciwe dla gracza?
- Co bardziej szkodzi grze: nagroda bez powodu czy brak nagrody za poprawną akcję?

## Przydział przewodników

| Zespół | Przewodnik |
|---|---|
| _[uzupełnijcie]_ | _[uzupełnijcie]_ |
| _[uzupełnijcie]_ | _[uzupełnijcie]_ |
| _[uzupełnijcie]_ | _[uzupełnijcie]_ |
| _[uzupełnijcie]_ | _[uzupełnijcie]_ |
