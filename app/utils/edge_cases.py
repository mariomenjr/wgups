class EdgeCases:

    @staticmethod
    def set_same_truck_same_time_grouping(packages):
        grouped = list([13, 14, 15, 16, 19, 20])
        for i in grouped:
            packages.get(f"{i}").group = "same"

    @staticmethod
    def set_only_truck_2_grouping(packages):
        grouped = list([3, 18, 36, 38])
        for i in grouped:
            packages.get(f"{i}").start_time = 9.0833

    @staticmethod
    def set_cannot_leave_before_905_grouping(packages):
        grouped = list([6, 25, 28, 32])
        for i in grouped:
            packages.get(f"{i}").assigned_truck = 2