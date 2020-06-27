class App(object):
    _TRUCK_SPEED = 18
    _MAX_ALLOWED_PACKAGES = 16

    def __init__(self):
        self.__packages = []
        self.__distances = []

    def get_packages(self):
        return self.__packages

    def set_packages(self, packages):
        self.__packages = packages

    def get_distances(self):
        return self.__distances

    def set_distances(self, distances):
        self.__distances = distances

    def packages_count(self):
        return len(self.get_packages())

    def distances_count(self):
        return len(self.get_distances())

    def run(self):
        print(f"App started: there are {self.packages_count()} packages and {self.distances_count()} distances.")
