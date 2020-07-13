from .utils.hash_table import HashTable
from .utils.distance_matrix import DistanceMatrix

class App(object):
    MAX_ALLOWED_PACKAGES = 16
    TRUCK_SPEED = 18
    DRIVERS_COUNT = 2
    TRUCKS_COUNT = 3

    def __init__(self):
        self.__packages = None
        self.__distance_matrix = None

    def get_packages(self):
        return self.__packages

    def set_packages(self, packages):
        self.__packages = HashTable(size=len(packages))
        for package in packages:
            self.__packages.add(package.id, package)

    def get_distances_matrix(self):
        return self.__distance_matrix

    def set_distances_matrix(self, distances_list):
        self.__distance_matrix = DistanceMatrix()
        self.__distance_matrix.feed(distances_list)

    def count_packages(self):
        return self.get_packages().get_count()

    def count_distances(self):
        count = self.get_distances_matrix().get_count()
        return count * count

    def run(self):
        print(
            f"App started: there are {self.count_packages()} packages and {self.count_distances()} distances.")
        
        f_street = "4001 South 700 East"
        t_street = "233 Canyon Rd"

        distance = self.get_distances_matrix().between_streets(f_street, t_street)

        pass
