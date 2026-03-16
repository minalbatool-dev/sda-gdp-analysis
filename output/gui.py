import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import time


class MatplotlibDashboard:
    """ Observer & Visualizer: Subscribes to telemetry updates and renders Matplotlib charts. """

    def __init__(self, max_queue_size: int, config: dict, processed_queue=None):
        self.max_queue_size = max_queue_size
        self.config = config
        self.processed_queue = processed_queue

        # -----------------------------
        # Telemetry State (Bar Chart)
        # -----------------------------
        self.raw_size = 0
        self.worker_size = 0
        self.processed_size = 0

        # -----------------------------
        # Chart State (Line Graphs)
        # -----------------------------
        MAX_POINTS = 100
        self.times = deque(maxlen=MAX_POINTS)
        self.raw_values = deque(maxlen=MAX_POINTS)
        self.avg_values = deque(maxlen=MAX_POINTS)

        # -----------------------------
        # Setup Figure
        # -----------------------------
        self.fig = plt.figure(figsize=(12, 8))
        self.fig.canvas.manager.set_window_title("Real-Time Pipeline Dashboard")

        # Grid spec to split layout
        gs = self.fig.add_gridspec(3, 1, height_ratios=[1, 2, 2], hspace=0.4)

        # 1. Bar Chart Subplot
        self.ax_bars = self.fig.add_subplot(gs[0, 0])
        self.ax_bars.set_title("Pipeline Telemetry - Stream Queue Health")
        self.ax_bars.set_xlim(0, self.max_queue_size)
        
        self.bar_labels = ["Processed Stream", "Intermediate Stream", "Raw Stream"]
        self.y_pos = [0, 1, 2]

        self.bars = self.ax_bars.barh(self.y_pos, [0, 0, 0], color=['green', 'green', 'red'])
        self.ax_bars.set_yticks(self.y_pos)
        self.ax_bars.set_yticklabels(self.bar_labels)
        
        # 2. Raw Values Line Graph
        self.ax_raw = self.fig.add_subplot(gs[1, 0])
        self.ax_raw.set_title("Live Sensor Values (Authentic Only)")
        self.ax_raw.set_ylabel("metric_value")
        self.line_raw, = self.ax_raw.plot([], [], lw=1.5, color='tab:blue')

        # 3. Running Average Line Graph
        self.ax_avg = self.fig.add_subplot(gs[2, 0])
        self.ax_avg.set_title("Live Sensor Running Average")
        self.ax_avg.set_xlabel("time_period")
        self.ax_avg.set_ylabel("computed_metric")
        self.line_avg, = self.ax_avg.plot([], [], lw=1.5, color='tab:red')

    # -----------------------------
    # Observer Update (Called by PipelineTelemetry)
    # -----------------------------
    def update(self, raw_size: int, worker_size: int, processed_size: int):
        self.raw_size = raw_size
        self.worker_size = worker_size
        self.processed_size = processed_size

    # -----------------------------
    # Drain Processed Stream
    # -----------------------------
    def _drain_processed_queue(self):
        if not self.processed_queue:
            return

        try:
            while True:
                item = self.processed_queue.get_nowait()
                if item is None:
                    continue  # In this GUI we just ignore poison pills for now

                # Store data point
                self.times.append(item.get("time_period", time.time()))
                self.raw_values.append(item.get("metric_value", 0.0))
                self.avg_values.append(item.get("computed_metric", 0.0))

        except:
            pass # Queue empty

    # -----------------------------
    # Animation Trigger
    # -----------------------------
    def _animate(self, frame):
        
        # 1. Update Telemetry Bars
        sizes = [self.processed_size, self.worker_size, self.raw_size]
        for i, bar in enumerate(self.bars):
            bar.set_width(sizes[i])

            # Color coding (Red > 80%, Yellow > 50%, Green)
            percentage = sizes[i] / self.max_queue_size if self.max_queue_size else 0
            if percentage > 0.8:
                bar.set_color('tab:red')
            elif percentage > 0.5:
                bar.set_color('tab:orange')
            else:
                bar.set_color('tab:green')

        # 2. Update Charts
        self._drain_processed_queue()

        if len(self.times) > 0:
            
            x_data = list(self.times)
            
            self.line_raw.set_data(x_data, list(self.raw_values))
            self.ax_raw.set_xlim(min(x_data), max(x_data) + 1)
            self.ax_raw.set_ylim(min(self.raw_values) - 10, max(self.raw_values) + 10)

            self.line_avg.set_data(x_data, list(self.avg_values))
            self.ax_avg.set_xlim(min(x_data), max(x_data) + 1)
            self.ax_avg.set_ylim(min(self.avg_values) - 10, max(self.avg_values) + 10)

        return self.bars + (self.line_raw, self.line_avg)

    # -----------------------------
    # Blocking GUI Loop
    # -----------------------------
    def show(self):
        # Update 10 times a second
        self.ani = animation.FuncAnimation(
            self.fig, self._animate, interval=100, blit=False, cache_frame_data=False
        )
        
        # This blocks until window is closed
        plt.show()
