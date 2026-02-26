import json
from core.engine import TransformationEngine
from core.contracts import DataSink


# Mock Output (for testing only)
class MockSink(DataSink):
    def write(self, data):
        print("\n===== TEST OUTPUT =====")
        for key in data:
            print(f"{key} -> type: {type(data[key])}")


def load_test_data():
    with open("data/gdp_with_continent_filled.csv", encoding="utf-8") as f:
        import csv
        return list(csv.DictReader(f))


def main():
    config = {
        "continent": "Asia",
        "year": 2020,
        "start_year": 2015,
        "end_year": 2020
    }

    sink = MockSink()
    engine = TransformationEngine(sink, config)

    data = load_test_data()
    engine.execute(data)


if __name__ == "__main__":
    main()