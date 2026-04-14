#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any

class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data : list[str] = []
        self._rank : int = 0

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

    def validate(self, data: Any) -> bool:
        return isinstance(data, (int, float)) or (
            isinstance(data, list) and all(isinstance(x, (int, float)) for x in data))
    

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._data.append(str(item))
        else:
            self._data.append(str(data))


class TextProcessor(DataProcessor):

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

    def _is_valid_dict(self, data: Any) -> bool:
        return isinstance(data, dict) and all(
            isinstance (k, str) and isinstance(v, str) for k, v in data.items())
    
    def validate(self, data: Any) -> bool:
        return self._is_valid_dict(data) or (
            isinstance(data, list) and all(self._is_valid_dict(x) for x in data))
    
    def ingest(self, data: dict | list[dict]) -> None:
        if not self.validate(data):
            raise TypeError("improper log data")
        if isinstance(data, list):
            for item in data:
                self._data.append(f"{item['log_level']}: {item['log_message']}")
        else:
            self._data.append(f"{data['log_level']}: {data['log_message']}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    print(f"\nTest Numeric Processor...")
    numeric = NumericProcessor()

    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")

    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")
    except TypeError as e:
        print(f"Got exception: {e}")

    print(f"Processing data: [1, 2, 3, 4, 5]")
    numeric.ingest([1, 2, 3, 4, 5])

    print("Extracting 3 values...")

    for i in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    text = TextProcessor()

    print(f"Trying to validate input '42': {text.validate(42)}")

    print(f"Processing data: ['Hello', 'Nexus', 'World']")
    text.ingest(["Hello", "Nexus", "World"])

    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log = LogProcessor()

    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")

    logs = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"}
    ]
    print(f"Processing data: {logs}")
    log.ingest(logs)

    print("Extracting 2 values...")
    for i in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")
