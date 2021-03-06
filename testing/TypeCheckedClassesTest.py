import unittest
from app.repository.alpaca.models.Instructions import Instruction
from testing.TestModels import ExampleBasicTypeCheckedClass


class MyTestCase(unittest.TestCase):

    # Funnily, test functions must be named "test_[function name]" or they literally won't be processed.
    def test_check_strict_data_class_with_correct_types(self):
        try:
            ExampleBasicTypeCheckedClass()
            # FIXME: No proper way in python to have something like self.assertNotRaises so we use this nonsense
            #  instead. Add it?
        except TypeError:
            self.fail("Unexpected error")

    def test_check_strict_data_class_with_int_as_string_for_fake_class(self):
        with self.assertRaises(TypeError):
            ExampleBasicTypeCheckedClass(exampleString=1)

    def test_check_strict_data_class_for_real_class(self):
        try:
            Instruction()
        except TypeError:
            self.fail("Unexpected error")

    def test_check_strict_data_class_string_as_float_with_real_class(self):
        with self.assertRaises(TypeError):
            Instruction(weight="string")

    def test_check_strict_data_class_string_as_int_with_real_class(self):
        with self.assertRaises(TypeError):
            Instruction(type=123)
