import enum


class TruckStatus(enum.Enum):
    IN_ORIGIN = 0
    IN_ROUTE = 1


class Truck(object):

    MAX_ALLOWED_PACKAGES = 16

    def __init__(self, comparitor, start_time=8):
        self.route = list([])
        self.places = list([])

        self.status = TruckStatus.IN_ORIGIN
        self.start_time = start_time

        self.packages_count = 0
        self.check_if_special = comparitor
