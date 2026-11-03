# Notatki do prezentacji

Około 10 minut. Nie zdradzamy wyników na konkretnych zdjęciach.

| Slajd | Czas | Co powiedzieć |
|---|---|---|
| 1. Tytuł | 30 s | Powitanie i przedstawienie zespołu. Każdy zespół dostaje jednego przewodnika od nas. |
| 2. Problem | 1 min | To zadanie o połączeniu modelu z logiką gry, a nie o trenowaniu sieci. Kamera jest tylko rozszerzeniem. |
| 3. Co zwraca model? | 2 min | Model zna tylko 80 klas COCO, więc nie rozpozna dowolnego obiektu z gry. Ufność to sygnał, który porównujemy z progiem, a nie prawdopodobieństwo poprawności. |
| 4. Reguła gry | 2 min | Liczy się środek ramki, a nie to, czy ramka zahacza o strefę. Zielona ramka przekracza próg, pomarańczowa nie. |
| 5. Próg ufności | 1,5 min | Pytanie do sali: co bardziej szkodzi grze, nagroda bez powodu czy brak nagrody za poprawną akcję? Nie ma jednej dobrej odpowiedzi. |
| 6. Narzędzia | 1 min | Środowisko powinno być zainstalowane przed zajęciami. Sprawdza je `python sprawdz_srodowisko.py`. Polecenia dla każdego systemu są w README. |
| 7. Plan pracy | 1 min | Komórki z `assert` pokazują, czy reguła działa, zanim zespół przejdzie do pełnego testu. Oddajemy także rozwiązanie częściowe. |
| 8. Wyniki i demo | 30 s | Przewodnicy rozchodzą się do zespołów. Mały zestaw służy demonstracji i nie uzasadnia ogólnej oceny detektora. |
