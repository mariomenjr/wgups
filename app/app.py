from .utils.hash_table import HashTable
from .utils.distance_matrix import DistanceMatrix


class App(object):
    GOAL_MILES = 145
    TOTAL_PACKAGES = 40
    MAX_ALLOWED_PACKAGES = 16
    TRUCK_SPEED = 18
    DRIVERS_COUNT = 2
    TRUCKS_COUNT = 3

    def __init__(self):
        self.__packages = None
        self.__places = None
        self.__distance_matrix = None

    def get_packages(self):
        return self.__packages

    def set_packages(self, packages):
        self.__packages = HashTable(size=len(packages))
        for package in packages:
            self.__packages.add(package.id, package)

    def get_distances_matrix(self):
        return self.__distance_matrix

    def set_distances_matrix(self, places):
        self.__distance_matrix = DistanceMatrix()
        self.__distance_matrix.feed(places)
        self.__places = self.__distance_matrix.fill_closest(places)

    def count_packages(self):
        return self.get_packages().get_count()

    def count_distances(self):
        count = self.get_distances_matrix().get_count()
        return count * count

    def run(self):
        print(
            f"App started: there are {self.count_packages()} packages and {self.count_distances()} distances.")

        self.build_best_route(self.__places)
        # self.load_trucks()

    def build_best_route(self, places, first_index = 0):
        route_stack = list([])
        count_places = len(places)
        visited_places_indexs = dict({first_index: 0})

        print(f"Finding best routes...")
        place = places[first_index]

        while((count_places - 1) >= len(visited_places_indexs.keys())):
            nearest = None
            been_visited = True
            place_index = 0
            index_closest = 0

            while(been_visited):
                place_index = place.closest_places[index_closest].get('place_index')
                been_visited = place_index in visited_places_indexs.keys()
                if been_visited:
                    index_closest = index_closest + 1
                else:
                    visited_places_indexs[place_index] = index_closest

            nearest = places[place_index]
            route_stack.append(nearest)

            print(
                f"... `{place.place_street}` is away from `{nearest.place_street}` by {place.closest_places[0].get('distance')} miles")            

            place = nearest

        return route_stack
