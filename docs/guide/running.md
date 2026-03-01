# Running the Pipeline

Detailed instructions for executing the GDP analysis.

## Prerequisite

Ensure `config.json` is properly configured (see [Configuration Guide](configuration.md)).

## Running Locally

### Method 1: Direct Execution

```bash
python main.py
```

Output appears immediately on console (if output type is `console`) or is written to file.

### Method 2: With Python Module

```bash
python -m main
```

Equivalent to the above.

## Output

### Console Output

Results are printed line-by-line:

```
===== GDP ANALYSIS RESULTS =====

--- TOP_10 ---
[...]

--- BOTTOM_10 ---
[...]

--- GROWTH_RATE ---
[...]

...
```

### File Output

Results are written to disk:

```bash
# Check if file was created
ls -la out/results.json

# View results
cat out/results.json
```

## Monitoring

### Check Execution Time

```bash
time python main.py
```

Typical runtime: 1-2 seconds.

### Validate Output Integrity

```python
import json
with open('out/results.json') as f:
    data = json.load(f)
    print(f"Keys: {data.keys()}")
    print(f"Top 10 count: {len(data['top_10'])}")
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError` | Input file missing | Check `config.json` path |
| `ValueError: Missing config keys` | Incomplete config | Verify all required keys present |
| `jsonDecodeError` | Malformed JSON input | Regenerate data.json from CSV |

### Debug Mode

Add logging to trace execution:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Tips

- **CSV faster than JSON**: CSV parsing is ~10% quicker
- **Console faster than file**: Console output is negligible; file I/O dominates
- **Subset data**: Filter to single continent to reduce processing

---

See also: [Configuration Guide](configuration.md)
