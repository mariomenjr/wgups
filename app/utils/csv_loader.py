import csv


class CsvLoader(object):

    # Complexity: O(n^2)
    def load(self, items):
        my_dict = dict()
        
        for item in items:
            path = item.get("path")
            with open(f'{path}.csv') as data:
                reader = csv.reader(data)
                for line in reader:
                    if path not in my_dict:
                        my_dict[path] = []
                    if len(line) == item.get("len"):
                        my_dict[path].append(item.get("model")(line, len(my_dict[path])))
        return my_dict
