from typing import Dict, Any, Tuple

def running_average(state: tuple, item: Dict[str, Any], window_size: int) -> Tuple[tuple, Dict[str, Any]]:
    """
    Purely functional calculation of a running average.
    
    Args:
        state: A tuple representing the previous history. e.g., (oldest_val, next_val, ..., newest_val). 
               Must be immutable.
        item: The current generic data packet.
        window_size: The window size for the running average.
        
    Returns:
        (new_state, updated_item): The new immutable state and the item with added calculations.
    """
    
    metric_value = item.get("metric_value", 0.0)
    
    # Calculate new state
    new_state_list = list(state)
    new_state_list.append(metric_value)
    if len(new_state_list) > window_size:
        new_state_list = new_state_list[-window_size:]
        
    new_state = tuple(new_state_list)
    
    # Calculate computed metric
    computed_avg = sum(new_state) / len(new_state) if new_state else 0.0
    
    # Do not mutate the original dictionary
    updated_item = item.copy()
    updated_item["computed_metric"] = computed_avg
    
    return new_state, updated_item
