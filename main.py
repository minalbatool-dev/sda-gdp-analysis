from multiprocessing import Process, Queue

from input.input_reader import input_reader
from core.worker import verification_worker
from core.aggregator import aggregator_worker
from output.dashboard import dashboard_worker
from telemetry.pipeline_telemetry import PipelineTelemetry
from config.config_loader import load_config


def main():
    print("\n" + "="*80)
    print("PHASE 3: GENERIC CONCURRENT REAL-TIME PIPELINE")
    print("="*80)

    config = load_config("config.json")

    max_size = config["pipeline_dynamics"]["stream_queue_max_size"]

    raw_queue = Queue(maxsize=max_size)
    verified_queue = Queue(maxsize=max_size)
    processed_queue = Queue(maxsize=max_size)

    input_process = Process(target=input_reader, args=(config, raw_queue))

    workers = []

    for _ in range(config["pipeline_dynamics"]["core_parallelism"]):

        p = Process(target=verification_worker, args=(raw_queue, verified_queue, config))
        workers.append(p)

    aggregator = Process(target=aggregator_worker, args=(verified_queue, processed_queue, config))

    dashboard = Process(target=dashboard_worker, args=(processed_queue,))

    telemetry = PipelineTelemetry(raw_queue, verified_queue, processed_queue, max_size)

    input_process.start()

    for w in workers:
        w.start()

    aggregator.start()

    dashboard.start()

    import threading

    telemetry_thread = threading.Thread(target=telemetry.display)
    telemetry_thread.start()

if __name__ == "__main__":
    main()
