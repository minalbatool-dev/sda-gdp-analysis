import multiprocessing as mp
import json
import time

from input.input_reader import InputReader
from core.worker import start_worker
from core.aggregator import start_aggregator
from telemetry.pipeline_telemetry import PipelineTelemetry
from output.dashboard import Dashboard
from output.charts import LiveCharts


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

    dashboard = Dashboard(max_size, config)
    telemetry.subscribe(dashboard)

    charts = LiveCharts(config)

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

    producer_alive = True

    print("\n[SYSTEM] Pipeline started\n")

    # -------------------------------
    # Main event loop
    # -------------------------------
    while True:

        # If producer finished → send poison pills
        if producer_alive and not producer.is_alive():

            producer_alive = False
            producer.join()

            print("\n[SYSTEM] Input stream finished. Sending poison pills...\n")

            for _ in range(parallelism):
                raw_queue.put(None)

        # ---------------------------
        # Read processed output
        # ---------------------------
        try:
            while True:

                item = processed_queue.get_nowait()

                if item is None:
                    print("\n[SYSTEM] Pipeline finished successfully\n")
                    return

                charts.render(item)

        except:
            pass

        # ---------------------------
        # Update telemetry
        # ---------------------------
        telemetry.notify()

        time.sleep(0.5)


if __name__ == "__main__":
    mp.set_start_method("spawn")
    main()
