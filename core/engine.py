"""Core transformation engine: business logic for GDP analysis.

The TransformationEngine is the heart of the system:

- **Implements** PipelineService: accepts raw data via execute()
- **Depends on** DataSink: injects a writer to persist results
- **Computes** all analytics: rankings, trends, growth rates, aggregations

Design principles:
    - Constructor injection: sink and config are passed in, never hardcoded
    - Pure transformations: no I/O side effects except final sink.write()
    - Validation: filters invalid/aggregate countries before analysis
    - Configurable: changes in config.json automatically affect output

Building a new analytic is simple: add a method like _my_metric(),
call it in _process(), and return it in the result dict.

Examples:
    >>> from core.engine import TransformationEngine
    >>> from plugins.outputs import ConsoleWriter
    >>> config = {"continent": "Asia", "year": 2020, "start_year": 2015, "end_year": 2020}
    >>> sink = ConsoleWriter()
    >>> engine = TransformationEngine(sink, config)
    >>> engine.execute(raw_data)  # processes data and outputs result
"""
from typing import List, Dict, Any
from core.contracts import DataSink, PipelineService


class TransformationEngine(PipelineService):
    """Main orchestrator for GDP data transformation and analysis.

    This class implements the PipelineService protocol, meaning external input
    plugins can call its execute() method to submit raw data. The engine then
    transforms the data according to config and writes results to an
    injected DataSink.

    Attributes:
        sink (DataSink): The output destination (injected at construction).
        config (Dict): Parameters controlling the analysis (continent, year range).

    Constructor Injection:
        Both sink and config are required at construction and cannot be changed.
        This makes the dependency graph clear and testable.

    Public Methods:
        - execute(raw_data): Processes raw data and outputs result via sink.

    Analytics:
        - _top_10, _bottom_10: Rankings by GDP for given year
        - _growth_rate: % change per country over date range
        - _average_by_continent: Mean GDP per continent
        - _global_trend: Year-by-year aggregate GDP
        - _fastest_growing_continent: Highest growth by absolute change
        - _consistent_decline: Countries with declining GDP every year
        - _global_contribution: Each continent\'s % of global GDP

    Validation:
        - _is_valid_country(): Filters aggregates; requires 3-letter ISO code
    """

    def __init__(self, sink: DataSink, config: Dict[str, Any]):
        """Initialize the engine with output sink and analysis parameters.

        Args:
            sink: DataSink implementation (ConsoleWriter, JSONWriter, etc.).
                  Engine calls sink.write(results) after processing.
            config: Dict with keys:
                - continent: str (e.g., "Asia")
                - year: int (reference year for rankings)
                - start_year: int (first year in trend)
                - end_year: int (last year in trend)

        Raises:
            ValueError: If required config keys are missing.
        """
        self.sink = sink
        self.config = config
        self._validate_config()

    # -------------------------
    # Public API
    # -------------------------

    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        result = self._process(raw_data)
        self.sink.write(result)

    # -------------------------
    # Validation & Utilities
    # -------------------------

    def _validate_config(self):
        required_keys = {"continent", "year", "start_year", "end_year"}
        missing = required_keys - self.config.keys()
        if missing:
            raise ValueError(f"Missing config keys: {missing}")

    def _safe_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _is_valid_country(self, record: Dict[str, Any]) -> bool:
        name = record.get("Country Name", "")
        code = record.get("Country Code", "")
    
        # Exclude aggregates by checking if Continent is valid
        if record.get("Continent") in ["Global", None, ""]:
            return False

        # Exclude known aggregated names (World Bank aggregates often have no ISO region classification)
        if "World" in name or "income" in name:
            return False

        # Must have 3-letter ISO code
        return len(code) == 3

    # -------------------------
    # Master Processing
    # -------------------------

    def _process(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:

        continent = self.config.get("continent")
        year = str(self.config.get("year"))
        start_year = str(self.config.get("start_year"))
        end_year = str(self.config.get("end_year"))

        return {
            "top_10": self._top_10(data, continent, year),
            "bottom_10": self._bottom_10(data, continent, year),
            "growth_rate": self._growth_rate(data, continent, start_year, end_year),
            "average_by_continent": self._average_by_continent(data, end_year),
            "global_trend": self._global_trend(data, start_year, end_year),
            "fastest_growing_continent": self._fastest_growing_continent(data, start_year, end_year),
            "consistent_decline": self._consistent_decline(data, start_year, end_year),
            "global_contribution": self._global_contribution(data, end_year)
        }

    # -------------------------
    # Analytics Methods
    # -------------------------

    def _top_10(self, data, continent, year):

        filtered = [
            {
                "Country": x["Country Name"],
                "GDP": self._safe_float(x.get(year))
            }
            for x in data
            if x.get("Continent") == continent
            and x.get(year)
            and self._is_valid_country(x)
        ]

        sorted_data = sorted(filtered, key=lambda x: x["GDP"], reverse=True)

        return sorted_data[:10]

    def _bottom_10(self, data, continent, year):

        filtered = [
            {
                "Country": x["Country Name"],
                "GDP": self._safe_float(x.get(year))
            }
            for x in data
            if x.get("Continent") == continent
            and x.get(year)
            and self._is_valid_country(x)
        ]

        sorted_data = sorted(filtered, key=lambda x: x["GDP"])

        return sorted_data[:10]

    def _growth_rate(self, data, continent, start_year, end_year):

        result = []

        for x in data:
            if (
                x.get("Continent") == continent
                and x.get(start_year)
                and x.get(end_year)
                and self._is_valid_country(x)
            ):
                start = self._safe_float(x[start_year])
                end = self._safe_float(x[end_year])

                if start != 0:
                    growth = ((end - start) / start) * 100
                else:
                    growth = 0

                result.append({
                    "Country": x["Country Name"],
                    "GrowthRate(%)": growth
                })

        return result

    def _average_by_continent(self, data, end_year):

        continents = {
            x["Continent"]
            for x in data
            if x.get("Continent") != "Global"
        }

        result = {}

        for continent in continents:
            values = [
                self._safe_float(x.get(end_year))
                for x in data
                if x.get("Continent") == continent
                and x.get(end_year)
                and self._is_valid_country(x)
            ]

            result[continent] = sum(values) / len(values) if values else 0

        return result

    def _global_trend(self, data, start_year, end_year):

        years = range(int(start_year), int(end_year) + 1)

        return {
            str(year): sum(
                self._safe_float(x.get(str(year)))
                for x in data
                if self._is_valid_country(x)
            )
            for year in years
        }

    def _fastest_growing_continent(self, data, start_year, end_year):

        continents = {
            x["Continent"]
            for x in data
            if x.get("Continent") != "Global"
        }

        growth_rates = {}

        for continent in continents:

            start_total = sum(
                self._safe_float(x.get(start_year))
                for x in data
                if x.get("Continent") == continent
                and self._is_valid_country(x)
            )

            end_total = sum(
                self._safe_float(x.get(end_year))
                for x in data
                if x.get("Continent") == continent
                and self._is_valid_country(x)
            )

            growth_rates[continent] = end_total - start_total

        return max(growth_rates, key=growth_rates.get) if growth_rates else None

    def _consistent_decline(self, data, start_year, end_year):

        years = list(range(int(start_year), int(end_year) + 1))

        declining_countries = []

        for record in data:
            if not self._is_valid_country(record):
                continue

            values = [
                self._safe_float(record.get(str(y)))
                for y in years
                if record.get(str(y))
            ]

            if len(values) > 1 and all(values[i] > values[i + 1] for i in range(len(values) - 1)):
                declining_countries.append(record["Country Name"])

        return declining_countries

    def _global_contribution(self, data, end_year):

        continents = {
            x["Continent"]
            for x in data
            if x.get("Continent") != "Global"
        }

        total_global = sum(
            self._safe_float(x.get(end_year))
            for x in data
            if self._is_valid_country(x)
        )

        contribution = {}

        for continent in continents:

            continent_total = sum(
                self._safe_float(x.get(end_year))
                for x in data
                if x.get("Continent") == continent
                and self._is_valid_country(x)
            )

            contribution[continent] = (
                (continent_total / total_global) * 100
                if total_global != 0 else 0
            )

        return contribution