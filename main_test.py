import unittest

from main import calculate_score

class TestCalculateScore(unittest.TestCase):
    def test_failed(self):
        self.assertEqual(calculate_score('X'), 0)

    def test_1_attempt(self):
        self.assertEqual(calculate_score('1'), 6)

    def test_6_attempts(self):
        self.assertEqual(calculate_score('6'), 1)

    def test_8_attempt(self):
        with self.assertRaises(ValueError):
            calculate_score('8')

    def test_negative_attempt(self):
        self.assertEqual(calculate_score('-1'), 0)

    def test_invalid_char(self):
        self.assertEqual(calculate_score('Y'), 0)


if __name__ == "__main__":
    unittest.main()
