"""Core protocol contracts for Dependency Inversion.

This module defines the two structural interfaces (Protocols) that enable
complete decoupling of the system:

- **DataSink**: Where the engine sends results (ConsoleWriter, FileWriter, etc.)
- **PipelineService**: How external inputs feed data to the engine

Using typing.Protocol enables *duck typing* in Python: any class with the
matching method signatures automatically satisfies the interface, no inheritance
or explicit registration needed.

Architecture:
    - plugins.inputs implements PipelineService (calls execute)
    - core.engine implements PipelineService and depends on DataSink
    - plugins.outputs implements DataSink
    - Dependencies point toward core (Dependency Inversion Principle)

Examples:
    See the README and architecture diagram for a visual overview.
    See core/engine.py for an example of injecting DataSink.
"""

from typing import Protocol, List, Dict, Any, runtime_checkable


@runtime_checkable
class DataSink(Protocol):
    """Outbound abstraction: where the core sends processed results.

    The TransformationEngine does not depend on any concrete writer class.
    Instead, it accepts a DataSink and calls its write method to persist
    or display the analysis results. This ensures the core is agnostic of
    file formats, databases, UI layers, or export targets.

    Any output implementation that defines a write(data) method with the
    correct signature will work.

    Implementations:
        - plugins.outputs.ConsoleWriter: writes pretty-printed dict to stdout
        - plugins.outputs.JSONWriter: writes dict to JSON file
        - plugins.outputs.CSVWriter: writes dict rows to CSV file

    Custom implementations can be added by creating a class with a write method
    and registering it in main.OUTPUT_DRIVERS.
    """

    def write(self, data: Dict[str, Any]) -> None:
        """Persist or display the analysis results.

        Args:
            data: Dictionary with keys:
                - top_10: Top 10 countries by GDP for given continent/year
                - bottom_10: Bottom 10 countries by GDP
                - growth_rate: % change in GDP over date range per country
                - average_by_continent: Mean GDP per continent for end year
                - global_trend: Year-by-year global GDP totals
                - fastest_growing_continent: Which continent grew most (by delta)
                - consistent_decline: Countries whose GDP declined every year
                - global_contribution: Each continent's % of global GDP
        """
        ...


class PipelineService(Protocol):
    """Inbound abstraction: how input sources feed data to the core.

    External input plugins (CSV, JSON, database readers, APIs, etc.) do not
    import any core transformation logic. Instead, they accept a PipelineService
    in their constructor and call its execute method to submit raw data.

    This ensures inputs remain decoupled from the engine. You can add a new
    data source by implementing this protocol.

    Implementations:
        - plugins.inputs.CSVReader: reads CSV file, calls execute()
        - plugins.inputs.JSONReader: reads JSON file, calls execute()

    Custom implementations can be added by creating a class that accepts
    (filepath, service: PipelineService) and calls service.execute(data).
    """

    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        """Receive and process raw data from an input source.

        Args:
            raw_data: List of dictionaries representing rows of data.
                Expected keys (for GDP dataset):
                - Country Name: e.g. "China", "India"
                - Country Code: 3-letter ISO code (e.g. "CHN")
                - Continent: e.g. "Asia", "Europe"
                - Year columns as string keys: "2015", "2016", ..., "2020"

        Behavior:
            The implementation (typically TransformationEngine) will:
            1. Validate and filter raw_data based on config
            2. Compute all eight analytics metrics
            3. Call sink.write(results) to persist output
        """
        ...
