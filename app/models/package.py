import enum


class PackageStatus(enum.Enum):
    IN_ORIGIN = 0
    IN_ROUTE = 1
    DELIVERED = 2


class Package(object):

    def __init__(self, line, index):
        self.index = index

        self.id = line[0].strip()
        self.street_address = line[1].strip()
        self.city = line[2].strip()
        self.state = line[3].strip()
        self.zip = line[4].strip()
        self.delivery_deadline = line[5].strip()
        self.mass = line[6].strip()
        self.notes = line[7].strip()

        self.start_time = 8
        self.assigned_truck = None
        self.group = None
