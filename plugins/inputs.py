import csv
import json
from typing import List, Any
from core.contracts import PipelineService


class CSVReader:
    def __init__(self, filepath: str, service: PipelineService):
        self.filepath = filepath
        self.service = service

    def read(self) -> None:
        data = []
        with open(self.filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)

        self.service.execute(data)


class JSONReader:
    def __init__(self, filepath: str, service: PipelineService):
        self.filepath = filepath
        self.service = service

    def read(self) -> None:
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.service.execute(data)