import unittest
from app import biaya


class TestBiaya(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(biaya(0), 0)

    def test_below_threshold(self):
        self.assertEqual(biaya(49_999), 0)

    def test_at_threshold(self):
        self.assertEqual(biaya(50_000), 500)

    def test_normal(self):
        self.assertEqual(biaya(275_550), 2_755)

    def test_round_down(self):
        self.assertEqual(biaya(123_456), 1_234)

    def test_cap_boundary(self):
        self.assertEqual(biaya(500_000), 5_000)

    def test_above_cap(self):
        self.assertEqual(biaya(900_000), 5_000)

    def test_negative(self):
        with self.assertRaises(ValueError):
            biaya(-1)

    def test_wrong_types(self):
        for value in ["50000", 50000.0, True, None]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    biaya(value)

    def test_just_above_threshold(self):
        self.assertEqual(biaya(50_001), 500)

    def test_just_below_cap(self):
        self.assertEqual(biaya(499_999), 4_999)
if __name__ == "__main__":
    unittest.main()
