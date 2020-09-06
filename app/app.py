from .utils.hash_table import HashTable
from .utils.distance_matrix import DistanceMatrix
from .utils.edge_cases import EdgeCases
from .models.truck import Truck


class App(object):
    GOAL_MILES = 145
    TRUCK_SPEED = 18

    TOTAL_PACKAGES = 40

    DRIVERS_COUNT = 2
    TRUCKS_COUNT = 3

    def __init__(self):
        self.__packages = None
        self.__places = None
        self.__distance_matrix = None

    def get_packages(self):
        return self.__packages

    def set_packages(self, packages):
        self.__packages = HashTable(size=len(packages))
        for package in packages:
            self.__packages.add(package.id, package)

    def set_edge_cases_config(self):
        # set assumptions
        EdgeCases.set_cannot_leave_before_905_grouping(self.__packages)
        EdgeCases.set_same_truck_same_time_grouping(self.__packages)
        EdgeCases.set_only_truck_2_grouping(self.__packages)

    def get_distances_matrix(self):
        return self.__distance_matrix

    def set_distances_matrix(self, places):
        self.__distance_matrix = DistanceMatrix()
        self.__distance_matrix.feed(places)

        self.__places = self.__distance_matrix.fill_closest(places)

    def packages_count(self):
        return self.get_packages().get_count()

    def count_distances(self):
        count = self.get_distances_matrix().get_count()
        return count * count

    def run(self):
        print(f"App started: there are {self.packages_count()} packages and {self.count_distances()} distances.")

        self.set_edge_cases_config()

        places = self.assign_packages(self.__places, self.__packages)
        loaded_trucks = self.load_trucks(places, self.__places[0])

        for truck in loaded_trucks:
            truck.route = self.build_best_route(truck.places)
            pass
        
        pass
    
    def assign_packages(self, places, packages):
        places_by_street_address = {place.street_address: place for place in places}

        # distribute packages
        for id in range(1, packages.get_count()):
            package = packages.get(f"{id}")

            place = places_by_street_address.get(package.street_address)
            if place is not None:
                place.packages_ids.append(package.id)

        return places
        
    def build_best_route(self, places, first_index=0):
        places_stack = list([])

        places_count = len(places)
        visited_places_indexs = dict({first_index: 0})
        places_by_indexs = {place.index:place for place in places}

        print(f"Finding best routes...")
        place = places[first_index]
        places_stack.append(place)

        while((places_count - 1) >= len(visited_places_indexs.keys())):
            nearest = None

            place_index = 0
            closest_index = 0

            is_place_found = False
            while(not is_place_found):
                place_index = place.nearest[closest_index].place_index

                been_visited = place_index in visited_places_indexs.keys()
                not_there = places_by_indexs.get(place_index) == None

                is_place_found = not (been_visited or not_there)
                if not is_place_found:
                    closest_index = closest_index + 1
                else:
                    visited_places_indexs[place_index] = closest_index

            nearest = places_by_indexs.get(place_index)
            places_stack.append(nearest)

            print(f"`{place.place_street}` is away from `{nearest.place_street}` by {place.points[nearest.index]} miles")
            place = nearest

        return places_stack

    def load_trucks(self, places_stack, start_place):
        trucks = list([
            Truck(lambda pkg: pkg.group == "same"), 
            Truck(lambda pkg: pkg.start_time == 9.0833, start_time=9.0833), 
            Truck(lambda pkg: pkg.assigned_truck == 2)])
        
        places_by_street_address = list([dict() for truck in range(len(trucks))])
        
        # first load special packages
        for i in range(len(places_stack)):
            place = places_stack[i]

            is_broken = False
            for j in range(len(place.packages_ids)):
                package = self.__packages.get(place.packages_ids[j])

                for index, truck in enumerate(trucks):
                    is_broken = places_by_street_address[index].get(place.street_address) is not None
                    if is_broken: break

                    if truck.check_if_special(package):
                        places_by_street_address[index][place.street_address] = place
                        truck.packages_count = truck.packages_count + len(places_by_street_address[index][place.street_address].packages_ids)

                if is_broken: break                    

        # put the list in the truck
        for index, truck in enumerate(trucks):
            truck.places = list([])
            truck.places.append(start_place)
            truck.places.extend(places_by_street_address[index].values()) 

        return trucks # [delivery for delivery in deliveries]
