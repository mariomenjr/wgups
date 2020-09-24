
class Route(object):
    CONSTANT_SPEED = 18

    def __init__(self, places):
        self.places = places
        self.time = 0
        self.miles = 0

        self.calculate_cost()

    # this method sole purpose is helping us avoid duplicated code
    # it provides a loop interface and a callback is provided 
    # so the actions in the call back get called in each loop
    # passign origin and destination places
    # as the system is traveling the route
    # Complexity: O(n)
    def travel_route(self, callback):
        for i, origin in enumerate(self.places):
            j = i + 1
            if j == len(self.places): break
            
            callback(origin, self.places[j])

    # Complexity: O(n)
    def calculate_cost(self):
        # the whole cost in time and miles is calculated for this truck
        def accumulate_props(origin, destination):
            self.time = self.time + self.get_time_between_places(origin, destination)
            self.miles = self.miles + self.find_distance_between_places(origin, destination)
        
        self.travel_route(accumulate_props)

    # Complexity: O(1)
    def get_time_between_places(self, one, two):
        distance = float(one.points[two.index])
        return distance / self.CONSTANT_SPEED

    # Complexity: O(1)
    def find_distance_between_places(self, one, two):
        return float(one.points[two.index])
        