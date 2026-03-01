# Adding Input Plugins

Learn how to extend the system with new data sources.

## Overview

Input plugins read data from various sources (CSV, JSON, databases, APIs, etc.) and feed it to the core engine. Because we use the `PipelineService` protocol, new inputs can be added without modifying any core code.

## Step-by-Step Guide

### Step 1: Create the Reader Class

In `plugins/inputs.py`, create a new class:

```python
class MyDataReader:
    \"\"\"Read GDP data from a custom source.\"\"\"
    
    def __init__(self, filepath: str, service: PipelineService):
        \"\"\"
        Args:
            filepath: Path/URL/connection string to data source
            service: PipelineService (typically TransformationEngine)
        \"\"\"
        self.filepath = filepath
        self.service = service
    
    def read(self) -> None:
        \"\"\"Parse data and call service.execute(data).\"\"\"
        # 1. Load/parse your data source
        data = self._load_data()
        
        # 2. Validate/normalize format
        data = self._normalize(data)
        
        # 3. Feed to engine
        self.service.execute(data)
    
    def _load_data(self):
        \"\"\"Load raw data from source.\"\"\"
        # Your custom loading logic
        pass
    
    def _normalize(self, raw):
        \"\"\"Ensure data has required keys.\"\"\"
        # Convert to list of dicts with keys:
        # - Country Name
        # - Country Code
        # - Continent
        # - Years (as string keys: \"2015\", \"2016\", etc.)
        return raw
```

### Step 2: The Data Contract

Your reader **must** feed the engine a list of dictionaries with these keys:

```python
[
    {
        \"Country Name\": \"China\",
        \"Country Code\": \"CHN\",
        \"Continent\": \"Asia\",
        \"2015\": \"10050000000000\",  # May be string or float
        \"2016\": \"10480000000000\",
        ...
        \"2020\": \"14720000000000\",
    },
    ...
]
```

This is the contract defined by `PipelineService.execute()`.

### Step 3: Register in main.py

Add your reader to the factory:

```python
from plugins.inputs import CSVReader, JSONReader, MyDataReader

INPUT_DRIVERS = {
    \"csv\": CSVReader,
    \"json\": JSONReader,
    \"my_format\": MyDataReader,  # Add this
}
```

### Step 4: Use in config.json

```json
{
  \"input\": {
    \"type\": \"my_format\",
    \"path\": \"/path/to/data.xyz\"
  },
  ...
}
```

### Step 5: Run

```bash
python main.py
```

---

## Example: SQLite Reader

Here's a real example that reads from a SQLite database:

```python
import sqlite3
from typing import List, Dict, Any
from core.contracts import PipelineService

class SQLiteReader:
    \"\"\"Read GDP data from a SQLite database.\"\"\"
    
    def __init__(self, db_path: str, service: PipelineService):
        self.db_path = db_path
        self.service = service
    
    def read(self) -> None:
        \"\"\"Query database and execute pipeline.\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Query all rows
        cursor.execute(\"SELECT * FROM gdp_data\")
        rows = cursor.fetchall()
        
        # Convert to list of dicts
        data = [self._row_to_dict(row) for row in rows]
        
        conn.close()
        
        # Feed to engine
        self.service.execute(data)
    
    def _row_to_dict(self, row):
        # Convert SQLite row to dict with required keys
        return {
            \"Country Name\": row[0],
            \"Country Code\": row[1],
            \"Continent\": row[2],
            \"2015\": str(row[3]),
            \"2016\": str(row[4]),
            ...
        }
```

**Register and use:**

```python
INPUT_DRIVERS[\"sqlite\"] = SQLiteReader
```

```json
{
  \"input\": {
    \"type\": \"sqlite\",
    \"path\": \"data/gdp.db\"
  }
}
```

---

## Example: REST API Reader

```python
import requests
from core.contracts import PipelineService

class APIReader:
    \"\"\"Read GDP data from a REST API.\"\"\"
    
    def __init__(self, api_url: str, service: PipelineService):
        self.api_url = api_url
        self.service = service
    
    def read(self) -> None:
        # Fetch data from API
        response = requests.get(self.api_url)
        data = response.json()  # Expects list of dicts
        
        # Feed to engine (assumes API returns correct format)
        self.service.execute(data)
```

---

## Design Principles

1. **No Core Dependencies**: Your reader should not import core engine/contracts (except the protocol hint)
2. **One Job**: Focus only on parsing and normalizing your data source
3. **Format Conversion**: Map your source's column names to the required keys
4. **Error Handling**: Raise exceptions for missing files, connection errors, etc.
5. **Documentation**: Add docstrings explaining the source format

---

## Testing Your Reader

```python
from plugins.inputs import MyDataReader
from plugins.outputs import ConsoleWriter
from core.engine import TransformationEngine

# Mock data reader
class TestReader:
    def __init__(self, filepath, service):
        self.filepath = filepath
        self.service = service
    
    def read(self):
        # Hardcoded test data
        data = [
            {
                \"Country Name\": \"Test Country\",
                \"Country Code\": \"TST\",
                \"Continent\": \"Asia\",
                \"2015\": \"100\",
                \"2016\": \"110\",
                ...
            }
        ]
        self.service.execute(data)

# Test it
sink = ConsoleWriter()
config = {\"continent\": \"Asia\", \"year\": 2020, ...}
engine = TransformationEngine(sink, config)
reader = TestReader(\"dummy.txt\", engine)
reader.read()  # Should work without errors
```

---

See also: [Adding Output Plugins](output_plugins.md)
