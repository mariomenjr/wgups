class DistanceMatrix(object):

    def __init__(self):
        self.__mapped_addresses = dict()
        self.__matrix = []
        pass

    def get_count(self):
        return len(self.__matrix)

    def feed(self, distances_list):
        for index, row in enumerate(distances_list):
            self.__mapped_addresses[row.street_address] = index
            self.__matrix.append(row.points)

        matrix_height = len(distances_list)
        matrix_width = len(self.__mapped_addresses)

        if matrix_height != matrix_width:
            raise TypeError(
                f"Distance matrix isn't square ({matrix_height}x{matrix_width})")
    
    
