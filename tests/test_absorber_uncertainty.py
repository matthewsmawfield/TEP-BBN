import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.lib.absorber_uncertainty import density_interval


class UncertaintyTests(unittest.TestCase):
    def test_power_law_endpoints_and_inverse(self):
        lo, hi = density_interval(657.4, .15)
        self.assertAlmostEqual(lo,657.4*10**(-.1))
        self.assertAlmostEqual(hi,657.4*10**(.1))
        self.assertAlmostEqual(lo*hi,657.4**2)

    def test_zero_error(self):
        self.assertEqual(density_interval(10,0),(10,10))

    def test_invalid_inputs(self):
        for density, sigma in [(0,.1),(-1,.1),(1,-1),(float('nan'),.1),(1,float('inf'))]:
            with self.assertRaises(ValueError):
                density_interval(density,sigma)


if __name__ == '__main__':
    unittest.main()
