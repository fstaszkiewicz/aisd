import os
from priority_queue import MinPriorityQueue
from huffman_logic import HuffmanCoding


# ścieżka do folderu, w którym znajduje się plik main.py (tutaj będą przechowywane pliki testowe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_full_path(filename):
    """Zwraca pełną ścieżkę do pliku w folderze projektu."""
    return os.path.join(BASE_DIR, filename)

def create_shopping_list():
    """Tworzy plik plik_do_testow.txt w folderze projektu, jeśli nie istnieje."""
    filename = "plik_do_testow.txt"
    full_path = get_full_path(filename)
    
    if not os.path.exists(full_path):
        content = (
            "Lista zakupow:\n"
            "1. Mleko - 2 sztuki\n"
            "2. Chleb razowy\n"
            "3. Jajka (10 szt)\n"
            "4. Maslo orzechowe\n"
            "5. Woda mineralna\n"
        )
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Utworzono przykładowy plik: {filename}")
    return filename

def demo_priority_queue():
    pq = MinPriorityQueue()
    print("\n--- Kolejka priorytetowa ---")
    
    while True:
        print("\n1. Wstaw element")
        print("2. Pobierz minimum")
        print("3. Zmniejsz priorytet")
        print("4. Zbuduj kolejkę z listy")
        print("5. Pokaż kolejkę")
        print("6. Wstecz")
        
        choice = input("Wybór: ")
        if choice == '1':
            element = input("Element: ")
            try:
                prio = int(input("Priorytet (int): "))
                pq.insert([prio, element])
                print("Dodano.")
            except ValueError: print("Priorytet musi być liczbą.")
        elif choice == '2':
            print(f"Pobrano: {pq.extract_min()}")
        elif choice == '3':
            element = input("Element: ")
            try:
                prio = int(input("Nowy priorytet: "))
                if pq.decrease_priority(element, prio): print("Zmieniono.")
                else: print("Nie znaleziono lub błąd priorytetu.")
            except ValueError: print("Błąd liczby.")
        elif choice == '4':
            data = [[15, 'A'], [3, 'B'], [8, 'C']]
            print(f"Buduję z: {data}")
            pq.build_queue(data)
        elif choice == '5':
            print("Kopiec:", pq)
        elif choice == '6':
            break

def main():
    # Stworzenie pliku testowego przy starcie
    test_file_name = create_shopping_list()
    
    huffman = HuffmanCoding()
    
    while True:
        print("\n=== PROGRAM HUFFMANA ===")
        print(f"Folder roboczy: {BASE_DIR}")
        print("1. Kolejka Priorytetowa")
        print("2. Kompresja pliku")
        print("3. Dekompresja pliku")
        print("4. Wyjście")
        
        choice = input("Wybierz opcję: ")

        if choice == '1':
            demo_priority_queue()
        
        elif choice == '2':
            print(f"\nDostępne pliki w folderze: {[f for f in os.listdir(BASE_DIR) if f.endswith('.txt')]}")
            in_name = input(f"Podaj nazwę pliku (domyślnie '{test_file_name}'): ")
            if not in_name: in_name = test_file_name
            
            out_name = input("Podaj nazwę pliku wynikowego (np. wynik_kompresji.txt): ")
            if not out_name: out_name = "wynik_kompresji.txt"

            # Łączenie folderu bazowego z nazwą pliku
            huffman.compress(get_full_path(in_name), get_full_path(out_name))

        elif choice == '3':
            in_name = input("Podaj nazwę pliku do dekompresji (np. wynik_kompresji.txt): ")
            out_name = input("Podaj nazwę pliku odzyskanego (np. wynik_dekompresji.txt): ")
    
            if in_name and out_name:
                huffman.decompress(get_full_path(in_name), get_full_path(out_name))
            else:
                print("Musisz podać nazwy plików.")

        elif choice == '4':
            print("Koniec.")
            break

if __name__ == "__main__":
    main()