import json
import os

DEFAULTS = {
    "continent": None,
    "year": None,
    "operation": "average",
    "output": "dashboard",
    "data_path": "data.csv"
}


def load_config(path="config.json"):
    """Load and validate configuration from a JSON file.

    Returns a dict with keys: continent, year, operation, output, data_path
    """
    if not os.path.exists(path):
        print(f"Warning: config file not found at {path}. Using defaults.")
        return DEFAULTS.copy()

    try:
        with open(path, "r") as f:
            cfg = json.load(f)
    except Exception as e:
        print(f"Error reading config {path}: {e}. Using defaults.")
        return DEFAULTS.copy()

    # Normalize keys (accept both 'region' and 'continent')
    normalized = {k.lower(): v for k, v in cfg.items()}
    if "region" in normalized and "continent" not in normalized:
        normalized["continent"] = normalized.pop("region")

    # Merge with defaults without overwriting provided values
    merged = DEFAULTS.copy()
    for k, v in normalized.items():
        if k in merged and v is not None:
            merged[k] = v

    # Validate operation
    if merged["operation"] not in ("average", "sum"):
        print(f"Warning: invalid operation '{merged['operation']}' in config. Falling back to 'average'.")
        merged["operation"] = "average"

    # Year should be an int when provided
    y = merged.get("year")
    if y is not None:
        try:
            merged["year"] = int(y)
        except Exception:
            print(f"Warning: invalid year '{y}' in config. Ignoring year filter.")
            merged["year"] = None

    print(f"Loaded configuration from: {path}")
    return merged
