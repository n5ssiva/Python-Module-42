#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any
from typing import Protocol


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class DataProcessor(ABC):

    def __init__(self) -> None:
        self._data: list[str] = []
        self._rank: int = 0
        self.name: str = ""

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise ValueError("No data to output")
        rank = self._rank
        value = self._data.pop(0)
        self._rank += 1
        return (rank, value)


class NumericProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__()

        self.name = "Numeric Processor"

    def validate(self, data: Any) -> bool:
        return isinstance(data, (int, float)) or (
            isinstance(data, list) and
            all(isinstance(x, (int, float)) for x in data))

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._data.append(str(item))
        else:
            self._data.append(str(data))


class TextProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__()

        self.name = "Text Processor"

    def validate(self, data: Any) -> bool:
        return isinstance(data, str) or (
            isinstance(data, list) and all(isinstance(x, str) for x in data))

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("improper text data")
        if isinstance(data, list):
            for item in data:
                self._data.append(item)
        else:
            self._data.append(str(data))


class LogProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__()

        self.name = "Log Processor"

    def _is_valid_dict(self, data: Any) -> bool:
        return isinstance(data, dict) and all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in data.items())

    def validate(self, data: Any) -> bool:
        return self._is_valid_dict(data) or (
            isinstance(data, list) and
            all(self._is_valid_dict(x) for x in data))

    def ingest(self, data: dict | list[dict]) -> None:
        if not self.validate(data):
            raise TypeError("improper log data")
        if isinstance(data, list):
            for item in data:
                self._data.append(f"{item['log_level']}:"
                                  f" {item['log_message']}")
        else:
            self._data.append(f"{data['log_level']}: {data['log_message']}")


class DataStream:

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            processed = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    processed = True
                    break
            if not processed:
                print("DataStream error - Can't process"
                      f" element in stream: {element}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            total = proc._rank + len(proc._data)
            remaining = len(proc._data)
            print(f"{proc.name}: total {total} items processed,"
                  f" remaining {remaining} on processor")

    def output_pipeline(self, nb: int,
                        plugin: ExportPlugin) -> None:
        for proc in self._processors:
            results: list[tuple[int, str]] = []
            for _ in range(min(nb, len(proc._data))):
                results.append(proc.output())
            if results:
                plugin.process_output(results)


class CSVPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = [item[1] for item in data]
        print("CSV Output:")
        print(",".join(values))


class JSONPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        entries = [f'"item_{item[0]}": "{item[1]}"' for item in data]
        print("JSON Output:")
        print("{" + ", ".join(entries) + "}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")
    print("Initialize Data Stream...\n")
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Processors\n")
    ds.register_processor(NumericProcessor())
    ds.register_processor(TextProcessor())
    ds.register_processor(LogProcessor())

    batch1 = [
        "Hello world",
        [3.14, -1, 2.71],
        [{"log_level": "WARNING",
          "log_message": "Telnet access! Use ssh instead"},
         {"log_level": "INFO",
          "log_message": "User wil is connected"}],
        42,
        ["Hi", "five"]
    ]
    print(f"Send first batch of data on stream: {batch1}")
    print()
    ds.process_stream(batch1)
    ds.print_processors_stats()

    print("\nSend 3 processed data from each processor"
          " to a CSV plugin:")
    ds.output_pipeline(3, CSVPlugin())
    ds.print_processors_stats()

    batch2 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [{"log_level": "ERROR",
          "log_message": "500 server crash"},
         {"log_level": "NOTICE",
          "log_message": "Certificate expires in 10 days"}],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]

    print(f"\nSend another batch of data: {batch2}")
    print()
    ds.process_stream(batch2)
    ds.print_processors_stats()

    print("\nSend 5 processed data from each processor"
          " to a JSON plugin:")
    ds.output_pipeline(5, JSONPlugin())
    print()
    ds.print_processors_stats()
