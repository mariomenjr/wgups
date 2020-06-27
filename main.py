from app.csv_loader import CsvLoader

if __name__ == "__main__":
    loader = CsvLoader()
    loader.load(["data/distances", "data/packages"])
