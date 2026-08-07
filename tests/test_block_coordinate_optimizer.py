import unittest

import numpy as np

from scripts.lib.block_coordinate_optimizer import BlockCoordinateOptimizer


class TestBlockOptimizer(unittest.TestCase):
    def test_synthetic_benchmark(self):
        # Simple quadratic bowl benchmark function
        # Global minimum at x = [1.0, 1.0, ..., 1.0], f(x) = 0.0
        def benchmark_objective(x):
            return np.sum((x - 1.0) ** 2)

        opt = BlockCoordinateOptimizer(benchmark_objective)
        x0 = np.zeros(5)

        res = opt.optimize_block_coordinate(x0, verbose=False)

        self.assertLess(res["fun"], 1e-3)
        self.assertTrue(np.allclose(res["x"], np.ones(5), atol=1e-1))

    def test_multi_start_stability(self):
        def simple_quadratic(x):
            return np.sum((x - 2.5) ** 2)

        opt = BlockCoordinateOptimizer(simple_quadratic)
        x0 = np.zeros(3)

        ms_res = opt.run_multi_start(x0, n_starts=5, jitter_scale=0.1, verbose=False)

        self.assertTrue(ms_res["is_mode_stable"])
        self.assertGreaterEqual(ms_res["matching_starts"], 3)
        self.assertAlmostEqual(ms_res["best_result"]["fun"], 0.0, places=4)


if __name__ == "__main__":
    unittest.main()
