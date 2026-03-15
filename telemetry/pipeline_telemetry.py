import time

class PipelineTelemetry:

    def __init__(self, raw_queue, verified_queue, processed_queue, max_size):

        self.raw_queue = raw_queue
        self.verified_queue = verified_queue
        self.processed_queue = processed_queue
        self.max_size = max_size

    def get_bar(self, size):

        percent = size / self.max_size

        filled = int(percent * 10)

        bar = "[" + "#" * filled + "-" * (10 - filled) + "]"

        return bar

    def display(self):

        while True:

            raw_size = self.raw_queue.qsize()
            ver_size = self.verified_queue.qsize()
            proc_size = self.processed_queue.qsize()

            print("\nTELEMETRY")

            print(f"RAW STREAM        {self.get_bar(raw_size)} {raw_size}/{self.max_size}")
            print(f"INTERMEDIATE      {self.get_bar(ver_size)} {ver_size}/{self.max_size}")
            print(f"PROCESSED         {self.get_bar(proc_size)} {proc_size}/{self.max_size}")

            time.sleep(1)