from typing import Dict, Any

class LiveCharts:
    """Simulates real-time charting by printing formatted streams."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def render(self, item: Dict[str, Any]):
        """Renders the data points requested by the configuration."""
        entity = item.get("entity_name", "Unknown")
        time_period = item.get("time_period", "Unknown")
        val = item.get("metric_value", 0.0)
        avg = item.get("computed_metric", 0.0)
        
        # ANSI formatting for visual distinction in console
        BLUE = "\033[94m"
        RESET = "\033[0m"
        
        # We start with a newline if dashboard is using \r
        print(f"\n{BLUE}[CHART - {entity} {time_period}] "
              f"Value: {val:6.2f} | Running Avg: {avg:6.2f}{RESET}")
