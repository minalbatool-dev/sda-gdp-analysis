# core/engine.py

from typing import List, Dict, Any
from core.contracts import DataSink, PipelineService


class TransformationEngine(PipelineService):

    def __init__(self, sink: DataSink, config: Dict[str, Any]):
        self.sink = sink
        self.config = config
        self._validate_config()

    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        result = self._process(raw_data)
        self.sink.write(result)

    # -------------------------
    # Utility Helpers
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
        filtered = list(filter(
            lambda x: x.get("Continent") == continent and x.get(year),
            data
        ))

        sorted_data = sorted(
            filtered,
            key=lambda x: self._safe_float(x.get(year)),
            reverse=True
        )

        return sorted_data[:10]

    def _bottom_10(self, data, continent, year):
        filtered = list(filter(
            lambda x: x.get("Continent") == continent and x.get(year),
            data
        ))

        sorted_data = sorted(
            filtered,
            key=lambda x: self._safe_float(x.get(year))
        )

        return sorted_data[:10]

    def _growth_rate(self, data, continent, start_year, end_year):
        filtered = list(filter(
            lambda x: x.get("Continent") == continent
            and x.get(start_year) and x.get(end_year),
            data
        ))

        return list(map(
            lambda x: {
                "Country": x["Country Name"],
                "GrowthRate": (
                    ((self._safe_float(x[end_year]) - self._safe_float(x[start_year]))
                     / self._safe_float(x[start_year])) * 100
                    if self._safe_float(x[start_year]) != 0 else 0
                )
            },
            filtered
        ))

    def _average_by_continent(self, data, end_year):
        continents = set(map(lambda x: x["Continent"], data))

        result = {}

        for continent in continents:
            filtered = list(filter(
                lambda x: x["Continent"] == continent and x.get(end_year),
                data
            ))

            values = list(map(lambda x: self._safe_float(x[end_year]), filtered))

            result[continent] = (
                sum(values) / len(values) if values else 0
            )

        return result

    def _global_trend(self, data, start_year, end_year):
        years = range(int(start_year), int(end_year) + 1)

        return {
            str(year): sum(
                map(
                    lambda x: self._safe_float(x.get(str(year))),
                    data
                )
            )
            for year in years
        }

    def _fastest_growing_continent(self, data, start_year, end_year):
        continents = set(map(lambda x: x["Continent"], data))

        growth_rates = {
            continent:
            (
                sum(map(
                    lambda x: self._safe_float(x.get(end_year)),
                    filter(lambda x: x["Continent"] == continent, data)
                ))
                -
                sum(map(
                    lambda x: self._safe_float(x.get(start_year)),
                    filter(lambda x: x["Continent"] == continent, data)
                ))
            )
            for continent in continents
        }

        return max(growth_rates, key=growth_rates.get)

    def _consistent_decline(self, data, start_year, end_year):
        years = list(range(int(start_year), int(end_year) + 1))

        def declining(record):
            values = [
                self._safe_float(record.get(str(y)))
                for y in years if record.get(str(y))
            ]
            return all(values[i] > values[i + 1] for i in range(len(values) - 1))

        return list(map(
            lambda x: x["Country Name"],
            filter(declining, data)
        ))

    def _global_contribution(self, data, end_year):

        continents = set(map(lambda x: x["Continent"], data))

        total_global = sum(
            map(lambda x: self._safe_float(x.get(end_year)), data)
        )

        contribution = {
            continent:
            (
                sum(
                    map(
                        lambda x: self._safe_float(x.get(end_year)),
                        filter(lambda x: x["Continent"] == continent, data)
                    )
                ) / total_global * 100
                if total_global != 0 else 0
            )
            for continent in continents
        }

        return contribution

    