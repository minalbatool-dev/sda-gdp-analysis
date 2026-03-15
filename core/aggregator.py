from collections import deque

def aggregator_worker(verified_queue, processed_queue, config):
    window_size = config["processing"]["stateful_tasks"].get("running_average_window_size", 10)

    window = deque(maxlen=window_size)

    while True:

        packet = verified_queue.get()

        if packet is None:
            break

        value = packet["metric_value"]

        window.append(value)

        avg = sum(window) / len(window)

        packet["computed_metric"] = avg

        processed_queue.put(packet)