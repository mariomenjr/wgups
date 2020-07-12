class Package(object):
    COLUMN_COUNT = 8

    def __init__(self, line):

        # TODO: We should'nt be ignoring lines
        if len(line) == Package.COLUMN_COUNT:
            self.id = line[0].strip()
            self.street_address = line[1].strip()
            self.city = line[2].strip()
            self.state = line[3].strip()
            self.zip = line[4].strip()
            self.delivery_deadline = line[5].strip()
            self.mass = line[6].strip()
            self.notes = line[7].strip()
