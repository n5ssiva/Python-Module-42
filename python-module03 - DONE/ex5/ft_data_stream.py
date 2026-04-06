#!/usr/bin/env python3
"""Exercise 5: Generator - Generetor system with event."""
import random
import typing

names = ['alice', 'bob', 'charlie', 'dylan']
actions = ['run', 'eat', 'sleep', 'climb', 'swim', 'grab', 'move', 'release']


def gen_event() -> typing.Generator[tuple[str, str], None, None]:
    while True:
        name = random.choice(names)
        action = random.choice(actions)
        yield (name, action)


def consume_event(
    events: list[tuple[str, str]]
) -> typing.Generator[tuple[str, str], None, None]:
    while events:
        event = random.choice(events)
        events.remove(event)
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")

    gen = gen_event()
    for i in range(1000):
        event = next(gen)
        print(f"Event {i}: Player {event[0]} did action {event[1]}")

    events_list = [next(gen) for _ in range(10)]
    print(f"Built list for 10 events: {events_list}")

    for event in consume_event(events_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events_list}")


if __name__ == "__main__":
    main()
