import json
from pprint import pprint
from typing import List


class HamiltonianPath:
    def __init__(self, edge_distances: List[List[float]]) -> None:
        self.n = len(edge_distances)
        self.edge_distances = edge_distances
        self.graph_edges = [
            (i, j) for j in range(self.n) for i in range(self.n) if i < j
        ]
        self.connect_list = [[] for _ in range(self.n)]

        for (src, dest) in self.graph_edges:
            self.connect_list[src].append(dest)
            self.connect_list[dest].append(src)

        self.path_cost_dict = {}
        self.source_len_cost_matrix = [
            [1e9 for _ in range(self.n + 1)] for _ in range(self.n)
        ]
        self.result = {source: None for source in range(self.n)}

    def find_paths(self) -> None:
        for start in range(self.n):
            path = [start]

            visited = [False] * self.n
            visited[start] = True

            self.hamiltonian_paths(start, visited, path)

    def hamiltonian_paths(
        self,
        index: int,
        visited: List[List[bool]],
        path: List[int],
    ) -> None:
        if len(path) == self.n:
            cost = self.path_cost(path)

            if self.compare_source_len_cost(path, cost):
                self.save_path(path)

            return

        for node in self.connect_list[index]:

            if not visited[node]:
                visited[node] = True
                path.append(node)
                cost = self.path_cost(path)

                if self.compare_source_len_cost(path, cost):
                    self.hamiltonian_paths(node, visited, path)

                visited[node] = False
                path.pop()

    def compare_source_len_cost(self, path: List[int], cost: float) -> bool:
        start_index = path[0]
        lenght = len(path)
        val = self.source_len_cost_matrix[start_index][lenght]
        if cost > val:
            return False

        self.source_len_cost_matrix[start_index][lenght] = cost
        return True

    def path_cost(self, path: List[int]) -> float:
        path_key = "-".join(map(str, path))

        if path_key in self.path_cost_dict:
            return self.path_cost_dict[path_key]

        cost = 0
        for i in range(len(path) - 1):
            x = path[i]
            y = path[i + 1]
            cost += self.edge_distances[x][y]

        self.path_cost_dict[path_key] = cost
        return cost

    def save_path(self, path: List[int]) -> None:
        start_index = path[0]
        cost = self.path_cost(path)
        self.result[start_index] = path.copy()
        print("=" * 64)
        print("Source:", start_index, "Path:", path, "Cost:", cost)


if __name__ == "__main__":
    with open("8n_distances.json", "r") as json_file:
        distances = json.load(json_file)

    hamiltonian = HamiltonianPath(distances)
    hamiltonian.find_paths()
    print("=" * 64)
    print()
    pprint(hamiltonian.result)
