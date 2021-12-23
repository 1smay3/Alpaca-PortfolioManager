from app.util.strictdataclasses import StrictDataClass


@StrictDataClass
class ExampleBasicStrictDataClass:
    exampleString: str = ""
    exampleInt: int = 0
    exampleFloat: float = 0.0
    exampleBoolean: bool = False
