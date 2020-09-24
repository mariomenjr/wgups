from .utils.hash_table import HashTable
from .utils.distance_matrix import DistanceMatrix
from .utils.edge_cases import EdgeCases
from .models.truck import Truck
from .models.route import Route

import sys

class App(object):

    def __init__(self):
        self.__packages = None
        self.__places = None
        self.__distance_matrix = None

    # Complexity: O(1)
    def get_packages(self):
        return self.__packages

    # Complexity: O(n)
    def set_packages(self, packages):
        self.__packages = HashTable(size=len(packages))
        for package in packages:
            self.__packages.add(package.id, package)

    # Complexity: O(n)
    def set_assumptions(self):
        # set assumptions
        EdgeCases.set_cannot_leave_before_905_grouping(self.__packages)
        EdgeCases.set_same_truck_same_time_grouping(self.__packages)
        EdgeCases.set_only_truck_2_grouping(self.__packages)

    # Complexity: O(1)
    def get_distances_matrix(self):
        return self.__distance_matrix

    # Complexity: O(n^3)
    def set_distances_matrix(self, places):
        self.__distance_matrix = DistanceMatrix()
        self.__distance_matrix.feed(places)
        
        # gets all the distances related to each package, 
        # and creates the nearest property 
        # which will helps us build the best route
        self.__places = self.__distance_matrix.fill_closest(places)

    # Complexity: O(1)
    def packages_count(self):
        return self.get_packages().get_count()

    # Complexity: O(1)
    def count_distances(self):
        count = self.get_distances_matrix().get_count()
        return count * count

    # Complexity: O(1)
    def get_time_for_report(self):
        return "" if len(sys.argv) <= 1 else sys.argv[1]

    # Complexity: O(n^3)       
    def run(self):
        print(f"App started: there are {self.packages_count()} packages and {self.count_distances()} distances.")
        
        time_report = self.get_time_for_report()

        # setting problem's assumptions
        self.set_assumptions()

        # packages are assigned to places 
        # then places are assigned to trucks
        places = self.assign_packages(self.__places, self.__packages) 
        loaded_trucks = self.load_trucks(places, self.__places[0]) 

        # once each truck has been assigned places
        # the best route is built upon those places
        for truck in loaded_trucks:
            places = self.build_best_route(truck.places)
            truck.route = Route(places)

        deliveries = list([])
        total_miles = 0.0

        # we only have 2 drivers, so truck 3 can only start when truck 1 has came back
        loaded_trucks[2].start_time = loaded_trucks[2].start_time + loaded_trucks[0].route.time
        
        print("\n=============================")
        print("=     TRUCKS DEPARTURE      =")
        print("=============================")

        # the packages are delivered based on the route previously built
        # Complexity: O(n)
        for i, truck in enumerate(loaded_trucks):
            # the trucks need access to the hash table,
            # that's why we send the lambda
            (miles, report)= truck.deliver_route(lambda package_id: self.__packages.get(package_id), time_report)
            
            total_miles = total_miles + miles
            deliveries.extend(report)

            print(f"Truck {i+1} @ {truck.decimal_to_hours(truck.start_time)}")

        print("\n=============================")
        print("=       ALL PACKAGES        =")
        print("=============================")

        # report is printed
        # Complexity: O(n)
        for delivery in deliveries: 
            print(delivery)
        
        print(f"\nTotal miles: {total_miles} miles")

    # Complexity: O(n)
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
    
    # greedy algorithm to find the best route given a list of places
    # based on a list of places, find the best route to reach them all
    # Complexity: O(n^2)
    def build_best_route(self, places, first_index=0):
        places_stack = list([])
        places_count = len(places)

        # have we included this place in the route yet?
        routed_places_indexs = dict({first_index: 0})
        # a map that will help us find the place faster by it's index
        places_by_indexs = {place.index:place for place in places}

        place = places[first_index]
        places_stack.append(place)

        # Complexity: O(n^2)
        while(places_count > len(routed_places_indexs.keys())): # until I have register them all
            nearest = None

            place_index = 0
            closest_index = 0

            # the flag is clear in each loop
            # this helps avoiding skip any place
            is_place_found = False
            # Complexity: O(n)
            while(not is_place_found):
                # the nearest places is selected
                place_index = place.nearest[closest_index].place_index

                # has this place been routed in a loop before?
                been_routed = place_index in routed_places_indexs.keys()
                # is this place non-existence?
                not_there = places_by_indexs.get(place_index) == None

                is_place_found = not (been_routed or not_there)
                if not is_place_found:
                    # this will help the algorithm select the next nearest place
                    closest_index = closest_index + 1
                else:
                    # the place is routed
                    routed_places_indexs[place_index] = closest_index

            nearest = places_by_indexs.get(place_index)
            places_stack.append(nearest)

            place = nearest
        # then, at the end of this loop: O(n^2)

        # at the end, not matter what
        # we need to get back to the origin
        places_stack.append(places[first_index])
        return places_stack

    # this method will create an stack of places beloging to a route
    # Complexity: O(n^3)
    def load_trucks(self, places_stack, start_place):
        # just use 2 trucks
        trucks = list([
            Truck(1, lambda pkg: pkg.group == "same"), 
            Truck(2, lambda pkg: pkg.start_time == 9.0833, start_time=9.0833), 
            Truck(3, lambda pkg: pkg.assigned_truck == 2)])
        
        totals = dict()
        totals["packages"] = 0

        # general track of places routed
        routed_places_by_street_address = dict()
        # specific truck's track of places routed
        routed_places_in_truck_by_street_address = list([dict() for _ in range(len(trucks))])
        
        # register places in both tracks, general and truck's
        # Complexity: O(1)
        def route_place_in_truck(place, truck_tuple):
            (k, truck) = truck_tuple

            # the place is registered in this trucks route
            routed_places_by_street_address[place.street_address] = place
            # and also globally, so we don't route this place in other truck
            routed_places_in_truck_by_street_address[k][place.street_address] = place

            # keeping track of the number of packages
            # help us keep the truck loaded with the allowed number of packages
            packages_count = len(routed_places_by_street_address[place.street_address].packages_ids)
            truck.packages_count = truck.packages_count + packages_count
            
            totals["packages"] = totals.get('packages') + packages_count

        # only allow registration of places based on:
        # 1. Is a package already on any truck?
        # 2. Is the truck full?
        # Complexity: O(n^3)
        def load_packages_by_place(callback):
            for place in places_stack:

                # a flag is clear
                # so we don't miss a package
                is_place_routed = False
                for package_id in place.packages_ids:
                    package = self.__packages.get(package_id)

                    # by each truck, 
                    # we need to figure out if the place for a package has been included in the roue
                    for k, truck in enumerate(trucks):
                        is_place_routed = routed_places_by_street_address.get(place.street_address) is not None
                        if is_place_routed: break

                        # keeping the number of packges in each truck in control
                        if truck.packages_count < truck.MAX_ALLOWED_PACKAGES:
                            callback(package, place, (k, truck))
                        
                    if is_place_routed: break

        # Load special packages
        # Complexity: O(n^3)
        def handle_special_packages(package, place, truck_tuple):
            (_, truck) = truck_tuple
            if truck.check_edge_case(package):
                route_place_in_truck(place, truck_tuple)
        load_packages_by_place(handle_special_packages)

        # Once I distributed the special cases, distribute the rest
        # Complexity: O(n^3)
        def handle_normal_packages(package, place, truck_tuple):
            route_place_in_truck(place, truck_tuple)
        load_packages_by_place(handle_normal_packages)

        # put the list in the truck
        # Complexity: O(n)
        for k, truck in enumerate(trucks):
            truck.places = list([])
            truck.places.append(start_place)
            truck.places.extend(routed_places_in_truck_by_street_address[k].values())

        return trucks # [delivery for delivery in deliveries]
