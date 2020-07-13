from app.models.package import Package
from app.models.place import Place
from app.utils.csv_loader import CsvLoader
from app.app import App

if __name__ == "__main__":
    PATH_PACKAGES = "data/packages"
    PATH_PLACES = "data/distances"

    loaded = CsvLoader().load([{'path': PATH_PACKAGES, 'model': Package, 'len': 8},
                               {'path': PATH_PLACES, 'model': Place, 'len': 29}])
    app = App()

    app.set_packages(loaded.get(PATH_PACKAGES))
    app.set_distances_matrix(loaded.get(PATH_PLACES))

    del loaded

    app.run()
