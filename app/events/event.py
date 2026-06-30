from dataclasses import dataclass


@dataclass
class Event:

    title: str

    severity: str

    description: str