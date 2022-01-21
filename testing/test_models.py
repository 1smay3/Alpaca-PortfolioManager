from app.util.strictdataclasses import StrictDataClass


@StrictDataClass
class ExampleBasicStrictDataClass:
    exampleString: str = ""
    exampleInt: int = 0
    exampleFloat: float = 0.0
    exampleBoolean: bool = False


portfolio_hardcode = {
    "VYM": 0.0033,
    "USMV": 0.1891,
    "MTUM": 0.0766,
    "IWF": 0.6586,
    "IWD": 0.0423,
    "IJR": 0.0291,
}
