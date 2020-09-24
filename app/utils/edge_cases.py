class EdgeCases:

    # Complexity: O(n)
    @staticmethod
    def set_same_truck_same_time_grouping(packages):
        # list of packages that belongs to this edge case
        grouped = list([13, 14, 15, 16, 19, 20])
        for i in grouped:
            packages.get(f"{i}").group = "same"

    # Complexity: O(n)
    @staticmethod
    def set_only_truck_2_grouping(packages):
        # list of packages that belongs to this edge case
        grouped = list([3, 9, 18, 36, 38])
        for i in grouped:
            packages.get(f"{i}").assigned_truck = 2

    # Complexity: O(n)
    @staticmethod
    def set_cannot_leave_before_905_grouping(packages):
        # list of packages that belongs to this edge case
        grouped = list([6, 25, 28, 32])
        for i in grouped:
            # the package 9 address will be corrected at 10:20
            # we will set this truck to leave at 10:30
            packages.get(f"{i}").start_time = 10.5 
