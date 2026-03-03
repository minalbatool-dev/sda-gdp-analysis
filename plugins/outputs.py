"""Output plugins: result persistence implementations.

This module provides writer classes that persist analysis results to various
destinations (console, files, etc.). Each writer implements the DataSink protocol,
allowing the core engine to remain agnostic of presentation and export details.

Design:
    - No writer imports core business logic
    - Each writer only implements DataSink protocol
    - Core engine calls sink.write() with no knowledge of the implementation
    - Easy to add new outputs (databases, APIs, charts, etc.) without modifying core

Usage:
    >>> from plugins.outputs import JSONWriter
    >>> from core.engine import TransformationEngine
    >>> sink = JSONWriter(path="output.json")
    >>> config = {"continent": "Asia", "year": 2020, ...}
    >>> engine = TransformationEngine(sink, config)
    >>> engine.execute(raw_data)  # write occurs automatically
"""

import json
import csv
from typing import Any, Dict


class ConsoleWriter:
    """Write analysis results to stdout (console output).

    This is the simplest output implementation. Results are pretty-printed
    to the terminal for immediate inspection.

    Useful for:
        - Development and debugging
        - Interactive use
        - Quick verification of results

    Example Output:
        ===== GDP ANALYSIS RESULTS =====

        --- TOP_10 ---
        [{'Country': 'China', 'GDP': 14996414166715.1}, ...]

        --- BOTTOM_10 ---
        [{'Country': 'Timor-Leste', 'GDP': 2162619240.87}, ...]
    """

    def __init__(self, **kwargs: Any):
        """Initialize the console writer.

        Args:
            **kwargs: Ignored; accepts arbitrary kwargs for factory compatibility.
        """
        pass

    def write(self, data: Dict[str, Any]) -> None:
        """Print analysis results to stdout.

        Args:
            data: Dictionary containing analysis results with keys:
                - top_10, bottom_10, growth_rate, average_by_continent,
                  global_trend, etc.
        """
        print("\n===== GDP ANALYSIS RESULTS =====\n")
        for section, content in data.items():
            print(f"\n--- {section.upper()} ---")
            print(content)


class JSONWriter:
    """Write analysis results to a JSON file.

    Results are serialized to JSON format with formatting for human readability.
    Files are written with 2-space indentation.

    Useful for:
        - Integration with downstream tools
        - Long-term archival
        - Web API responses
        - Data pipelines that consume JSON

    Attributes:
        path: Output file path (e.g., "output.json" or "out/results.json")

    Example Usage:
        writer = JSONWriter(path="results.json")
        engine = TransformationEngine(writer, config)
        engine.execute(data)  # results written to results.json
    """

    def __init__(self, path: str = "output.json", **kwargs: Any):
        """Initialize the JSON writer.

        Args:
            path: Output file path. Default is "output.json".
            **kwargs: Ignored; accepts arbitrary kwargs for factory compatibility.

        Note:
            The parent directory must exist; FileNotFoundError is raised otherwise.
        """
        self.path = path

    def write(self, data: Dict[str, Any]) -> None:
        """Serialize and write analysis results to a JSON file.

        Args:
            data: Dictionary containing analysis results.

        Raises:
            FileNotFoundError: If parent directory does not exist.
            IOError: If file cannot be written.
        """
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Results written to {self.path}")


class CSVWriter:
    """Write analysis results to a CSV file.

    This is a simple implementation that writes two columns:
    - section: Name of the analysis section
    - payload: The stringified result

    Useful for:
        - Spreadsheet tools (Excel, Google Sheets)
        - Simple tabular export
        - Quick data interchange

    Attributes:
        path: Output file path (e.g., "output.csv" or "out/results.csv")

    Example CSV Output:
        section,payload
        top_10,"[{'Country': 'China', 'GDP': 14996414166715.1}, ...]"
        bottom_10,"[{'Country': 'Timor-Leste', 'GDP': 2162619240.87}, ...]"

    Example Usage:
        writer = CSVWriter(path="results.csv")
        engine = TransformationEngine(writer, config)
        engine.execute(data)  # results written to results.csv
    """

    def __init__(self, path: str = "output.csv", **kwargs: Any):
        """Initialize the CSV writer.

        Args:
            path: Output file path. Default is "output.csv".
            **kwargs: Ignored; accepts arbitrary kwargs for factory compatibility.

        Note:
            The parent directory must exist; FileNotFoundError is raised otherwise.
        """
        self.path = path

    def write(self, data: Dict[str, Any]) -> None:
        """Serialize and write analysis results to a CSV file.

        Each row has two columns: section name and stringified payload.

        Args:
            data: Dictionary containing analysis results.

        Raises:
            FileNotFoundError: If parent directory does not exist.
            IOError: If file cannot be written.
        """
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["section", "payload"])
            for section, content in data.items():
                writer.writerow([section, content])
        print(f"Results written to {self.path}")
