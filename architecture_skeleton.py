# auto‑generated Python skeleton (from architecture.puml)
from typing import Protocol, List, Any, Dict

class Main:
    def bootstrap(self) -> None:
        pass


class DataSink(Protocol):
    def write(self, records: List[Dict[str, Any]]) -> None:
        ...


class PipelineService(Protocol):
    def execute(self, raw_data: List[Any]) -> None:
        ...


class TransformationEngine(PipelineService):
    def __init__(self, sink: DataSink, config: Dict[str, Any]) -> None:
        self.sink = sink
        self.config = config

    def execute(self, raw_data: List[Any]) -> None:
        pass


class CSVReader:
    def __init__(self, filepath: str, service: PipelineService) -> None:
        self.filepath = filepath
        self.service = service

    def read(self) -> None:
        pass


class JSONReader:
    def __init__(self, filepath: str, service: PipelineService) -> None:
        self.filepath = filepath
        self.service = service

    def read(self) -> None:
        pass


class ConsoleWriter:
    def __init__(self, **kwargs) -> None:
        pass

    def write(self, data: Any) -> None:
        pass


class JSONWriter:
    def __init__(self, path: str = "output.json", **kwargs) -> None:
        self.path = path

    def write(self, data: Any) -> None:
        pass


class CSVWriter:
    def __init__(self, path: str = "output.csv", **kwargs) -> None:
        self.path = path

    def write(self, data: Any) -> None:
        pass
