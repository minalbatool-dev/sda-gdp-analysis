class Dashboard:
    """Observer: Subscribes to telemetry updates and generates colored capacity warnings."""

    def __init__(self, max_queue_size: int, config: dict = None):
        self.max_queue_size = max_queue_size
        self.config = config or {}

        # ANSI Escape Codes for Colors
        self.GREEN = "\033[92m"
        self.YELLOW = "\033[93m"
        self.RED = "\033[91m"
        self.RESET = "\033[0m"

    def update(self, raw_size: int, worker_size: int, processed_size: int):
        """Receives updates from the PipelineTelemetry subject subject."""
        
        telemetry_cfg = self.config.get("visualizations", {}).get("telemetry", {})
        show_raw = telemetry_cfg.get("show_raw_stream", True)
        show_int = telemetry_cfg.get("show_intermediate_stream", True)
        show_proc = telemetry_cfg.get("show_processed_stream", True)

        def get_color(size):
            percentage = size / self.max_queue_size if self.max_queue_size else 0
            if percentage < 0.5:
                return self.GREEN
            elif percentage < 0.8:
                return self.YELLOW
            else:
                return self.RED
                
        def build_bar(size, color):
            fill = int((size / self.max_queue_size) * 20) if self.max_queue_size else 0
            bar = "=" * fill + "-" * (20 - fill)
            return f"{color}[{bar}] {size}/{self.max_queue_size}{self.RESET}"

        parts = []
        if show_raw:
            parts.append(f"Raw: {build_bar(raw_size, get_color(raw_size))}")
        if show_int:
            parts.append(f"Intermediate: {build_bar(worker_size, get_color(worker_size))}")
        if show_proc:
            parts.append(f"Processed: {build_bar(processed_size, get_color(processed_size))}")
        
        print(f"\rTELEMETRY | {' | '.join(parts)}{' ' * 10}", end="")
