# this script gets called when the player wants location data
# need a list of all map objects.
# map object includes data of the airport
#   - airport code
#   - current weather
#   - food amount

# class map gets data from the airport database before the game starts
# data is stored in an ordered list
#
# we also need a functon that will take 2 airport codes and calculate their distance

# also we need to somehow store a list of airport codes
# external readable file?

# storing the distance between 2 airports is probably dumb so i think i will just calculate them when needed

# example of how the cold value will increase overtime

#   2, 1, 0, 0, 0, ...
#   3, 2, 1, 0, 0, ...
#   4, 3, 2, 1, 0, ...

# also the next airport has a random weather modifier like hail, thunderstorm or sunny.
# when choosing where to go you are given a description of the weather for each route.

# submaps?
# maybe there will be a crossroad where you can choose the fast and trecherous route or
# the safe and longer route.

# map 1 => map 2 or map 3
# map 2 => map 4
# map 3 => map 4
# map 4 => finish

# maps = [(map 1), (map2, map3), (map 4)]

#           - - -
# - - - - <       > - - - finish
#           - - -

# basic version where there cant be crossroads inside crossroads
# will probably rework

# so basically all this is useless cuz i need to use a graph data structure
# it needs to be a directed wheighted connected graph

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
                    g.AddEdge(i, edge, 1)  # weight to be added
    return


def InitMap():
    ReadMapJson("testmap.json")


# InitMap()
# print(g.GetIcaoIndex("EGBB"))
