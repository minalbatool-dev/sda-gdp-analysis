from multiprocessing import Queue
from typing import Dict, Any
from core.processors import running_average


class Aggregator:

    def __init__(self, config: Dict[str, Any], worker_queue: Queue, output_queue: Queue, worker_count: int):

        self.config = config
        self.worker_queue = worker_queue
        self.output_queue = output_queue
        self.worker_count = worker_count
        
        self.states = {}

    def run(self):

        processing_cfg = self.config.get("processing", {})
        stateful_cfg = processing_cfg.get("stateful_tasks", {})
        window_size = stateful_cfg.get("running_average_window_size", 10)

        finished_workers = 0

        while True:

            item = self.worker_queue.get()

            # -----------------------------
            # Worker finished
            # -----------------------------
            if item is None:

                finished_workers += 1

                if finished_workers == self.worker_count:
                    self.output_queue.put(None)
                    break

                continue

            # -----------------------------
            # Stateful Processing (Running Average)
            # -----------------------------
            entity = item.get("entity_name")

            if entity not in self.states:
                self.states[entity] = ()

            new_state, updated_item = running_average(
                self.states[entity],
                item,
                window_size
            )

            self.states[entity] = new_state
            
            # Map running_average to computed_metric for charts
            updated_item["computed_metric"] = updated_item.get("running_average", 0.0)

            # -----------------------------
            # Forward processed item
            # -----------------------------
            self.output_queue.put(updated_item)


# --------------------------------------
# Multiprocessing entry point
# --------------------------------------

def start_aggregator(config, worker_queue, output_queue, worker_count):

    aggregator = Aggregator(config, worker_queue, output_queue, worker_count)
    aggregator.run()
