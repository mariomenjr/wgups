class Distance(object):
    COLUMN_COUNT = 29

    def __init__(self, line):

        # TODO: We should'nt be ignoring lines
        if len(line) == Distance.COLUMN_COUNT:
            self.address = line[0]
            self.hub = line[1]
            self.points = line[2:]
