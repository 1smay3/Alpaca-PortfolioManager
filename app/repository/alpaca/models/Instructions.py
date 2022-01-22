from app.util.strictdataclasses import StrictDataClass


@StrictDataClass
class Instruction:
    symbol: str
    side: str  # Enum
    weight: float
    type: str = "market"
    approval_status: bool = False
