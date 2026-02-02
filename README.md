# Algorytm Huffmana – Kompresja i Dekompresja

## Menu główne

Program sterowany jest za pomocą menu tekstowego:

1. **Kolejka Priorytetowa** – demonstracja działania kopca minimum
2. **Kompresja pliku** – kodowanie pliku tekstowego algorytmem Huffmana
3. **Dekompresja pliku** – odtwarzanie pliku z postaci skompresowanej
4. **Wyjście** – zakończenie programu

---

### 1. Kolejka priorytetowa

Pozwala przetestować wszystkie wymagane operacje zawarte w klasie `MinPriorityQueue`:

* **wstawianie elementów** z priorytetem,
* **pobieranie minimum**,
* **zmniejszanie priorytetu** wybranego elementu,
* **budowanie kolejki** z gotowej listy (operacja `build_queue`),
* **podgląd aktualnego stanu kopca**.

---

### 2. Kompresja pliku

* Program wyświetla listę dostępnych plików `.txt` w folderze projektu do sformatowani.
* Domyślnie można użyć pliku `plik_do_testow.txt` (powstaje automatycznie przy uruchomieniu programu).
* Użytkownik podaje nazwę pliku wyjściowego (np. `wynik.txt`).

**Plik wyjściowy jest sformatowany w sposób czytelny, umożliwiający dekompresję:**

* **Każda linia to**: `Znak:Częstotliwość-Kod`.
* **Obsługa spacji i enterów**: Znaki specjalne są zapisywane jako `<SP>` i `<NL>` dla bezpieczeństwa danych.
* **Separator**: Stała linia `##############################` oddziela słownik od zakodowanej treści.
* **Dane**: Strumień bitowy reprezentowany jako ciąg znaków '0' i '1'.

**Podczas kompresji program:**

* wyświetla tabelę znaków, ich częstotliwości i kodów Huffmana,
* zapisuje słownik i dane binarne do pliku wynikowego.

---

### 3. Dekompresja pliku

* Użytkownik podaje nazwę pliku skompresowanego (np. `wynik_kompresji.txt`).
* Następnie nazwę pliku wynikowego (np. `odzyskany.txt`).

---

## Testowanie poprawności działania

### Test 1 – poprawność kompresji i dekompresji
Należy:

1. Skompresować plik `plik_do_testow.txt`.
2. Zdekompresować uzyskany plik `.txt`.
3. Plik oryginalny i odzyskany  **powinny być identyczne**.

### Test 2 – kolejka priorytetowa

Należy sprawdzić ręcznie w module demonstracyjnym:

* czy `extract_min` zawsze zwraca element o najmniejszym priorytecie,
* czy `decrease_priority` poprawnie reorganizuje kopiec,
* czy `build_queue` tworzy poprawną strukturę (struktura jest twardo zakodowana, aby ułatwić testowanie).

---

## Funkcjonalności

* **Własna implementacja**: Brak bibliotek typu `heapq`, cała logika kopca znajduje się w `priority_queue.py`.
* **Kompresja plików**: Kodowanie tekstów do formatu zawierającego słownik + dane.
* **Dekompresja plików**: Przywracanie danych do postaci oryginalnej.
* **Wprowadzanie nazw plików**: Obsługa ścieżek przez użytkownika.

* **Poprawna obsługa znaków**: Specjalne traktowanie spacji i znaków nowej linii.
