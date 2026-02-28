from typing import List

class ConsoleWriter:
    def write(self, data):
        print("\n===== GDP ANALYSIS RESULTS =====\n")
        
        for section, content in data.items():
            print(f"\n--- {section.upper()} ---")
            print(content)