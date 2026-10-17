import sys
import unittest
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.lib.acoustic_peaks import interpolated_peak


class PeakTests(unittest.TestCase):
    def test_recovers_off_grid_parabola(self):
        x = np.arange(180, 261)
        self.assertAlmostEqual(interpolated_peak(x, 100 - (x - 220.37)**2), 220.37)

    def test_preserves_previous_interior_formula(self):
        x = np.arange(180, 261)
        y = np.exp(-((x - 220.37)/5)**2)
        i = np.argmax(y)
        old = x[i] + .5*(y[i-1]-y[i+1])/(y[i-1]-2*y[i]+y[i+1])
        self.assertEqual(interpolated_peak(x, y), old)

    def test_rejects_boundary_flat_nonfinite_and_irregular(self):
        for x, y in [([0,1,2], [3,2,1]), ([0,1,2], [1,2,3]),
                     ([0,1,2], [1,1,1]), ([0,1,2,3], [0,2,2,0]),
                     ([0,1,2], [0,float('nan'),0]), ([0,1,3], [0,1,0])]:
            with self.subTest(x=x, y=y), self.assertRaises(ValueError):
                interpolated_peak(x, y)


if __name__ == '__main__':
    unittest.main()
