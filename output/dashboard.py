def dashboard_worker(processed_queue):

    while True:

        packet = processed_queue.get()

        if packet is None:
            break

        entity = packet["entity_name"]
        time_period = packet["time_period"]
        value = packet["metric_value"]
        avg = packet["computed_metric"]

        print("\n=============================")
        print(f"[CHART] {entity} | Time {time_period}")
        print(f"Value: {value:.2f}")
        print(f"Running Avg: {avg:.2f}")