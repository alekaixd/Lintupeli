# HERE ARE ALL POSSIBLE LOCATIONS FOR THE BIRD

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

icaoCodes = ["BR-0673", "EFHK", "EFRN", "EFVA"]
maps = []  # list of submaps
mapsIndex = 0  # tells which submap player is on


class Map:
    def __init__(self, codes: list):
        self.codes = codes
        self.airports = []
        self.InitAirports()

    def __str__(self):
        return f"{self.codes}"

    def InitAirports(self):
        for i in range(0, len(self.codes)):
            self.airports.append(Airport(i, 1, 1))
            if i < len(self.codes) - 1:
                self.airports[i].nextAirport = self.codes[i + 1]
            else:
                return  # should return the next submaps first airport

    def GetAirport(self, index: int):
        return self.airports[index]


class Airport:
    def __init__(self, code: str, weather: int, food: int):
        self.code = code
        self.weather = weather
        self.food = food
        self.nextAirport = []

    def __str__(self):
        return f"Code: {self.code}"


maps.append(Map(icaoCodes))
print(maps[mapsIndex])

position = maps[mapsIndex].GetAirport(2)
print(position.nextAirport)


def ReadMapFile(url: str):
    raw = open(url).read()
    # need to split with ':' aswell to make crossroads
    submaps = raw.replace('\n', '').split(';')
    print(submaps)


ReadMapFile("testmap.map")
