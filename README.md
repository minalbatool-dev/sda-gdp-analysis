# SDA GDP Analysis Project

## Features
- GDP data loading and cleaning
- Configuration-based filtering
- Statistical analysis (average / sum)
- Dashboard-based visualizations

  ## Technologies
  - Python
  - JSON
  - GitHub

## Quick Start

1. Create a virtual environment and install dependencies (only pandas and matplotlib required):

```bash
python -m venv .venv
.
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install pandas matplotlib
```

2. Configure analysis in `config.json` (fields: `continent`, `year`, `operation`, `output`, `data_path`). Example:

```json
{
  "continent": "South Asia",
  "year": 2020,
  "operation": "average",
  "output": "dashboard",
  "data_path": "data.csv"
}
```

3. Run the dashboard:

```bash
# From project root
python dashboard.py
```

The dashboard will read `config.json`, load and normalize `data.csv`, print computed statistics, and open charts. If a filter yields no rows, a message is shown and charts are skipped.

## Example git workflow & commit messages

This project should be developed incrementally in a team. Example commits that show good incremental work:

- `feat: add config_loader to support config.json and validation`
- `feat: normalize data processor to support wide/long CSV formats`
- `feat: add region & year visualization wrappers (bar, pie, histogram)`
- `fix: handle empty filter result without KeyError`
- `chore: update README with run instructions and example commits`

When pairing, create a branch per feature and push frequently. Include small, focused commits so reviewers can follow progress.

## Next steps (suggested)
- Add automated tests for `data_processor.normalize_data` and `compute_statistics`.
- Add CLI flags to override `config.json` at runtime.
- Save generated charts to `outputs/` when running in non-interactive environments.
