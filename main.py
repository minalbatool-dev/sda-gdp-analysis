import json
from core import TransformationEngine
from plugins import CSVReader, JSONReader, ConsoleWriter

# Factory Registries
INPUT_DRIVERS = {
    "csv": CSVReader,
    "json": JSONReader
}

OUTPUT_DRIVERS = {
    "console": ConsoleWriter
}


def bootstrap():
    # 1. Load configuration
    with open("config.json", "r") as f:
        config = json.load(f)

    input_type = config["input"]["type"]
    input_path = config["input"]["path"]
    output_type = config["output"]["type"]
    parameters = config["parameters"]

    # 2. Instantiate Sink
    sink_class = OUTPUT_DRIVERS[output_type]
    sink = sink_class()

    # 3. Instantiate Core (Dependency Injection)
    engine = TransformationEngine(sink, parameters)

    # 4. Instantiate Input (Inject Core as Service)
    input_class = INPUT_DRIVERS[input_type]
    reader = input_class(input_path, engine)

    # 5. Execute Pipeline
    reader.read()


if __name__ == "__main__":
    bootstrap()