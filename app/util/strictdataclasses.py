import dataclasses


def check_keyword_args(cls, kwargs):
    # Get all "annotations" from the original class, which are actually it's arguments, and parse to a dictionary
    class_fields = cls.__annotations__.items()
    for field_name, field_type in class_fields:
        # Iterate over all class field names, types and all keyword arg names and types
        for keyword_arg_name, keyword_arg in kwargs.items():
            # When we find a keyword arg that matches a class field
            if field_name == keyword_arg_name:
                # Check that incoming type matches expected
                if not isinstance(keyword_arg, field_type):
                    # Throw a fatal exception if we try to force a type that is defined otherwise
                    raise TypeError(
                        f"Expected {field_name} to be {field_type}, "
                        f"but got {repr(type(keyword_arg))}"
                    )


class TypeCheckedClass(object):
    original_class: None

    # Called when the "SDC"-annotated class is imported
    def __init__(self, original_class):
        self.original_class = original_class

    # Called when the "SDC"-annotated class is instantiated, with any arguments
    def __call__(self, *args, **kwargs):
        # Checks all keyword args for their expected types, returning this if all types are expected
        check_keyword_args(self.original_class, kwargs)
        return self.original_class(**kwargs)
