class Package(object):
    COLUMN_COUNT = 8

    def __init__(self, line):

        # TODO: We should'nt be ignoring lines
        if len(line) == Package.COLUMN_COUNT:
            self.id = line[0]
            self.address = line[1]
            self.city = line[2]
            self.state = line[3]
            self.zip = line[4]
            self.delivery_deadline = line[5]
            self.mass = line[6]
            self.notes = line[7]
