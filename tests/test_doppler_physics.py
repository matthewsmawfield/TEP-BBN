import unittest

import numpy as np

from scripts.lib.doppler_physics import KB_OVER_MP, compute_doppler_b


class TestDopplerPhysics(unittest.TestCase):
    def test_thermal_width_relation(self):
        T_K = 10000.0  # 10,000 K
        b_turb = 5.0  # 5 km/s

        b_H = compute_doppler_b(T_K, b_turb, isotope="H")
        b_D = compute_doppler_b(T_K, b_turb, isotope="D")

        # Verify b_D < b_H for T > 0
        self.assertLess(b_D, b_H)

        # Expected thermal components:
        # b_thermal_H = sqrt(2 * 0.008254958 * 10000) = sqrt(165.099) = 12.849 km/s
        # b_thermal_D = sqrt(0.008254958 * 10000) = sqrt(82.54958) = 9.0857 km/s
        # b_H = sqrt(25 + 165.099) = sqrt(190.099) = 13.7876 km/s
        # b_D = sqrt(25 + 82.54958) = sqrt(107.54958) = 10.3706 km/s

        self.assertAlmostEqual(b_H, np.sqrt(25.0 + 2.0 * KB_OVER_MP * T_K), places=5)
        self.assertAlmostEqual(b_D, np.sqrt(25.0 + KB_OVER_MP * T_K), places=5)

    def test_zero_temperature(self):
        T_K = 0.0
        b_turb = 8.5
        b_H = compute_doppler_b(T_K, b_turb, isotope="H")
        b_D = compute_doppler_b(T_K, b_turb, isotope="D")
        self.assertEqual(b_H, b_turb)
        self.assertEqual(b_D, b_turb)


if __name__ == "__main__":
    unittest.main()
