from collections import deque


def running_average(state, item, window_size):

    """
    Functional core: compute running average per entity.

    state: tuple containing the sliding window
    item: incoming data packet
    window_size: max window size
    """

    if not state:
        window = deque(maxlen=window_size)
    else:
        window = state

    value = item.get("metric_value", 0.0)

    window.append(value)

    avg = sum(window) / len(window)

    updated_item = item.copy()
    updated_item["running_average"] = avg

    return window, updated_item
