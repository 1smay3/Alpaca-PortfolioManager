from app.util.strictdataclasses import TypeCheckedClass


@TypeCheckedClass
class Instruction:
    symbol: str
    side: str  # Enum
    weight: float
    type: str = "market"
    approval_status: bool = False
