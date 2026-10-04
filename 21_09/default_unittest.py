from solution import classify_number
import unittest
class TestClassifyNumber(unittest.TestCase):
    def test_positive_even(self):
        self.assertEqual(
        classify_number(8),
        "positive even"
        )
if __name__ == "__main__":
    unittest.main()