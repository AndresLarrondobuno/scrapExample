import csv

class CsvExporter:
    def __init__(self):
        self.csv = None


    def createCsvFile(self, path: str, header: list[str]):
        self.csv = CsvFile(path, header)


    def append(self, data: list):
        with open(self.csv.path, "a", newline='', encoding="UTF-8") as file:
            writer = csv.writer(file)
            writer.writerow(data)


class CsvFile:
    def __init__(self, path: str, header: list[str]):
        self.path = path
        self.header = header
        
        with open(self.path, "w", newline='', encoding="UTF-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)