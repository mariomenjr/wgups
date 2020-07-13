from app.models.package import Package
from app.models.distance import Distance
from app.utils.csv_loader import CsvLoader
from app.app import App

if __name__ == "__main__":
    PATH_PACKAGES = "data/packages"
    PATH_DISTANCES = "data/distances"

    loaded = CsvLoader().load([{'path': PATH_PACKAGES, 'model': Package},
                               {'path': PATH_DISTANCES, 'model': Distance}])
    app = App()

    app.set_packages(loaded.get(PATH_PACKAGES))
    app.set_distances_matrix(loaded.get(PATH_DISTANCES))

    del loaded

    app.run()
