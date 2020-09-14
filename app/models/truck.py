import enum
from .package import PackageStatus


class TruckStatus(enum.Enum):
    IN_ORIGIN = 0
    IN_ROUTE = 1


class Truck(object):

    MAX_ALLOWED_PACKAGES = 16

    def __init__(self, truck_id, comparitor, start_time=8):
        self.id = truck_id
        self.check_edge_case = comparitor

        self.places = list([])
        self.route = None

        self.status = TruckStatus.IN_ORIGIN
        self.start_time = start_time

        self.packages_count = 0
        self.elapsed_time = 0

    def decimal_to_hours(self, decimal_time):
        in_minutes = (decimal_time * 60)
        partial_hour = in_minutes % 60
        real_hours = (in_minutes - partial_hour) / 60

        hours = f"{int(float(real_hours))}".zfill(2)
        minutes = f"{round(partial_hour)}".zfill(2)

        half = "PM" if real_hours > 12 else "AM"
        return f"{hours}:{minutes} {half}"

    def deliver_route(self, get_package_by_id):
        delivery_report = list([])

        for _, routed_place in enumerate(self.route.places):
            for _, package_id in enumerate(routed_place.packages_ids):
                get_package_by_id(package_id).status = PackageStatus.IN_ROUTE

        def travel_route(origin, destination):
            travel_time = self.route.get_time_between_places(origin, destination)
            distance = self.route.find_distance_between_places(origin, destination)

            print(f"From {origin.place_street} to {destination.place_street} by {distance}")
            self.elapsed_time = self.elapsed_time + travel_time

            for _, package_id in enumerate(destination.packages_ids):
                now_time = self.start_time + self.elapsed_time
                get_package_by_id(package_id).status = PackageStatus.DELIVERED
                delivery_report.append((package_id, destination, distance, self, f"{PackageStatus.DELIVERED.value} @ {self.decimal_to_hours(now_time)}"))
        
        self.route.travel_route(travel_route)
        print("-----")
        
        return delivery_report
