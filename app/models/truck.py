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

    # return the 00:00 representation of a decimal value
    def decimal_to_hours(self, decimal_time):
        in_minutes = (decimal_time * 60)
        partial_hour = in_minutes % 60
        real_hours = (in_minutes - partial_hour) / 60

        hours = f"{int(float(real_hours))}".zfill(2)
        minutes = f"{round(partial_hour)}".zfill(2)

        half = "PM" if real_hours > 12 else "AM"
        return f"{hours}:{minutes} {half}"

    # return the decimal representation of a 00:00 value
    def hours_to_decimal(self, hours_time):
        (h, m) = hours_time.split(':')
        return int(h) + (int(m)/60)

    def deliver_route(self, get_package_by_id, report_time):
        totals = {'miles': 0.0}
        delivery_report = list([])

        is_time_report = len(report_time) > 0

        # O(n)
        # this is the callback provided to the `Route.travel_route` method
        # it will travel the route and generate the values for the report
        def travel_route(origin, destination):
            travel_time = self.route.get_time_between_places(origin, destination)
            distance = self.route.find_distance_between_places(origin, destination)

            # tracking miles and elapsed time
            totals['miles'] = totals['miles'] + distance
            self.elapsed_time = self.elapsed_time + travel_time

            # by package in the place,
            for _, package_id in enumerate(destination.packages_ids):
                delivery_time = self.start_time + self.elapsed_time

                # are we getting a report based on a specific time?
                if is_time_report:
                    time_report_status = PackageStatus.IN_ROUTE

                    param_time = self.hours_to_decimal(report_time)
                    passed_time = param_time > delivery_time

                    # has the package been delivered already?
                    if passed_time:
                        time_report_status = PackageStatus.DELIVERED
                    elif param_time < self.start_time:
                        time_report_status = PackageStatus.IN_ORIGIN

                    # if the package has been not delivered, we use the current time
                    if time_report_status is not PackageStatus.DELIVERED:
                        delivery_time = param_time

                    get_package_by_id(package_id).status = time_report_status
                else:
                    get_package_by_id(package_id).status = PackageStatus.DELIVERED

                log_time = self.decimal_to_hours(delivery_time)

                delivery_report.append(f"{package_id.zfill(2)} | {get_package_by_id(package_id).status.value.zfill(9).replace('0', ' ')} @ {log_time} in Truck {self.id} | `{destination.place_street}` in `{destination.street_address}`")

        self.route.travel_route(travel_route)

        return (totals['miles'], delivery_report)
