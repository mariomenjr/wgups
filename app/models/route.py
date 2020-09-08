
class Route(object):
    CONSTANT_SPEED = 18

    def __init__(self, places):
        self.places = places
        self.time = 0
        self.miles = 0

        self.calculate_cost()

    def travel_route(self, callback):
        for i, origin in enumerate(self.places):
            j = i + 1
            if j == len(self.places): break;
            
            callback(origin, self.places[j])

    def calculate_cost(self):
        def accumulate_props(origin, destination):
            self.time = self.time + self.get_time_between_places(origin, destination)
            self.miles = self.miles + self.find_distance_between_places(origin, destination)
        
        self.travel_route(accumulate_props)

    def get_time_between_places(self, one, two):
        distance = float(one.points[two.index])
        return distance / self.CONSTANT_SPEED

    def find_distance_between_places(self, one, two):
        return float(one.points[two.index])
        