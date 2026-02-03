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
* **budowanie kolejki** z gotowej listy (operacja `build_queue` wykorzystująca **algorytm Floyda** o złożoności $O(n)$),
* **podgląd aktualnego stanu kopca**.

---

### 2. Kompresja pliku

* Program wyświetla listę dostępnych plików `.txt` w folderze projektu.
* Domyślnie można użyć pliku `plik_do_testow.txt` (powstaje automatycznie przy uruchomieniu programu).
* Użytkownik podaje nazwę pliku wyjściowego (np. `wynik.bin`).

**Plik wyjściowy jest zapisywany binarnie (`.bin`), co zapewnia rzeczywistą oszczędność miejsca:**

* **Nagłówek (SŁOWNIK)**: Tekstowy zapis mapowania (np. `a: 5 - 101`) umożliwiający dekompresję.
* **Obsługa spacji i enterów**: Znaki specjalne w słowniku są zapisywane jako `<SP>` i `<NL>`.
* **Sekcja DANE**: Po separatorze `DANE:` następuje zapis binarny.
* **Bit Packing**: Ciągi zer i jedynek są pakowane w 8-bitowe bajty (nie jako tekst).
* **Padding**: Na końcu pliku zapisywana jest informacja `PADDING: X`, mówiąca ile bitów należy zignorować w ostatnim bajcie.

**Podczas kompresji program:**

* generuje kody Huffmana na podstawie częstości znaków,
* tworzy plik binarny zawierający niezbędny nagłówek oraz skompresowane dane.

---

### 3. Dekompresja pliku

* Użytkownik podaje nazwę pliku skompresowanego (np. `wynik_kompresji.bin`).
* Następnie nazwę pliku wynikowego (np. `odzyskany.txt`).
* Program odczytuje nagłówek, odtwarza drzewo kodów i dekoduje bajty z powrotem na tekst.

---

## Testowanie poprawności działania

### Test 1 – poprawność kompresji i dekompresji
Należy:

1. Skompresować plik `plik_do_testow.txt`.
2. Zdekompresować uzyskany plik `.bin`.
3. Plik oryginalny i odzyskany **powinny być identyczne**.

### Test 2 – kolejka priorytetowa

Należy sprawdzić ręcznie w module demonstracyjnym:

* czy `extract_min` zawsze zwraca element o najmniejszym priorytecie,
* czy `decrease_priority` poprawnie reorganizuje kopiec,
* czy `build_queue` tworzy poprawną strukturę (zgodnie z regułą rodzic <= dzieci).

---

## Funkcjonalności

* **Własna implementacja**: Brak bibliotek typu `heapq`, cała logika kopca znajduje się w `priority_queue.py`.
* **Kompresja binarna**: Rzeczywiste upychanie bitów (bit packing) do pliku `.bin`, a nie zapis ciągu "01" jako tekstu.
* **Dekompresja plików**: Przywracanie danych binarnych do postaci oryginalnego tekstu.
* **Wprowadzanie nazw plików**: Obsługa ścieżek przez użytkownika.
* **Poprawna obsługa znaków**: Specjalne traktowanie spacji i znaków nowej linii w nagłówku pliku.