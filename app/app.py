from .models.hash_table import HashTable


class App(object):
    _TRUCK_SPEED = 18
    _MAX_ALLOWED_PACKAGES = 16

    def __init__(self):
        self.__packages = None
        self.__distances_matrix = []

    def get_packages(self):
        return self.__packages

    def set_packages(self, packages):
        self.__packages = HashTable(size = len(packages))
        for package in packages:
            self.__packages.add(package.id, package)

    def get_distances_matrix(self):
        return self.__distances_matrix

    def set_distances_matrix(self, distances_matrix):
        self.__distances_matrix = distances_matrix

    def packages_count(self):
        return len(self.get_packages())

    def distances_count(self):
        return len(self.get_distances_matrix())

    def run(self):
        print(
            f"App started: there are {self.packages_count()} packages and {self.distances_count()} distances.")
