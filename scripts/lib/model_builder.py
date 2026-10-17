from scripts.lib.doppler_physics import compute_doppler_b


def build_model_components(model_name, theta_shared, theta_cand, pm, z_abs_ref, c_kms,
                           d_velocity_offset_kms, parent_idx='auto',
                           parent_window_kms=1000.0):
    """
    Constructs the exact grouped components dictionary for RadiativeTransferEngine
    under one of the 7 formal model hypotheses:
      - 'M_NULL': D-free scaffold (H I + metals only, no candidate component).
      - 'M_D6a': Published model-6a D architecture (frozen D at isotope offset).
      - 'M_Drefit': Refitted model-6a D architecture.
      - 'M_Dfree': Matched-flexibility D component (v tied to parent H_j,
        free N_D, T, b_turb).
      - 'M_H' (alias 'M_Hfree'): Ordinary H interloper (free v_H, N_H, T, b_turb).
      - 'M_kinematic': Pure kinematic shift (free v, N; b inherited from parent).
      - 'M_D+H': Physical D candidate plus an ordinary H interloper.

    parent_idx: index of the H I component to use as the D parent.
        If 'auto' (default), automatically detects the H I component with
        the highest logN that has a D counterpart in the VPFIT model
        (matched by redshift).  This ensures the candidate D is placed at
        the velocity of the strongest D feature.

    d_velocity_offset_kms: velocity offset of D from parent H in km/s.
        Must be passed from the sightline config (cfg["d_velocity_offset_kms"]).
        The standard value is -81.6 km/s (Cooke et al. 2018).

    parent_window_kms: window for parent reassignment eligibility.
        Used by step_03 to filter eligible parents externally; not used
        inside this function (the auto-detection always picks the strongest
        D-parent regardless of velocity window).
    """
    # Accept M_Hfree as an alias for M_H
    if model_name == 'M_Hfree':
        model_name = 'M_H'

    comps = pm.reconstruct(theta_shared)
    grouped = {'H_I': [], 'D_I': [], 'C_IV': [], 'C_III': [], 'C_II': [], 'Si_IV': []}

    # Auto-detect parent_idx: among H I components that have a D counterpart
    # in the VPFIT model (matched by redshift), pick the one with the highest
    # logN_H.  This ensures the candidate D component is placed at the velocity
    # of the strongest D feature, maximising detectability.  Using the first
    # parent can select a weak component (e.g. J1332 parent A at logN_H=16.68
    # vs parent B at logN_H=19.25), placing D at the wrong velocity and making
    # the D absorption undetectable.
    if parent_idx == 'auto':
        d_zs = set()
        for c in comps:
            if c['ion'] == 'D_I':
                d_zs.add(round(c['z'], 10))
        parent_idx = 0
        h_count = 0
        best_logN = float('-inf')
        for c in comps:
            if c['ion'] == 'H_I':
                if round(c['z'], 10) in d_zs:
                    if c['logN'] > best_logN:
                        best_logN = c['logN']
                        parent_idx = h_count
                h_count += 1

    parent_h_v = 0.0
    parent_count = 0

    for c in comps:
        v = c_kms * (c['z'] - z_abs_ref) / (1.0 + z_abs_ref)
        cd = {'N': 10**c['logN'], 'b': c['b'], 'v': v}

        if c['ion'] == 'H_I':
            if parent_count == parent_idx:
                parent_h_v = v
            parent_count += 1
            grouped['H_I'].append(cd)
        elif c['ion'] == 'D_I':
            if model_name in ['M_D6a', 'M_Drefit']:
                cd['v'] += d_velocity_offset_kms
                grouped['D_I'].append(cd)
            # For other models, candidate D components from published model_6a are handled separately
        elif c['ion'] in grouped:
            grouped[c['ion']].append(cd)

    if model_name in ['M_NULL', 'M_D6a', 'M_Drefit']:
        pass

    elif model_name == 'M_Dfree':
        # Candidate D component tied to parent H_j
        if theta_cand is not None and len(theta_cand) >= 3:
            logN_D, T_K, b_turb = theta_cand[:3]
            b_D = compute_doppler_b(T_K, b_turb, isotope='D')
            v_D = parent_h_v + d_velocity_offset_kms
            grouped['D_I'].append({'v': v_D, 'N': 10**logN_D, 'b': b_D})

    elif model_name == 'M_H':
        # Ordinary H component with free velocity v_H
        if theta_cand is not None and len(theta_cand) >= 4:
            v_H, logN_H, T_K, b_turb = theta_cand[:4]
            b_H = compute_doppler_b(T_K, b_turb, isotope='H')
            grouped['H_I'].append({'v': v_H, 'N': 10**logN_H, 'b': b_H})

    elif model_name == 'M_kinematic':
        # Pure kinematic shift: free velocity and column density,
        # but b-value inherited from parent H I (no mass scaling, no free b).
        # Tests whether a pure velocity offset without isotope physics
        # can explain the candidate feature.
        if theta_cand is not None and len(theta_cand) >= 2:
            v_H, logN_H = theta_cand[:2]
            # Find the parent component's b from the shared scaffold
            b_parent = 0.0
            h_count = 0
            for c in comps:
                if c['ion'] == 'H_I':
                    if h_count == parent_idx:
                        b_parent = c['b']
                        break
                    h_count += 1
            grouped['H_I'].append({'v': v_H, 'N': 10**logN_H, 'b': b_parent})

    elif model_name == 'M_D+H':
        # Physical D component + ordinary H interloper
        if theta_cand is not None and len(theta_cand) >= 5:
            logN_D, v_H, logN_H, T_K, b_turb = theta_cand[:5]
            b_D = compute_doppler_b(T_K, b_turb, isotope='D')
            b_H = compute_doppler_b(T_K, b_turb, isotope='H')
            v_D = parent_h_v + d_velocity_offset_kms
            grouped['D_I'].append({'v': v_D, 'N': 10**logN_D, 'b': b_D})
            grouped['H_I'].append({'v': v_H, 'N': 10**logN_H, 'b': b_H})

    else:
        raise ValueError(
            f"Unknown model_name '{model_name}'. "
            f"Expected one of: M_NULL, M_D6a, M_Drefit, M_Dfree, M_H, "
            f"M_Hfree, M_kinematic, M_D+H."
        )

    return grouped
