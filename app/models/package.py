class Package(object):
    COLUMN_COUNT = 8

    def __init__(self, line):
        columns = f"{line}".split(',')

        # TODO: We should'nt be ignoring lines
        if len(columns) == Package.COLUMN_COUNT:
            self.id = columns[0]
            self.address = columns[1]
            self.city = columns[2]
            self.state = columns[3]
            self.zip = columns[4]
            self.delivery_deadline = columns[5]
            self.mass = columns[6]
            self.notes = columns[7]
