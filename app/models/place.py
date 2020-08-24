import string as string


class Place(object):

    def __init__(self, line, index):
        self.index = index
        
        street_address = line[1].split("\n")
        self.street_address = street_address[0].strip()
        self.zip = street_address[1].strip()
        self.place_street = line[0].split("\n")[0].strip()
        self.points = line[2:]

        self.nearest = list([])
        self.packages_ids = list([])
