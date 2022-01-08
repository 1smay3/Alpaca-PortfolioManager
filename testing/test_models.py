from app.util.strictdataclasses import TypeCheckedClass


@TypeCheckedClass
class ExampleBasicTypeCheckedClass:
    exampleString: str = ""
    exampleInt: int = 0
    exampleFloat: float = 0.0
    exampleBoolean: bool = False


