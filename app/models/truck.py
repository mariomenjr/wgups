class Truck(object):

    MAX_ALLOWED_PACKAGES = 16

    def __init__(self, comparitor):
        self.route = list([])
        self.places = list([])

        self.packages_count = 0
        self.check_if_special = comparitor
    
