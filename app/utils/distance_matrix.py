from ..models.nearest import Nearest


class DistanceMatrix(object):

    def __init__(self):
        self.__mapped_addresses = dict()
        self.__matrix = []

    # Complexity: O(n^3)
    def fill_closest(self, places):
        places_count = len(places)
        for i, place in enumerate(places):
            for j in range(i + 1, places_count):
                place.points[j] = places[j].points[i]
            # keep the index for place and sort by short distance
            distances = [Nearest(distance=x, place_index=i)
                         for i, x in enumerate(place.points)]
            distances.sort(key=(lambda item: float(item.distance)))
            place.nearest = list(distances[1:])

        return places

    # Complexity: O(1)
    def get_count(self):
        return len(self.__matrix)

    # Complexity: O(n^2)
    def feed(self, places):
        for i, place in enumerate(places):
            self.__mapped_addresses[place.street_address] = i
            self.__matrix.append(place.points)

        matrix_height = len(places)
        matrix_width = len(self.__mapped_addresses)

        if matrix_height != matrix_width:
            raise TypeError(f"Distance matrix isn't square ({matrix_height}x{matrix_width})")
