# FAQ

## General

### Q: What is this project?

**A:** A modular, production-ready GDP analysis system that processes World Bank data and produces eight key analytics (rankings, trends, growth rates, etc.).

### Q: Why is it called "Phase 2"?

**A:** Phase 1 was a monolithic script. Phase 2 refactored it using proper software architecture (Dependency Inversion, Protocols, modular design).

### Q: Who should use this?

**A:** Data analysts, economists, software engineers learning SOLID principles, or anyone needing extensible GDP analytics.

---

## Architecture

### Q: What's Dependency Inversion?

**A:** A design principle that makes high-level code (business logic) independent of low-level code (I/O, config). Our core engine doesn't care if you read from CSV or JSON, or write to console or file.

### Q: Why use Protocols instead of inheritance?

**A:** Protocols enable **duck typing** – any class with matching methods automatically satisfies the interface. This prevents tight coupling and makes testing easier.

### Q: Can I add a new input format without modifying core code?

**A:** Yes! Create a reader class in `plugins/inputs.py`, register it in `main.py`, and use it in `config.json`. Done.

### Q: Can I add a new output format without modifying core code?

**A:** Yes! Create a writer class in `plugins/outputs.py`, register it in `main.py`, and use it in `config.json`. Done.

---

## Configuration

### Q: What does config.json do?

**A:** Drives the entire pipeline. Specifies input source, output destination, and analysis parameters (continent, years, etc.).

### Q: Can I run the pipeline without modifying code?

**A:** Yes! Edit `config.json` to change input/output and parameters. No code changes needed.

### Q: What if I run the pipeline with invalid configuration?

**A:** The `TransformationEngine` validates required keys and raises `ValueError` with a helpful message.

---

## Usage

### Q: How do I run the analysis?

**A:** 
1. Edit `config.json` with your desired settings
2. Run `python main.py`
3. Results are displayed (console) or written to file

### Q: How long does it take?

**A:** ~1 second for a typical analysis (266 countries, 8 metrics).

### Q: What if the output directory doesn't exist?

**A:** Create it first: `mkdir out`

### Q: Can I use both CSV and JSON at the same time?

**A:** Only one at a time in `config.json`. But you can run the pipeline multiple times with different configs.

---

## Data

### Q: What's the data source?

**A:** World Bank GDP data (CSV format, 266 countries, 2015-2020).

### Q: Can I use other GDP data?

**A:** Yes! As long as it has the same columns (Country Name, Country Code, Continent, years).

### Q: Is the JSON version auto-generated?

**A:** On first run, if JSON input is configured but the file doesn't exist, it's created from the CSV.

### Q: Why is there both CSV and JSON?

**A:** To demonstrate that the same engine works with different input formats.

---

## Analytics

### Q: What analytics are provided?

**A:** 
1. Top 10 countries by GDP (given continent/year)
2. Bottom 10 countries by GDP
3. GDP growth rate per country (over date range)
4. Average GDP per continent
5. Global GDP trend (year-by-year)
6. Fastest growing continent (by absolute change)
7. Countries with consistent decline (every year)
8. Each continent's share of global GDP

### Q: Can I add a new metric?

**A:** Yes! Add a method like `_my_metric()` to `TransformationEngine`, call it in `_process()`, and return it in the result dict.

### Q: How does the engine filter invalid data?

**A:** The `_is_valid_country()` method excludes:
- Rows without a 3-letter ISO country code
- World Bank aggregates (e.g., "East Asia & Pacific")

---

## Documentation

### Q: How do I view the API docs?

**A:** 
1. Install mkdocs: `pip install mkdocs mkdocs-material`
2. Build site: `mkdocs build`
3. Serve locally: `mkdocs serve`
4. Visit `http://localhost:8000` in your browser

### Q: Where are the docstrings?

**A:** In each Python file (contracts.py, engine.py, inputs.py, outputs.py, main.py).

### Q: How complete is the documentation?

**A:** Very! Module-level docs, class docs, method docs, usage examples, and a full mkdocs site with guides.

---

## Troubleshooting

### Q: I get "ModuleNotFoundError: No module named 'core'"

**A:** Make sure you're running from the project root: `cd d:\Pictures\FAST NUCES\4 Semester\SDA\Project\Phase 2`

### Q: I get "FileNotFoundError" when running

**A:** Check that `config.json` paths are correct and files exist:
- For CSV input: `data/data.csv` must exist
- For JSON input: `data/data.json` must exist
- For file output: parent directory must exist

### Q: Results look wrong or empty

**A:** Check `parameters.continent` matches actual data. Try "Asia" or "Europe" if unsure.

### Q: Can I run tests?

**A:** Not yet, but the code is designed to be testable. pytest tests would be a great addition!

---

## Contributing

### Q: How do I add a feature?

**A:** 
1. Create a branch: `git checkout -b feature/my-feature`
2. Modify code (follow existing patterns)
3. Test thoroughly
4. Commit with clear message: `git commit -m "feat: add my feature"`

### Q: What patterns should I follow?

**A:** 
- Use type hints (PEP 484)
- Write docstrings for all public methods
- No imports from plugins in core
- All new outputs must implement DataSink protocol
- All new inputs must call PipelineService.execute()

---

## Performance

### Q: Is there a memory limit?

**A:** For 266 countries × 6 years of data, memory usage is <50 MB.

### Q: Can I optimize for large datasets?

**A:** Possible approaches:
- Stream data line-by-line (modify `TransformationEngine`)
- Cache intermediate results
- Parallelize continent calculations

---

Still have questions? Check [Architecture Overview](architecture/overview.md) or [Quick Start](guide/quickstart.md).
