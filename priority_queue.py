class MinPriorityQueue:
    """
    Implementacja kolejki priorytetowej (Kopiec Min).
    """
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def min_heapify(self, i):
        smallest = i
        l = self.left_child(i)
        r = self.right_child(i)
        n = len(self.heap)

        if l < n and self.heap[l] < self.heap[smallest]:
            smallest = l
        if r < n and self.heap[r] < self.heap[smallest]:
            smallest = r

        if smallest != i:
            self.swap(i, smallest)
            self.min_heapify(smallest)

    def insert(self, item):
        """Dodaje element do kolejki."""
        self.heap.append(item)
        current = len(self.heap) - 1
        
        while current > 0 and self.heap[current] < self.heap[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)

    def extract_min(self):
        """Usuwa i zwraca element o najmniejszym priorytecie."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.min_heapify(0)
        return root

    def decrease_priority(self, item_matcher, new_priority):
        """
        Zmniejsza priorytet elementu.
        Zakłada strukturę [priorytet, element].
        """
        found_index = -1
        for i, val in enumerate(self.heap):
            if isinstance(val, list) and len(val) > 1 and val[1] == item_matcher:
                found_index = i
                break
        
        if found_index == -1:
            return False

        if new_priority > self.heap[found_index][0]:
            print("Nowy priorytet musi być mniejszy!")
            return False

        self.heap[found_index][0] = new_priority
        current = found_index
        
        while current > 0 and self.heap[current] < self.heap[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)
        return True

    def build_queue(self, data_list):
        """Buduje kopiec z podanej listy"""
        self.heap = data_list[:]
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self.min_heapify(i)

    def __str__(self):
        return str(self.heap)