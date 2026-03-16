class PipelineTelemetry:

    def __init__(self, raw_queue, worker_queue, processed_queue):

        self.raw_queue = raw_queue
        self.worker_queue = worker_queue
        self.processed_queue = processed_queue

        self.observers = []

    # ---------------------------------
    # Observer registration
    # ---------------------------------

    def subscribe(self, observer):
        self.observers.append(observer)

    # ---------------------------------
    # Notify observers
    # ---------------------------------

    def notify(self):

        try:
            raw_size = self.raw_queue.qsize()
        except:
            raw_size = 0

        try:
            worker_size = self.worker_queue.qsize()
        except:
            worker_size = 0

        try:
            processed_size = self.processed_queue.qsize()
        except:
            processed_size = 0

        for observer in self.observers:
            observer.update(raw_size, worker_size, processed_size)
