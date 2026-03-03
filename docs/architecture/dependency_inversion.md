# Dependency Inversion Principle (DIP)

## What is DIP?

The **Dependency Inversion Principle** states:

> 1. High-level modules should not depend on low-level modules.  
> Both should depend on abstractions.
>
> 2. Abstractions should not depend on details.  
> Details should depend on abstractions.

In plain terms: **The important code (core logic) should not be aware of supporting code (I/O, configuration, etc.).**

## Bad Design (Without DIP)

Here's an anti-pattern to avoid:

```python
# ❌ BAD: engine imports concrete writers

from plugins.outputs import ConsoleWriter, JSONWriter

class TransformationEngine:
    def __init__(self):
        # Hardcoded dependency – violates DIP
        if some_condition:
            self.writer = ConsoleWriter()
        else:
            self.writer = JSONWriter()
    
    def execute(self, data):
        result = self._process(data)
        # Tightly coupled to concrete writers
        self.writer.write(result)
```

**Problems:**
- Engine knows about `ConsoleWriter`, `JSONWriter`, etc.
- To add a new writer, you must modify engine code
- Testing requires actual files/console
- Inputs must know about the engine's structure

## Good Design (With DIP)

```python
# ✓ GOOD: engine depends on protocol

from core.contracts import DataSink, PipelineService

class TransformationEngine(PipelineService):
    def __init__(self, sink: DataSink, config):
        # Accepts any DataSink implementation
        self.sink = sink
        self.config = config
    
    def execute(self, raw_data):
        result = self._process(raw_data)
        # Calls protocol method (duck typing)
        self.sink.write(result)
```

**Benefits:**
- Engine depends only on `DataSink` protocol
- New writers can be added without touching engine
- Testing is trivial (mock sink)
- Inputs are completely decoupled from engine

## Our Implementation

### Principal 1: High-Level Independent of Low-Level

```
HIGH-LEVEL (Core)
    ↑
    | depends on
    ↓
ABSTRACTIONS (Protocols)
    ↑
    | implemented by
    ↓
LOW-LEVEL (Plugins)
```

### Principal 2: Abstractions Don't Depend on Details

The `core/contracts.py` protocols are **pure abstractions**:

```python
# No imports of plugins – protocols are self-contained
from typing import Protocol, Dict, List, Any

class DataSink(Protocol):
    def write(self, data: Dict[str, Any]) -> None: ...
```

Writers satisfy the protocol structurally, not through inheritance.

## The Direction of Dependencies

```
plugins/inputs.py ──→ core/contracts.py
plugins/outputs.py ──→ core/contracts.py
plugins/inputs.py ──→ core/engine.py
plugins/outputs.py ──→ core/engine.py
                      
main.py ──→ (everything)

BUT NEVER:
core ──→ plugins (WRONG!)
core ──→ main (mostly WRONG!)
```

**Rule:** Dependencies should point **toward** the core, never away.

## The Three Golden Rules (From Assignment)

### 1. Inbound Abstraction

> The Input Module must not depend on a concrete Core class. It interacts with a Protocol (PipelineService) residing in the Core.

**Implementation:**

```python
# plugins/inputs.py
class CSVReader:
    def __init__(self, filepath: str, service: PipelineService):
        # ✓ Accepts PipelineService protocol, not concrete engine
        self.service = service
    
    def read(self):
        # ✓ Calls execute() – only method it needs to know
        self.service.execute(data)
```

### 2. Outbound Abstraction  

> The Core must not import specific writers. It calls methods on a Protocol (DataSink) that is injected into it at runtime.

**Implementation:**

```python
# core/engine.py
from core.contracts import DataSink  # ✓ Import protocol only

class TransformationEngine(PipelineService):
    def __init__(self, sink: DataSink, config):
        self.sink = sink  # ✓ Accept any DataSink
    
    def execute(self, raw_data):
        result = self._process(raw_data)
        # ✓ Call protocol method – engine never imports ConsoleWriter, JSONWriter, etc.
        self.sink.write(result)
```

### 3. Ownership of Contracts

> The Core is the authority. It defines the contracts that other modules must satisfy to be "plugged in."

**Implementation:**

```
core/contracts.py owns DataSink and PipelineService protocols
↓
plugins/inputs.py must call PipelineService.execute()
↓
plugins/outputs.py must implement DataSink.write()
```

The core dictates the rules; plugins conform.

## Benefits in Practice

### Before (Tightly Coupled)

```python
# ❌ To add a database writer:
# 1. Modify core/engine.py to import DatabaseWriter
# 2. Add conditional logic in __init__
# 3. Test by running against actual database
# 4. Risk: might break existing code
```

### After (Loosely Coupled)

```python
# ✓ To add a database writer:
# 1. Create plugins/outputs.py::DatabaseWriter
# 2. Implement write(self, data) method
# 3. Register in main.py::OUTPUT_DRIVERS
# 4. Use in config.json
# No core code changes needed!
```

### Testing

**Without DIP:**
```python
# ❌ Engine test must use real files
engine = TransformationEngine()  # Creates ConsoleWriter or JSONWriter
engine.execute(data)  # Actually prints or writes to disk
```

**With DIP:**
```python
# ✓ Engine test uses mock sink
class MockSink:
    def write(self, data):
        self.data = data  # Capture for inspection

sink = MockSink()
engine = TransformationEngine(sink, config)
engine.execute(data)
assert sink.data == expected_result  # Easy!
```

## Conclusion

Dependency Inversion is about **direction of control and coupling**:

- Core tells plugins what to do (contracts)
- Plugins conform to core's interface
- Dependencies point inward
- System remains flexible and testable

Our implementation achieves this using Python's `typing.Protocol` for structural interfaces, no inheritance needed.

---

For more: See [Core Contracts](contracts.md) and [Architecture Overview](overview.md)
