import heapq


class Astar:
    """
    Algorytm do znajowania najkrótszej ścieżki w grafie ważonym.
    """
    def __init__(self, level):
        self.level = level

    @staticmethod
    def _heuristic(a, b):
        """
        Funkcja heurystyczna dla algorytmu A* - (odległość Manhattan)
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def _reconstruct_path(came_from, current):
        """
        Odwarza ścieżkę do celu na podstawie mapy punktów poprzedzających
        :param came_from: słownik przechowujący punkty poprzedzające na najkrótszej ścieżce
        :param current: aktualny punkt, od którego zaczynamy odbudowę ścieżki
        """
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        return path[::-1]

    @staticmethod
    def _get_neighbors(current):
        """
        Generuje sąsiadów dla danego punktu na podstawie przesunięć w poziomie i pionie.
        """
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        result = [(current[0] + i, current[1] + j) for i, j in neighbors]
        return result

    def _is_valid_point(self, point, goal):
        """
        Sprawdza, czy punkt jest wewnątrz granic i nie jest przeszkodą lub graczem
        """
        # x, y = point
        # return 0 <= x < self.level.width and 0 <= y < self.level.height and self.level.grid[y][x] != 1
        x, y = point
        valid = (0 <= x < self.level.width and 0 <= y < self.level.height and
                 (self.level.grid[y][x] != 1 or point == goal))
        return valid

    def _update_scores(self, neighbor, current, gscore, fscore, goal, open_set, came_from):
        """
        Aktualizuje wartości gscore i fscore oraz dodaje sąsiada do open_set
        """
        # Obliczanie tymczasowego kosztu dotarcia do sąsiada
        tentative_g_score = gscore[current] + 1

        # Sprawdzenie, czy tymczasowy koszt jest niższy niż obecny koszt dotarcia do sąsiada
        if tentative_g_score < gscore.get(neighbor, float('inf')):
            # Aktualizacja informacji o poprzedniku na najkrótszej ścieżce
            came_from[neighbor] = current

            # Aktualizacja kosztu dotarcia do sąsiada
            gscore[neighbor] = tentative_g_score

            # Obliczenie sumarycznego kosztu dotarcia i heurystyki dla sąsiada
            fscore[neighbor] = tentative_g_score + self._heuristic(neighbor, goal)

            # Dodanie sąsiada do kolejki priorytetowej open_set
            heapq.heappush(open_set, (fscore[neighbor], neighbor))

    def find_path(self, start, goal):
        """
        Przeszukuje przestrzeń stanów, aby znaleźć ścieżkę od punktu startowego do celu.
        :param start:
        :param goal:
        :return:
        """
        open_set = []   # kolejka priorytetowa, przechowuje punkty do przetworzenia
        close_set = set()  # punkty które już zostały przetworzone
        came_from = {}  # słownik przechowujący punkty poprzedzające na najkrótszej ścieżce
        gscore = {start: 0}  # koszt dotarcia do punktu
        fscore = {start: self._heuristic(start, goal)}  # suma kosztów g i heurystyki

        # dodanie punktu startowego do kolejki priorytetowej
        heapq.heappush(open_set, (fscore[start], start))

        # Pętla główna algorytmu
        while open_set:
            # pobranie i usunięcie z kolejki priorytetowej punktu o najniższym koszcie
            _, current = heapq.heappop(open_set)

            # jeśli aktualny punkt równa się celowi, zwraca ścieżkę do tego punktu
            if current == goal:
                return self._reconstruct_path(came_from, current)

            # Dodanie aktualnego punktu do zbioru przetworzonych
            close_set.add(current)

            # iteracja po sąsiadach aktualnego punktu
            for neighbor in self._get_neighbors(current):
                # Sprawdzenie, czy sąsiad jest prawidłowy i czy nie został jeszcze przetworzony
                if not self._is_valid_point(neighbor, goal) or neighbor in close_set:
                    continue
                # Aktualizacja kosztów dla sąsiada oraz dodanie go do kolejki priorytetowej
                self._update_scores(neighbor, current, gscore, fscore, goal, open_set, came_from)

        # Jeśli nie udało się znaleźć ścieżki, zwraca None
        return None
