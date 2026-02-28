from typing import List


class ConsoleWriter:
    def write(self, records: List[dict]) -> None:
        print("\n===== ANALYSIS OUTPUT =====\n")
        for record in records:
            for key, value in record.items():
                print(f"{key}:")
                print(value)
                print()