import os
from priority_queue import MinPriorityQueue

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Operatory potrzebne do działania kolejki priorytetowej
    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if other is None: return False
        return self.freq == other.freq
    
    def __repr__(self):
        return f"Node({self.char}:{self.freq})"

class HuffmanCoding:
    def __init__(self):
        self.heap = MinPriorityQueue()
        self.codes = {}
        self.reverse_mapping = {}

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            frequency[character] = frequency.get(character, 0) + 1
        return frequency

    def make_heap(self, frequency):
        nodes_list = []
        for key in frequency:
            node = HuffmanNode(key, frequency[key])
            nodes_list.append(node)
        
        # Poprawiona metoda build_queue (Algorytm Floyda)
        self.heap.build_queue(nodes_list)

    def merge_nodes(self):
        while len(self.heap.heap) > 1:
            node1 = self.heap.extract_min()
            node2 = self.heap.extract_min()

            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            self.heap.insert(merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = self.heap.heap[0]
        current_code = ""
        self.make_codes_helper(root, current_code)

    def compress(self, input_path, output_path):
        """
        Kompresuje plik używając zapisu binarnego.
        """
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {input_path}")
            return

        # Budowa drzewa i kodów
        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        # Kodowanie tekstu do ciągu zer i jedynek
        encoded_text_bits = ""
        for char in text:
            encoded_text_bits += self.codes[char]

        # Zapis do pliku binarnego
        with open(output_path, 'wb') as output:
            # Zapis słownika (jako tekst)
            output.write(b"S\xc5\x81OWNIK:\n") # "SŁOWNIK:" w UTF-8
            for char, code in self.codes.items():
                # Zamiana znaków specjalnych na czytelne
                display_char = char
                if char == '\n': display_char = '<NL>'
                elif char == ' ': display_char = '<SP>'
                
                line = f"{display_char}: {frequency[char]} - {code}\n"
                output.write(line.encode('utf-8'))
            
            output.write(b"DANE:\n")

            # Bit Packing (zamiana 01011000 -> bajt)
            padding = 8 - (len(encoded_text_bits) % 8)
            if padding == 8: padding = 0
            
            # Dopełnienie zerami, aby mieć pełne bajty
            encoded_text_bits += "0" * padding

            # Konwersja 8-bitowych fragmentów na bajty
            byte_array = bytearray()
            for i in range(0, len(encoded_text_bits), 8):
                byte_chunk = encoded_text_bits[i:i+8]
                byte_array.append(int(byte_chunk, 2))
            
            output.write(byte_array)

            # Zapis stopki z paddingiem (tekstowo)
            # Żeby wiedzieć ile bitów zignorować przy odczycie
            output.write(f"\nPADDING: {padding}".encode('utf-8'))

        print("Kompresja zakończona sukcesem!")

    def decompress(self, input_path, output_path):
        """
        Dekompresuje plik binarny.
        """
        try:
            # Otwieram binarnie, bo sekcja DANE zawiera surowe bajty
            with open(input_path, 'rb') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {input_path}")
            return

        # Rozdzielenie sekcji (Słownik, Dane, Padding)
        try:
            # Szukanie separatora "DANE:\n"
            data_separator = b"DANE:\n"
            split_idx = content.find(data_separator)
            
            if split_idx == -1:
                print("Błąd: Uszkodzony format pliku (brak sekcji DANE)")
                return

            header_part = content[:split_idx].decode('utf-8')
            binary_and_footer = content[split_idx + len(data_separator):]

            # Szukanie stopki "PADDING: X" od końca
            # Szukanie ostatniego wystąpienia "\nPADDING:"
            padding_marker = b"\nPADDING: "
            padding_idx = binary_and_footer.rfind(padding_marker)

            if padding_idx == -1:
                print("Błąd: Brak informacji o PADDINGU")
                return
            
            binary_data = binary_and_footer[:padding_idx]
            footer_part = binary_and_footer[padding_idx + len(padding_marker):].decode('utf-8')
            
            padding = int(footer_part.strip())

        except Exception as e:
            print(f"Błąd podczas parsowania pliku: {e}")
            return

        # Odtworzenie słownika (Reverse Mapping)
        self.reverse_mapping = {}
        lines = header_part.split('\n')
        for line in lines:
            if not line or line.startswith("SŁOWNIK"): continue
            # Format: "z: freq - kod"
            parts = line.split(' - ')
            if len(parts) < 2: continue
            
            code = parts[1].strip()
            left_side = parts[0]
            
            # Wyciągnięcie znaku (może być dwukropek, więc szukamy ostatniego :)
            last_colon = left_side.rfind(':')
            char_part = left_side[:last_colon]
            
            if char_part == '<NL>': char_part = '\n'
            elif char_part == '<SP>': char_part = ' '
            
            self.reverse_mapping[code] = char_part

        # Konwersja bajtów z powrotem na ciąg bitów "0101..."
        bit_string = ""
        for byte in binary_data:
            # Formatowanie do 8 bitów ( 5 -> 00000101)
            bit_string += f"{byte:08b}"

        # Usunięcie paddingu
        if padding > 0:
            bit_string = bit_string[:-padding]

        # Dekodowanie bitów na tekst
        decoded_text = ""
        current_code = ""
        for bit in bit_string:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text += self.reverse_mapping[current_code]
                current_code = ""

        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(decoded_text)

        print(f"Dekompresja zakończona! Wynik w: {output_path}")