import string as string


class Distance(object):
    COLUMN_COUNT = 29

    def __init__(self, line):

        # TODO: We should'nt be ignoring lines
        if len(line) == Distance.COLUMN_COUNT:
            street_address = line[1].split("\n")
            self.street_address = street_address[0].strip()
            self.zip = street_address[1].strip()
            self.place_street = line[0].strip()
            self.points = line[2:]
