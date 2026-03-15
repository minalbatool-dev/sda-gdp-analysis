class Dashboard:
    """Observer: Subscribes to telemetry updates and generates colored capacity warnings."""

    def __init__(self, max_queue_size: int):
        self.max_queue_size = max_queue_size

        # ANSI Escape Codes for Colors
        self.GREEN = "\033[92m"
        self.YELLOW = "\033[93m"
        self.RED = "\033[91m"
        self.RESET = "\033[0m"

    def update(self, raw_size: int, processed_size: int):
        """Receives updates from the PipelineTelemetry subject subject."""
        
        def get_color(size):
            percentage = size / self.max_queue_size if self.max_queue_size else 0
            if percentage < 0.5:
                return self.GREEN
            elif percentage < 0.8:
                return self.YELLOW
            else:
                return self.RED
                
        raw_color = get_color(raw_size)
        proc_color = get_color(processed_size)
        
        # Build UI Bar
        bar_length = 20
        raw_fill = int((raw_size / self.max_queue_size) * bar_length) if self.max_queue_size else 0
        proc_fill = int((processed_size / self.max_queue_size) * bar_length) if self.max_queue_size else 0
        
        raw_bar = "=" * raw_fill + "-" * (bar_length - raw_fill)
        proc_bar = "=" * proc_fill + "-" * (bar_length - proc_fill)
        
        # We output a carriage return string so it overlays dynamically, 
        # but standard print is safer in multi-process/threaded environments if interleaving occurs.
        print(f"\rTELEMETRY | Raw: {raw_color}[{raw_bar}] {raw_size}/{self.max_queue_size}{self.RESET} | "
              f"Processed: {proc_color}[{proc_bar}] {processed_size}/{self.max_queue_size}{self.RESET}", end="")
