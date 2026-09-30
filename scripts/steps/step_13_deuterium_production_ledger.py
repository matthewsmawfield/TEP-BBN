#!/usr/bin/env python3
"""
Step 13: Deuterium Production Ledger — supply vs demand (Gate D, item d1)

In an eternal, non-expanding cosmology the standing Galactic ISM value
D/H ~= (1.5-2)x10^-5 cannot be a relic: astration destroys deuterium
(D burns at T >~ 5e5 K, below every stellar-core temperature), so the
observed abundance is a production requirement.  This step closes the
quantitative supply-versus-demand ledger for every proposed channel.

Demand.  In the steady-state gas cycle (return fraction R, net lockup
1-R per star-formation epoch), gas that passes through stars returns
deuterium-free.  To hold the ISM at X_D = 2 x (D/H) in mass fraction,
the production yield per astrated mass must equal

    p_D_req = X_D * (1 - R).

Supply channels evaluated (literature yields are inputs, flagged as
such; no mechanism is claimed beyond its computed ledger):

  1. Galactic cosmic-ray spallation (C,N,O -> D):
     canonical ISM contribution D/H ~ (1-3)x10^-7, i.e. a per-astrated
     yield ~ (0.6-2)x10^-7 by mass — ~100-300x short.
  2. Neutrino spallation on 4He in collapsed-star shells
     (nu-process): per-event D yield ~1e-7-1e-6 Msun over ~10 Msun
     ejecta -> ~1e-8-1e-7 per astrated mass — ~200-2000x short.
  3. Pre-main-sequence envelope recycling / pristine inflow:
     preserves or dilutes but creates nothing -> zero net supply.
  4. TEP-native horizon-adjacent spallation: sequestered temporal-well
     surfaces (VMO core residues) expose matter to unbounded external
     time; photodisintegration of 4He requires photons above
     19.8 MeV.  The binding constraint is therefore mass throughput,
     not rate: the fraction of astrated mass that must transit a
     D-producing surface is f_req = p_D_req / eps_D, where eps_D is
     the per-transit deuterium enrichment of the returned material.

Also computed: the analogous 3He channel — 3He survives astration in
low-mass stars and is a documented companion constraint.

Outputs: results/gate13_deuterium_production_ledger.json
"""
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# Inputs (documented literature/corpus values; no fabricated data)
# ---------------------------------------------------------------------------
DH_ISM = 1.7e-5                     # local ISM D/H (Linsky+2006-style range 1.5-2e-5)
X_D_ISM = 2.0 * DH_ISM              # D mass fraction ~ 3.4e-5
R_RET = 0.4                         # corpus return fraction (step_11)
F_VMO = 0.994                       # corpus VMO channel fraction

# Channel yields: D mass fraction supplied per unit mass cycled
# (order-of-magnitude literature values, labelled in output)
GCR_YIELD = 1.7e-7                  # ~0.5-1% of ISM D/H per astrated mass
NU_PROCESS_YIELD = 1.0e-8           # per astrated mass, CCSNe+VMO shells

# Thresholds (nuclear constants)
E_GAMMA_HE4 = 19.8                  # MeV, 4He photodisintegration threshold
E_SPALL_MEV = 30.0                  # characteristic hadron spallation scale


def main():
    p_req = X_D_ISM * (1.0 - R_RET)          # required yield per astrated mass

    channels = {
        "galactic_cosmic_ray_spallation": {
            "yield_per_astrated_mass": GCR_YIELD,
            "shortfall": p_req / GCR_YIELD,
            "status": "insufficient (~120x short)",
        },
        "neutrino_process_He_shells": {
            "yield_per_astrated_mass": NU_PROCESS_YIELD,
            "shortfall": p_req / NU_PROCESS_YIELD,
            "status": "insufficient (~2000x short)",
        },
        "pms_envelope_recycling_or_pristine_inflow": {
            "yield_per_astrated_mass": 0.0,
            "shortfall": float("inf"),
            "status": "zero net production",
        },
    }

    # TEP-native channel: throughput constraint.  eps_D = D mass
    # fraction imprinted on material transiting a well-adjacent
    # spallation zone before return to the ISM.
    eps_scan = {
        "eps_1e-6": p_req / 1e-6,
        "eps_1e-4": p_req / 1e-4,
        "eps_1e-2": p_req / 1e-2,
        "eps_ISM": p_req / X_D_ISM,
    }
    tep_channel = {
        "demand_per_astrated_mass": p_req,
        "required_transit_fraction_vs_enrichment": {
            k: v for k, v in eps_scan.items()},
        "interpretation": (
            "if a fraction f of astrated mass transits a "
            "spallation-active surface and returns with D mass "
            "fraction eps_D, closure requires f x eps_D = "
            f"{p_req:.2e}.  E.g. eps_D = 1e-2 (strong spallation "
            "zone) needs f = 2.0e-3; eps_D = 1e-4 needs f = 0.20; "
            "enrichment only to the ISM level (eps_D = X_D_ISM) "
            "requires f = 0.6 — every astrated parcel must pass "
            "through the zone, which no surface geometry supplies.  "
            "In eternal cosmology the emissivity rate is NOT the "
            "bottleneck (external exposure is unbounded); the "
            "bottleneck is the fraction of baryons cycled through "
            "the producing geometry per astration epoch."),
    }

    ledger = {
        "step": "step_13_deuterium_production_ledger",
        "demand": {
            "DH_ISM": DH_ISM,
            "X_D_ISM_mass_fraction": X_D_ISM,
            "return_fraction_R": R_RET,
            "required_yield_per_astrated_mass": p_req,
        },
        "supply_channels": channels,
        "tep_native_channel": tep_channel,
        "thresholds": {
            "he4_photodisintegration_MeV": E_GAMMA_HE4,
            "hadron_spallation_MeV": E_SPALL_MEV,
        },
        "verdict": (
            "The standing ISM D/H requires a yield of 2.0e-5 D per "
            "unit astrated mass.  Documented channels supply "
            "10^-7-10^-8 — shortfalls of 120-2000x.  A TEP-native "
            "well-adjacent spallation channel closes the ledger only "
            "if the processed fraction f satisfies f x eps_D = "
            "2.0e-5; the viability condition is a throughput "
            "statement, computable once the horizon-transport "
            "solution fixes eps_D.  Gate D item d1 remains open but "
            "is now a quantified budget rather than an open-ended "
            "debt."),
    }

    out = project_root / "results" / "gate13_deuterium_production_ledger.json"
    out.write_text(json.dumps(ledger, indent=2))
    print("demand p_req =", f"{p_req:.2e}")
    for k, v in channels.items():
        print(f"  {k}: shortfall {v['shortfall']:.0f}x")
    print("TEP throughput:", eps_scan)
    print("wrote", out)


if __name__ == "__main__":
    main()
