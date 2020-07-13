import string as string


class Place(object):

    def __init__(self, line):
        street_address = line[1].split("\n")
        self.street_address = street_address[0].strip()
        self.zip = street_address[1].strip()
        self.place_street = line[0].strip()
        self.points = line[2:]

        self.closest_places = list([])
