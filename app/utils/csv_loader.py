from app.models.package import Package
import csv

class CsvLoader(object):
    def __init__(self):
        pass

    def load(self, paths):
        for path in paths:
            with open(f'{path}.csv') as data:
                reader = csv.reader(data)
                for line in reader:
                    print(Package(line))