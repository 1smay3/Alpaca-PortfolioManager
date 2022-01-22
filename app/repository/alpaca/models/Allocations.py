from app.util.strictdataclasses import StrictDataClass


@StrictDataClass
class Allocation:
    symbol: str
    weight: float
    approval_status: bool = False
