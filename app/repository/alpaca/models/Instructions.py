from dataclasses import dataclass


@dataclass
class Instruction:
    symbol: str
    side: str  # Enum
    weight: float
    type: str = "market"


