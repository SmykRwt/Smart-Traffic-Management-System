from dataclasses import dataclass

@dataclass
class Rule:

    name: str

    severity: str

    description: str

    condition: callable