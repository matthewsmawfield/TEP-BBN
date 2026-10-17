import numpy as np
from scipy.optimize import minimize


class BlockCoordinateOptimizer:
    """
    3-Block Coordinate Profiling Optimizer with scale-aware convergence gates.

    Blocks:
      1. Shared Baseline: Optimize shared physical parameters (holding candidate fixed).
      2. Candidate Neighbourhood: Optimize candidate component.
      3. Spectral Calibration: Analytical continuum/zero-level profiling (inside objective).

    Block 4 (Global Release) removed for performance — it was redundant after
    blocks 1+2 and dominated runtime with 141+ parameter L-BFGS-B calls.
    """
    def __init__(self, objective_func, candidate_param_indices=None, rel_tol=1e-6, abs_tol=0.1, grad_tol=1e-3,
                 maxiter_shared=50, maxiter_cand=50, maxiter_global=100):
        self.objective_func = objective_func
        self.candidate_param_indices = candidate_param_indices or []
        self.rel_tol = rel_tol
        self.abs_tol = abs_tol
        self.grad_tol = grad_tol
        self.maxiter_shared = maxiter_shared
        self.maxiter_cand = maxiter_cand
        self.maxiter_global = maxiter_global

    def optimize_block_coordinate(self, x0, bounds=None, max_cycles=5, verbose=False):
        x_curr = np.array(x0, dtype=float)
        n_params = len(x_curr)

        candidate_idx = set(self.candidate_param_indices)
        shared_idx = [i for i in range(n_params) if i not in candidate_idx]
        cand_idx_list = list(candidate_idx)

        l_curr = self.objective_func(x_curr)
        total_evals = 1
        total_iters = 0

        cycle_history = []

        if verbose:
            print(f"[BlockOptimizer] Initial NLL: {l_curr:.4f}")

        for cycle in range(max_cycles):
            cycle_start_l = l_curr
            x_cycle_start = np.copy(x_curr)

            # --- Block 1: Shared Baseline ---
            if len(shared_idx) > 0:
                def obj_b1(p_shared, _xc=x_curr, _si=shared_idx):
                    x_temp = np.copy(_xc)
                    x_temp[_si] = p_shared
                    return self.objective_func(x_temp)

                b1_bounds = [bounds[i] for i in shared_idx] if bounds else None
                res_b1 = minimize(obj_b1, x_curr[shared_idx], method='L-BFGS-B',
                                  bounds=b1_bounds,
                                  options={'maxiter': self.maxiter_shared, 'ftol': 1e-7, 'gtol': 1e-5})
                x_curr[shared_idx] = res_b1.x
                l_curr = res_b1.fun
                total_evals += res_b1.nfev
                total_iters += res_b1.nit

            # --- Block 2: Candidate Neighbourhood ---
            if len(cand_idx_list) > 0:
                def obj_b2(p_cand, _xc=x_curr, _ci=cand_idx_list):
                    x_temp = np.copy(_xc)
                    x_temp[_ci] = p_cand
                    return self.objective_func(x_temp)

                b2_bounds = [bounds[i] for i in cand_idx_list] if bounds else None
                res_b2 = minimize(obj_b2, x_curr[cand_idx_list], method='L-BFGS-B',
                                  bounds=b2_bounds,
                                  options={'maxiter': self.maxiter_cand, 'ftol': 1e-12, 'gtol': 1e-10})
                x_curr[cand_idx_list] = res_b2.x
                l_curr = res_b2.fun
                total_evals += res_b2.nfev
                total_iters += res_b2.nit

            # --- Block 3: Spectral Calibration (inside objective) ---
            l_curr = self.objective_func(x_curr)
            total_evals += 1

            # Check cycle convergence
            delta_l = abs(l_curr - cycle_start_l)
            rel_delta_l = delta_l / max(1.0, abs(l_curr))

            cand_param_change = 0.0
            if len(cand_idx_list) > 0:
                cand_param_change = np.max(np.abs(x_curr[cand_idx_list] - x_cycle_start[cand_idx_list]))

            grad_norm = 0.0  # Not available without Block 4

            cycle_history.append({
                'cycle': cycle + 1,
                'nll': l_curr,
                'delta_l': delta_l,
                'rel_delta_l': rel_delta_l,
                'cand_param_change': cand_param_change,
                'grad_norm': grad_norm
            })

            if verbose:
                print(f"[BlockOptimizer] Cycle {cycle+1}: NLL={l_curr:.4f}, rel_dL={rel_delta_l:.2e}, abs_dL={delta_l:.4f}")

            if rel_delta_l < self.rel_tol and delta_l < self.abs_tol and cand_param_change < 0.01:
                if verbose:
                    print(f"[BlockOptimizer] Converged at cycle {cycle+1}")
                break

        # Lightweight final polish: candidate-only refinement (not full 141-param global)
        if len(cand_idx_list) > 0:
            def obj_final(p_cand, _xc=x_curr, _ci=cand_idx_list):
                x_temp = np.copy(_xc)
                x_temp[_ci] = p_cand
                return self.objective_func(x_temp)

            b2_bounds = [bounds[i] for i in cand_idx_list] if bounds else None
            res_final = minimize(obj_final, x_curr[cand_idx_list], method='L-BFGS-B',
                                 bounds=b2_bounds,
                                 options={'maxiter': self.maxiter_cand, 'ftol': 1e-12, 'gtol': 1e-10})
            x_curr[cand_idx_list] = res_final.x
            l_final = res_final.fun
            total_evals += res_final.nfev
            total_iters += res_final.nit
            grad_final = np.linalg.norm(res_final.jac) if hasattr(res_final, 'jac') and res_final.jac is not None else 0.0
        else:
            x_final = x_curr
            l_final = l_curr
            grad_final = 0.0

        return {
            'x': x_curr,
            'fun': l_final,
            'log_likelihood': -l_final,
            'success': grad_final < self.grad_tol or delta_l < self.abs_tol,
            'message': 'converged' if delta_l < self.abs_tol else 'max_cycles',
            'nit': total_iters,
            'nfev': total_evals,
            'grad_norm': float(grad_final),
            'cycle_history': cycle_history
        }

    def run_multi_start(self, x0, bounds=None, n_starts=5, jitter_scale=0.05, verbose=False):
        results = []
        n_params = len(x0)

        for s in range(n_starts):
            if s == 0:
                x_init = np.copy(x0)
            else:
                np.random.seed(1000 + s)
                jitter = np.random.normal(0.0, jitter_scale, size=n_params)
                x_init = np.copy(x0) + jitter
                if bounds:
                    for i, (low, high) in enumerate(bounds):
                        if low is not None: x_init[i] = max(x_init[i], low)
                        if high is not None: x_init[i] = min(x_init[i], high)

            if verbose:
                print(f"\n--- Start {s+1}/{n_starts} ---")
            res = self.optimize_block_coordinate(x_init, bounds=bounds, verbose=verbose)
            results.append(res)

        nlls = [r['fun'] for r in results]
        best_idx = np.argmin(nlls)
        best_nll = nlls[best_idx]

        matching_starts = sum(1 for nll in nlls if abs(nll - best_nll) < 0.05)
        stable = matching_starts >= 3

        return {
            'best_result': results[best_idx],
            'all_results': results,
            'nlls': nlls,
            'matching_starts': matching_starts,
            'is_mode_stable': stable
        }
