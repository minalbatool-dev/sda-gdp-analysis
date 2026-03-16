from multiprocessing import Queue
from typing import Dict, Any
from core.security import generate_signature


class Worker:

    def __init__(self, raw_queue: Queue, worker_queue: Queue, config: Dict[str, Any]):
        self.raw_queue = raw_queue
        self.worker_queue = worker_queue
        self.config = config

    def run(self):

        processing_cfg = self.config.get("processing", {})

        stateless_cfg = processing_cfg.get("stateless_tasks", {})
        stateful_cfg = processing_cfg.get("stateful_tasks", {})

        secret_key = stateless_cfg.get("secret_key")
        iterations = stateless_cfg.get("iterations", 100000)

        # ---------------------------------
        # Counters
        # ---------------------------------

        valid_packets = 0
        dropped_packets = 0

        while True:

            item = self.raw_queue.get()

            if item is None:

                print(
                    f"[WORKER SUMMARY] Valid: {valid_packets} | Dropped: {dropped_packets}"
                )

                self.worker_queue.put(None)
                break

            # ---------------------------------
            # Signature Verification
            # ---------------------------------

            raw_value = item.get("metric_value")
            if raw_value is None:
                raw_value = 0.0
                
            raw_value_str = f"{raw_value:.2f}"

            received_hash = item.get("security_hash")

            if secret_key is not None:
                computed_hash = generate_signature(
                    raw_value_str,
                    secret_key,
                    iterations
                )

                if received_hash != computed_hash:
                    dropped_packets += 1
                    continue

            valid_packets += 1

            # ---------------------------------
            # Forward Valid Packet
            # ---------------------------------

            self.worker_queue.put(item)

            # ---------------------------------
            # Periodic Debug Output
            # ---------------------------------

            if valid_packets % 100 == 0:
                print(
                    f"[WORKER] Processed {valid_packets} valid packets | Dropped {dropped_packets}"
                )


# -----------------------------------------
# Multiprocessing entry function (IMPORTANT)
# -----------------------------------------

def start_worker(config, raw_queue, worker_queue):
    worker = Worker(raw_queue, worker_queue, config)
    worker.run()
