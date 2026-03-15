import multiprocessing as mp
import time
import queue

from config.config_loader import ConfigLoader
from input.input_reader import InputReader
from core.worker import Worker
from telemetry.pipeline_telemetry import PipelineTelemetry
from output.dashboard import Dashboard
from output.charts import LiveCharts

def start_input(config, raw_queue):
    reader = InputReader(config, raw_queue)
    reader.run()

def start_worker(config, raw_queue, processed_queue):
    worker = Worker(raw_queue, processed_queue, config)
    worker.run()

def main():
    print("\n" + "="*80)
    print("PHASE 3: GENERIC CONCURRENT REAL-TIME PIPELINE")
    print("="*80)

    # 1. Load Configurations
    config_path = "phase3/config.json" if "phase3" not in __file__ else "config.json"
    try:
        config = ConfigLoader.load(config_path)
    except FileNotFoundError:
        config_path = "phase3/config.json"
        config = ConfigLoader.load(config_path)
    dynamics = config.get("pipeline_dynamics", {})
    max_size = dynamics.get("stream_queue_max_size", 50)
    parallelism = dynamics.get("core_parallelism", 3)

    # 2. Initialize Bounded Streams
    raw_queue = mp.Queue(maxsize=max_size)
    processed_queue = mp.Queue(maxsize=max_size)

    # 3. Initialize Telemetry & Observers
    telemetry = PipelineTelemetry(raw_queue, processed_queue)
    dashboard = Dashboard(max_size)
    telemetry.subscribe(dashboard)
    charts = LiveCharts(config)

    # 4. Start Producer (InputReader)
    producer = mp.Process(target=start_input, args=(config, raw_queue))
    producer.start()

    # 5. Start Consumers (Core Workers)
    workers = []
    print(f"[SYSTEM] Starting {parallelism} Core Workers...")
    for i in range(parallelism):
        w = mp.Process(target=start_worker, args=(config, raw_queue, processed_queue))
        w.start()
        workers.append(w)

    print("[SYSTEM] Pipeline online. Awaiting stream processing...\n")
    
    # 6. Main Orchestrator Loop
    active_workers = parallelism
    producer_alive = True
    
    try:
        while active_workers > 0:
            # Poll Telemetry (Updates Dashboard)
            telemetry.notify()
            
            # Check if producer finished producing
            if producer_alive and not producer.is_alive():
                producer_alive = False
                # Inject poison pills for each worker into raw stream
                for _ in range(parallelism):
                    try:
                        raw_queue.put(None, timeout=1) # Prevent blocking orchestrator
                    except queue.Full:
                        pass
            
            # Non-blocking processing of output streams
            try:
                # Process all available items in the queue
                while not processed_queue.empty():
                    item = processed_queue.get_nowait()
                    if item is None:
                        active_workers -= 1
                    else:
                        charts.render(item)
            except queue.Empty:
                pass
                
            # Dashboard refresh rate (throttle orchestrator usage)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\n[SYSTEM] Pipeline interrupted by user.")
    
    finally:
        print("\n\n" + "="*80)
        print("PIPELINE EXECUTION COMPLETE. CLEANING UP...")
        print("="*80)
        
        if producer.is_alive():
            producer.terminate()
        producer.join()
        
        for w in workers:
            if w.is_alive():
                w.terminate()
            w.join()

if __name__ == '__main__':
    main()
