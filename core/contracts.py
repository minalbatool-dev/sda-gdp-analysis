# core/contracts.py

from typing import Protocol, List, Dict, Any, runtime_checkable


@runtime_checkable
class DataSink(Protocol):
    """
    Output abstraction.
    Core will send processed results to this.
    """
    def write(self, data: Dict[str, Any]) -> None:
        ...


class PipelineService(Protocol):
    """
    Input abstraction.
    Input plugins will call this.
    """
    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        ...