from multiprocessing import Queue
from typing import Dict, Any
from core.processors import running_average

class Worker:
    """Consumer/Producer: Pulls raw packets, functionally processes them, pushes processed packets."""

    def __init__(self, raw_queue: Queue, processed_queue: Queue, config: Dict[str, Any]):
        self.raw_queue = raw_queue
        self.processed_queue = processed_queue
        self.config = config

    def run(self):
        """Infinite loop pulling from raw_queue, maintaining pure functional states per entity."""
        window_size = self.config.get("processing", {}).get("running_average_window_size", 10)
        
        # State management dictionary: key=entity_name, value=tuple(history)
        # The processing logic itself is functional; we only bind the new state here.
        states = {}

        while True:
            item = self.raw_queue.get()
            
            # Poison pill pattern
            if item is None:
                # Pass poison pill down to output modules
                self.processed_queue.put(None)
                break

            entity = item.get("entity_name")
            if entity not in states:
                states[entity] = ()

            # Pure function call, no mutations inside processors
            new_state, updated_item = running_average(states[entity], item, window_size)
            
            # Rebind locally for next iteration
            states[entity] = new_state
            
            # Push processed stream
            self.processed_queue.put(updated_item)
