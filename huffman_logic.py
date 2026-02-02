import os
from priority_queue import MinPriorityQueue

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return other and self.freq == other.freq

class HuffmanCoding:
    SEPARATOR = "##############################"  # Stała dla bezpieczeństwa

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
        # Lista wszystkich węzłów (jeszcze nie ułożonych w kopiec)
        nodes_list = []
        for key in frequency:
            node = HuffmanNode(key, frequency[key])
            nodes_list.append(node)
            
        # Inicjalizacja kolejki
        self.heap = MinPriorityQueue()
        
        # Algorytm Floyda (czas liniowy zamiast wstawiania w pętli)
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
        if root is None: return
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        self.codes = {}
        self.reverse_mapping = {}
        if not self.heap.heap: return
        root = self.heap.heap[0]
        if root.char is not None:
             self.codes[root.char] = "0"
             self.reverse_mapping["0"] = root.char
             return
        self.make_codes_helper(root, "")

    def get_encoded_text(self, text):
        return "".join([self.codes[char] for char in text])

    def compress(self, input_path, output_path):
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"Nie znaleziono pliku {input_path}")
            return

        if not text:
            print("Plik jest pusty.")
            return

        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()
        encoded_text = self.get_encoded_text(text)
        
        # Wizualizacja
        print(f"\n{'Znak':<10} | {'Wystąpienia':<8} | {'Kod'}")
        print("-" * 35)
        for char, code in self.codes.items():
            disp = char
            if char == '\n': disp = '\\n'
            elif char == ' ': disp = "' '"
            print(f"{disp:<10} | {frequency[char]:<8} | {code}")
        print("-" * 35)

        with open(output_path, 'w', encoding='utf-8') as output:
            for char, code in self.codes.items():
                # Zabezpieczenie spacji i entera
                if char == '\n': char_repr = '<NL>'
                elif char == ' ': char_repr = '<SP>'
                else: char_repr = char
                
                output.write(f"{char_repr}:{frequency[char]}-{code}\n")
            
            output.write(f"{self.SEPARATOR}\n")
            output.write(encoded_text)
        
        print(f"\nWynik zapisano w: {os.path.basename(output_path)}")

    def decompress(self, input_path, output_path):
        self.reverse_mapping = {}
        encoded_text = ""
        
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {input_path}")
            return

        is_data = False
        for line in lines:
            line = line.rstrip('\n') 
            
            if line == self.SEPARATOR:
                is_data = True
                continue
            
            if not is_data:
                if not line: continue
                try:
                    parts = line.split('-')
                    code = parts[-1]
                    rest = "-".join(parts[:-1])
                    last_colon = rest.rfind(':')
                    char_part = rest[:last_colon]

                    # Obsługa znaczników
                    if char_part == '<NL>': char_part = '\n'
                    elif char_part == '<SP>': char_part = ' '
                    
                    self.reverse_mapping[code] = char_part
                except ValueError:
                    pass
            else:
                encoded_text += line

        decoded_text = ""
        current_code = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text += self.reverse_mapping[current_code]
                current_code = ""

        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(decoded_text)


        print(f"Dekompresja zakończona. Wynik znajduje się w: {os.path.basename(output_path)}")
