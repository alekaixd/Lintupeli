import json


class Map:  # https://www.w3schools.com/dsa/dsa_data_graphs_implementation.php
    def __init__(self, size: int):
        self.adjacent = [[None] * size for s in range(size)]
        self.size = size
        self.vertex = [''] * size

    def AddEdge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adjacent[u][v] = weight

    def AddVertexData(self, vertex, icao):
        if 0 <= vertex < self.size:
            self.vertex[vertex] = icao

    def print_graph(self):
        print("Adjacency Matrix:")
        for row in self.adjacent:
            print(' '.join(map(lambda x: str(x) if x is not None else '0', row)))
        print("\nVertex Data:")
        for vertex, data in enumerate(self.vertex):
            print(f"Vertex {vertex}: {data}")

    def GetPaths(self, location: int):
        # returns avaible paths from location vertex specifically icao code
        roads = []
        for v in range(len(self.adjacent[location])):
            if self.adjacent[location][v] is not None:
                roads.append(self.vertex[v])
        return roads

    def GetIcaoIndex(self, icao: str):
        for i in range(len(self.vertex)):
            if self.vertex[i] == icao:
                return i


g = None


def GetNextPort(icao: str):
    ports = g.GetPaths(g.GetIcaoIndex(icao))
    return ports


def GetFirstPort():
    return g.vertex[0]


def ReadMapJson(path: str):
    global g
    with open(path, 'r') as file:
        data = json.load(file)
    for map in data.values():
        for arr in map:
            g = Map(len(arr))
            for i, k in enumerate(arr):
                g.AddVertexData(i, k)
                for edge in arr[k]["edges"]:
                    g.AddEdge(i, edge, 1)  # weight can be ignored
    return


def InitMap():
    ReadMapJson("./maps/FinlandToItaly.json")


# InitMap()
# print(g.GetIcaoIndex("EGBB"))
