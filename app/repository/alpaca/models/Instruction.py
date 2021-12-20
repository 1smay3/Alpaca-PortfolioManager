from dataclasses import dataclass

@dataclass
class Instruction:
    symbol: str
    side: str  # Enum
    notional: float
    type: str = "market"

