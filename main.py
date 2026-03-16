import multiprocessing as mp
import json
import time
import threading

from input.input_reader import InputReader
from core.worker import start_worker
from core.aggregator import start_aggregator
from telemetry.pipeline_telemetry import PipelineTelemetry
from output.gui import MatplotlibDashboard


def telemetry_poller(telemetry, producer):
    """ Polls telemetry in the background so the GUI thread isn't blocked. """
    while producer.is_alive():
        telemetry.notify()
        time.sleep(0.1)


def main():

    # -------------------------------
    # Load configuration
    # -------------------------------
    with open("config.json") as f:
        config = json.load(f)

    dynamics = config.get("pipeline_dynamics", {})

    max_size = dynamics.get("stream_queue_max_size", 50)
    parallelism = dynamics.get("core_parallelism", 4)

    # -------------------------------
    # Create queues
    # -------------------------------
    raw_queue = mp.Queue(maxsize=max_size)
    worker_queue = mp.Queue(maxsize=max_size)
    processed_queue = mp.Queue(maxsize=max_size)

    # -------------------------------
    # Telemetry + Observers
    # -------------------------------
    telemetry = PipelineTelemetry(raw_queue, worker_queue, processed_queue)

    # GUI Dashboard
    dashboard = MatplotlibDashboard(max_size, config, processed_queue)
    telemetry.subscribe(dashboard)

    # -------------------------------
    # Producer
    # -------------------------------
    producer = mp.Process(
        target=InputReader(config, raw_queue).run
    )

    # -------------------------------
    # Workers
    # -------------------------------
    workers = []

    for _ in range(parallelism):
        p = mp.Process(
            target=start_worker,
            args=(config, raw_queue, worker_queue)
        )
        workers.append(p)

    # -------------------------------
    # Aggregator
    # -------------------------------
    aggregator = mp.Process(
        target=start_aggregator,
        args=(config, worker_queue, processed_queue, parallelism)
    )

    # -------------------------------
    # Start all processes
    # -------------------------------
    producer.start()

    for w in workers:
        w.start()

    aggregator.start()

    print("\n[SYSTEM] Pipeline started. Opening dashboard...\n")

    # Start independent telemetry thread
    poller = threading.Thread(target=telemetry_poller, args=(telemetry, producer), daemon=True)
    poller.start()

    # -------------------------------
    # Blocking GUI loop
    # -------------------------------
    dashboard.show()

    # If window is closed, shut down cleanly
    print("\n[SYSTEM] Shutting down...")
    if producer.is_alive():
        producer.terminate()
        
    for w in workers:
        w.terminate()
        
    aggregator.terminate()
    
    print("[SYSTEM] Pipeline finished successfully\n")


if __name__ == "__main__":
    mp.set_start_method("spawn")
    main()
