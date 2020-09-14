from .utils.hash_table import HashTable
from .utils.distance_matrix import DistanceMatrix
from .utils.edge_cases import EdgeCases
from .models.truck import Truck
from .models.route import Route

import sys

class App(object):
    GOAL_MILES = 145

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

    def set_assumptions(self):
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

    def get_time_for_report(self):
        return "" if len(sys.argv) <= 1 else sys.argv[1]
            
    def run(self):
        print(f"App started: there are {self.packages_count()} packages and {self.count_distances()} distances.")
        
        # setting problem's assumptions
        self.set_assumptions()

        places = self.assign_packages(self.__places, self.__packages)
        loaded_trucks = self.load_trucks(places, self.__places[0])
        time = self.get_time_for_report()

        for truck in loaded_trucks:
            places = self.build_best_route(truck.places)
            truck.route = Route(places)

        deliveries = list([])
        total_miles = 0.0

        loaded_trucks[2].start_time = loaded_trucks[2].start_time + loaded_trucks[0].route.time
        
        print("\n=============================")
        print("=     TRUCKS DEPARTURE      =")
        print("=============================")

        for i, truck in enumerate(loaded_trucks):
            (miles, report)= truck.deliver_route(lambda package_id: self.__packages.get(package_id), time)
            
            total_miles = total_miles + miles
            deliveries.extend(report)

            print(f"Truck {i+1} @ {truck.decimal_to_hours(truck.start_time)}")

        print("\n=============================")
        print("=       ALL PACKAGES        =")
        print("=============================")

        for delivery in deliveries: 
            print(delivery)
        
        print(f"\nTotal miles: {total_miles} miles")

    def assign_packages(self, places, packages):
        places_by_street_address = {place.street_address: place for place in places}

        # distribute packages to correct place
        for id in range(packages.get_count()):
            package = packages.get(f"{id + 1}")

            # get package's delivery place
            place = places_by_street_address.get(package.street_address)
            if place is not None:
                place.packages_ids.append(package.id)

        return places
    
    # heuristic algorithm to find the best route given a list of places
    def build_best_route(self, places, first_index=0):
        places_stack = list([])

        places_count = len(places)
        visited_places_indexs = dict({first_index: 0})
        places_by_indexs = {place.index:place for place in places}

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

            # print(f"`{place.place_street}` is away from `{nearest.place_street}` by {place.points[nearest.index]} miles")
            place = nearest

        places_stack.append(places[first_index])
        return places_stack

    def load_trucks(self, places_stack, start_place):
        # just use 2 trucks
        trucks = list([
            Truck(1, lambda pkg: pkg.group == "same"), 
            Truck(2, lambda pkg: pkg.start_time == 9.0833, start_time=9.0833), 
            Truck(3, lambda pkg: pkg.assigned_truck == 2)])
        
        totals = dict()
        totals["packages"] = 0

        routed_places_by_street_address = dict()
        routed_places_in_truck_by_street_address = list([dict() for _ in range(len(trucks))])
        
        def route_place_in_truck(place, truck_tuple):
            (k, truck) = truck_tuple
            routed_places_by_street_address[place.street_address] = place
            routed_places_in_truck_by_street_address[k][place.street_address] = place

            packages_count = len(routed_places_by_street_address[place.street_address].packages_ids)
            truck.packages_count = truck.packages_count + packages_count
            
            totals["packages"] = totals.get('packages') + packages_count

        def load_packages_by_place(callback):
            for place in places_stack:
                is_place_routed = False
                for package_id in place.packages_ids:
                    package = self.__packages.get(package_id)

                    for k, truck in enumerate(trucks):
                        is_place_routed = routed_places_by_street_address.get(place.street_address) is not None
                        if is_place_routed: break

                        if truck.packages_count < truck.MAX_ALLOWED_PACKAGES:
                            callback(package, place, (k, truck))
                        
                    if is_place_routed: break

        # Load special packages
        def handle_special_packages(package, place, truck_tuple):
            (_, truck) = truck_tuple
            if truck.check_edge_case(package):
                route_place_in_truck(place, truck_tuple)

        load_packages_by_place(handle_special_packages)

        # Once I distributed the special cases, distribute the rest
        def handle_normal_packages(package, place, truck_tuple):
            route_place_in_truck(place, truck_tuple)
        load_packages_by_place(handle_normal_packages)

        # put the list in the truck
        for k, truck in enumerate(trucks):
            truck.places = list([])
            truck.places.append(start_place)
            truck.places.extend(routed_places_in_truck_by_street_address[k].values())

        return trucks # [delivery for delivery in deliveries]
