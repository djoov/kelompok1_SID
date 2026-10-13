import unittest

from app import biaya


class TestBiaya(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(biaya(100000), 1000)

    def test_cap(self):
        self.assertEqual(biaya(1000000), 5000)

    def test_zero(self):
        self.assertEqual(biaya(0), 0)

    def test_invalid(self):
        for amount in [-1, "100000", True]:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    biaya(amount)


if __name__ == "__main__":
    unittest.main()
