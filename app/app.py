from .models.hash_table import HashTable


class App(object):
    _MAX_ALLOWED_PACKAGES = 16
    _TRUCK_SPEED = 18
    _DRIVERS_COUNT = 2
    _TRUCKS_COUNT = 3

    def __init__(self):
        self.__packages = None
        self.__distances_matrix = []
        self.__mapped_addresses = dict()

    def get_packages(self):
        return self.__packages

    def set_packages(self, packages):
        self.__packages = HashTable(size=len(packages))
        for package in packages:
            self.__packages.add(package.id, package)

    def get_distances_matrix(self):
        return self.__distances_matrix

    def set_distances_matrix(self, distances_matrix):
        for index, row in enumerate(distances_matrix):
            self.__mapped_addresses[row.street_address] = index
            self.__distances_matrix.append(row.points)
            del row.points

        matrix_height = len(distances_matrix)
        matrix_width = len(self.__mapped_addresses)

        if matrix_height != matrix_width:
            raise TypeError(
                f"Distance matrix isn't square ({matrix_height}x{matrix_width})")

    def packages_count(self):
        return self.get_packages().get_count()

    def distances_count(self):
        leng = len(self.get_distances_matrix())
        return leng * leng

    def run(self):
        print(
            f"App started: there are {self.packages_count()} packages and {self.distances_count()} distances.")
