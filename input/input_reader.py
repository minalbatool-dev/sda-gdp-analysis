import pandas as pd
import time
import os

def input_reader(config, raw_queue):
    print("INPUT PROCESS STARTED")
    dataset_path = config["dataset_path"]
    delay = config["pipeline_dynamics"]["input_delay_seconds"]

    # Detect file type
    if dataset_path.endswith(".csv"):
        df = pd.read_csv(dataset_path)

    elif dataset_path.endswith(".xlsx") or dataset_path.endswith(".xls"):
        df = pd.read_excel(dataset_path, engine="openpyxl")

    else:
        raise ValueError("Unsupported dataset format")

    columns = config["schema_mapping"]["columns"]

    for _, row in df.iterrows():

        packet = {}

        for col in columns:

            source = col["source_name"]
            internal = col["internal_mapping"]

            packet[internal] = row[source]

        raw_queue.put(packet)

        print("[INPUT] Packet pushed:", packet)

        time.sleep(delay)