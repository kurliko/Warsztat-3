# Warsztat 3 — wyniki referencyjne i notatki przewodnika

**Tylko dla zespołu liderskiego i prowadzącego. Nie umieszczać w pakiecie dla studentów.**

Działające rozwiązanie jest w `dla_nas/warsztat3`. Notatnik `warsztat3.ipynb` ma zapisane wyniki, a pozostałe pliki odpowiadają wersji dla studentów.

## Środowisko

Windows 11, Python 3.12.10, CPU. Detekcja na 12 zdjęciach trwa około 2 s.

| Składnik | Wersja |
|---|---|
| Model | `yolo11n.pt` |
| ultralytics | 8.4.201 |
| torch | 2.15.0+cpu |
| torchvision | 0.29.2 |
| opencv-python | 5.0.0.93 |
| numpy | 2.3.5 |
| matplotlib | 3.11.2 |

Żadna ufność istotna dla decyzji nie leży bliżej niż 0,09 od progów 0,25 i 0,60, więc drobne różnice między komputerami nie powinny zmienić wyników. Na innych systemach nie zostało to jeszcze sprawdzone.

## Zestawienie

| Wynik | Próg 0,25 | Próg 0,60 |
|---|---:|---:|
| Poprawne nagrody | 3 | 2 |
| Błędne nagrody | 3 | 0 |
| Pominięte nagrody | 1 | 2 |
| Poprawne odmowy | 5 | 8 |

Podniesienie progu usuwa wszystkie błędne nagrody, ale kosztuje jedną dodatkową pominiętą nagrodę.

## Wyniki dla każdego zdjęcia

| Zdjęcie | Grupa | Etykieta | Ufności butelek | Próg 0,25 | Próg 0,60 | Rola w zestawie |
|---|---|---|---|---|---|---|
| img01 | w strefie | nagroda | 0,93; 0,83 | poprawna nagroda | poprawna nagroda | łatwy przypadek |
| img02 | w strefie | nagroda | 0,85; 0,83 | poprawna nagroda | poprawna nagroda | butelki w strefie i poza nią |
| img03 | w strefie | nagroda | 0,34 | poprawna nagroda | pominięta nagroda | częściowe zasłonięcie |
| img04 | w strefie | nagroda | brak | pominięta nagroda | pominięta nagroda | butelka w kubełku, prawie niewidoczna |
| img05 | poza strefą | brak nagrody | 0,75 | poprawna odmowa | poprawna odmowa | łatwy przypadek |
| img06 | poza strefą | brak nagrody | 0,90 | poprawna odmowa | poprawna odmowa | ramka zahacza o strefę, środek poza nią |
| img07 | poza strefą | brak nagrody | 0,88; 0,22 | poprawna odmowa | poprawna odmowa | dwie butelki poza strefą |
| img08 | poza strefą | brak nagrody | 0,39; 0,12 | błędna nagroda | poprawna odmowa | słoik w strefie wzięty za butelkę |
| img09 | bez butelki | brak nagrody | brak | poprawna odmowa | poprawna odmowa | kubki, szczoteczki |
| img10 | bez butelki | brak nagrody | brak | poprawna odmowa | poprawna odmowa | kieliszki |
| img11 | bez butelki | brak nagrody | 0,45 | błędna nagroda | poprawna odmowa | solniczka wzięta za butelkę |
| img12 | bez butelki | brak nagrody | 0,43 | błędna nagroda | poprawna odmowa | słoik wzięty za butelkę |

## Przyczyny pomyłek

| Zdjęcie | Próg | Wynik | Przyczyna |
|---|---:|---|---|
| img03 | 0,60 | pominięta nagroda | Detekcja jest, ale z ufnością 0,34, poniżej progu. Butelkę częściowo zasłania jedzenie. |
| img04 | oba | pominięta nagroda | Brak detekcji: widać tylko szyjkę butelki w kubełku. Żaden próg tego nie naprawi. |
| img08 | 0,25 | błędna nagroda | Zła klasa: słoik w strefie z ufnością 0,39. Prawdziwa butelka poza strefą ma tylko 0,12. |
| img11 | 0,25 | błędna nagroda | Zła klasa: solniczka z ufnością 0,45. |
| img12 | 0,25 | błędna nagroda | Zła klasa: słoik z ufnością 0,43. |

W tym zestawie nie ma pomyłki spowodowanej samą regułą ani złym położeniem ramki. Do rozmowy o regule służy `img06`: butelka w dużej części nachodzi na strefę, a gra odmawia, bo środek ramki leży poza nią. Zgodnie z etykietą to poprawna odmowa, ale gracz mógłby uznać ją za niesprawiedliwą.

## Etykiety do weryfikacji

Etykiety pochodzą z adnotacji COCO i zostały sprawdzone wzrokowo. Dwa przypadki są dyskusyjne:

- **img02:** butelką w strefie jest dozownik do mydła. COCO oznacza go jako `bottle` i tak też go liczymy.
- **img12:** COCO oznacza dwa boczne słoiki jako `bottle`. Traktujemy je jak słoiki, dlatego zdjęcie jest w grupie „bez butelki”.

## Kamera

`python kamera.py --test` przechodzi wszystkie 6 przypadków. Na filmie testowym (butelka w strefie, poza strefą, znów w strefie, próg 0,60) gra daje 2 punkty, z oknem i bez okna. **Prawdziwej kamery nie sprawdzano.**

## Typowe trudności

| Miejsce | Objaw | Co podpowiedzieć |
|---|---|---|
| Uruchomienie | `TypeError: 'ellipsis' object is not iterable` lub `not subscriptable` | W komórce lub w komórce wcześniejszej został `...`. To znaczy tylko, że luka nie jest jeszcze uzupełniona. |
| Uruchomienie | `NameError` | Nie uruchomiono wcześniejszej komórki albo zakończyła się ona błędem. |
| `read_detections` | `TypeError` przy ufności lub klasie | `box.conf` i `box.cls` to tensory. Tabela w sekcji 4 pokazuje, jak je odczytać. |
| `get_zone` | Assert nie przechodzi albo strefa jest pusta | Szerokość to `image.shape[1]`, a `shape[0]` to wysokość. |
| `reward_decision` | Każde zdjęcie daje nagrodę lub żadne | Sprawdzić `class_name == TARGET_CLASS` i to, czy `return False` nie jest wewnątrz pętli. |
| Test progów | Oba progi dają ten sam wynik | Funkcja używa stałej zamiast parametru `threshold`. |
| Analiza pomyłek | Zespół przypisuje wszystko modelowi | Poprosić o przeczytanie listy detekcji dla konkretnego zdjęcia. |
| Kamera | Nie otwiera się | Na macOS terminal potrzebuje zgody na dostęp do kamery. Inny program może też zajmować kamerę. |

## Do zrobienia przed zajęciami

- [ ] Próba całego ćwiczenia z pomiarem czasu. Czas: _[uzupełnijcie]_.
- [ ] Instalacja na typowym laptopie z Linuksem i macOS.
- [ ] Sprawdzenie `kamera.py` z prawdziwą kamerą.
