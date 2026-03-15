import json
from typing import Dict, Any

class ConfigLoader:
    """Provides utility methods to load configuration."""

    @staticmethod
    def load(filepath: str) -> Dict[str, Any]:
        """Loads and parses a JSON configuration file.
        
        Args:
            filepath (str): The path to the configuration file.
            
        Returns:
            Dict[str, Any]: The parsed configuration dictionary.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
