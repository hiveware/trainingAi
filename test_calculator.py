import unittest

from calculator import calculate


class CalculatorTest(unittest.TestCase):
    def test_one_plus_two(self):
        self.assertEqual(calculate("1 + 2"), 3)

    def test_five_times_seven(self):
        self.assertEqual(calculate("5 * 7"), 35)

    def test_unknown_expression_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "not hard-coded"):
            calculate("2 + 2")

    def test_only_single_digit_operands_are_allowed(self):
        with self.assertRaisesRegex(ValueError, "left operand"):
            calculate("10 + 2")

    def test_only_plus_and_multiply_are_allowed(self):
        with self.assertRaisesRegex(ValueError, "Only \\+ and \\*"):
            calculate("5 - 2")


if __name__ == "__main__":
    unittest.main()
