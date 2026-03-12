from multiprocessing import Queue

class PipelineTelemetry:
    """Subject in the Observer pattern representing the pipeline telemetry monitor.
    
    Polls queue sizes independently without coupling directly to processor logic.
    """

    def __init__(self, raw_queue: Queue, processed_queue: Queue):
        self.raw_queue = raw_queue
        self.processed_queue = processed_queue
        self.observers = []

    def subscribe(self, observer):
        """Attach an observer."""
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer):
        """Detach an observer."""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self):
        """Notify all observers of the current queue sizes."""
        # Note: multiprocessing.Queue.qsize() can be approximate, 
        # but it serves our telemetry requirements.
        try:
            raw_size = self.raw_queue.qsize()
            processed_size = self.processed_queue.qsize()
            
            for observer in self.observers:
                observer.update(raw_size, processed_size)
        except NotImplementedError:
            print("Queue size not supported on this platform.")
