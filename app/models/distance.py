class Distance(object):
    COLUMN_COUNT = 29

    def __init__(self, line):
        columns = f"{line}".split(',')

        # TODO: We should'nt be ignoring lines
        if len(columns) == Distance.COLUMN_COUNT:
            self.address = columns[0]
            self.hub = columns[1]
            self.points = columns[2:]
