"""Input plugins: data source implementations.

This module provides reader classes that load data from various file formats.
Each reader accepts a PipelineService and calls its execute() method, allowing
the core engine to remain agnostic of file types and parsing details.

Design:
    - No reader imports core business logic
    - Each reader only depends on PipelineService protocol
    - Easy to add new formats (YAML, SQL, API, etc.) without modifying core

Usage:
    >>> from plugins.inputs import CSVReader
    >>> from core.engine import TransformationEngine
    >>> from plugins.outputs import ConsoleWriter
    >>> sink = ConsoleWriter()
    >>> config = {"continent": "Asia", "year": 2020, ...}
    >>> engine = TransformationEngine(sink, config)
    >>> reader = CSVReader("data/data.csv", engine)
    >>> reader.read()  # parses CSV and calls engine.execute(rows)
"""

import csv
import json
from typing import List, Any
from core.contracts import PipelineService


class CSVReader:
    """Read GDP data from a CSV file.

    Attributes:
        filepath: Path to the CSV file (e.g., "data/data.csv")
        service: PipelineService implementation (callback for processed data)

    Data Format:
        The CSV should have a header row with columns like:
        - Country Name: Name of the country
        - Country Code: 3-letter ISO code
        - Continent: Continental region
        - 2015, 2016, ..., 2020: Annual GDP values (year as column header)

    Example CSV Header:
        Country Name,Country Code,Continent,2015,2016,2017,2018,2019,2020
        China,CHN,Asia,10050000000000,10480000000000,...,14720000000000

    Example Usage:
        reader = CSVReader("data/data.csv", engine)
        reader.read()  # Loads CSV and calls engine.execute()
    """

    def __init__(self, filepath: str, service: PipelineService):
        """Initialize the CSV reader.

        Args:
            filepath: Path to CSV file.
            service: PipelineService to call with parsed rows.
        """
        self.filepath = filepath
        self.service = service

    def read(self) -> None:
        """Parse the CSV file and submit data to the service.

        The CSV is read line-by-line using csv.DictReader, which converts
        each row to a dict using the header row as keys. The list of dicts
        is passed to service.execute().

        Raises:
            FileNotFoundError: If filepath does not exist.
            csv.Error: If CSV parsing fails.
        """
        data = []
        with open(self.filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)

        self.service.execute(data)


class JSONReader:
    """Read GDP data from a JSON file.

    Attributes:
        filepath: Path to the JSON file (e.g., "data/data.json")
        service: PipelineService implementation (callback for parsed data)

    Data Format:
        The JSON should be an array of objects (rows), where each object
        has keys matching the CSV format (Country Name, Country Code, Continent, years):

        [
          {"Country Name": "China", "Country Code": "CHN", "Continent": "Asia", "2015": "10050000000000", ...},
          {"Country Name": "India", "Country Code": "IND", "Continent": "Asia", "2015": "2103590000000", ...},
          ...
        ]

    Example Usage:
        reader = JSONReader("data/data.json", engine)
        reader.read()  # Loads JSON array and calls engine.execute()
    """

    def __init__(self, filepath: str, service: PipelineService):
        """Initialize the JSON reader.

        Args:
            filepath: Path to JSON file.
            service: PipelineService to call with parsed array.
        """
        self.filepath = filepath
        self.service = service

    def read(self) -> None:
        """Parse the JSON file and submit data to the service.

        The JSON is expected to be a top-level array of objects. Each object
        represents a data row and is passed to service.execute().

        Raises:
            FileNotFoundError: If filepath does not exist.
            json.JSONDecodeError: If JSON is malformed.
        """
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.service.execute(data)
