import numpy as np
from scripts.lib.doppler_physics import compute_doppler_b

def build_model_components(model_name, theta_shared, theta_cand, pm, z_abs_ref, c_kms, parent_idx=0):
    """
    Constructs the exact grouped components dictionary for RadiativeTransferEngine 
    under one of the 6 formal model hypotheses:
      - 'M_NULL': No candidate D or replacement H component.
      - 'M_D6a': Published model-6a D architecture.
      - 'M_Drefit': Refitted model-6a D architecture.
      - 'M_Dfree': Matched-flexibility D component (v tied to parent H_j, free N_D, T, b_turb).
      - 'M_H': Ordinary H interloper (free v_H, N_H, T, b_turb).
      - 'M_D+H': Physical D candidate plus an ordinary H interloper.
    """
    comps = pm.reconstruct(theta_shared)
    grouped = {'H_I': [], 'D_I': [], 'C_IV': [], 'C_III': [], 'C_II': [], 'Si_IV': []}
    
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
                cd['v'] -= 81.6
                grouped['D_I'].append(cd)
            # For other models, candidate D components from published model_6a are handled separately
        elif c['ion'] in grouped:
            grouped[c['ion']].append(cd)
            
    if model_name in ['M_NULL', 'M_D6a', 'M_Drefit']:
        pass
        
    elif model_name == 'M_Dfree':
        # Candidate D component tied to parent H_j: v_D = v_parent - 81.6
        if theta_cand is not None and len(theta_cand) >= 3:
            logN_D, T_K, b_turb = theta_cand[:3]
            b_D = compute_doppler_b(T_K, b_turb, isotope='D')
            v_D = parent_h_v - 81.6
            grouped['D_I'].append({'v': v_D, 'N': 10**logN_D, 'b': b_D})
            
    elif model_name == 'M_H':
        # Ordinary H component with free velocity v_H
        if theta_cand is not None and len(theta_cand) >= 4:
            v_H, logN_H, T_K, b_turb = theta_cand[:4]
            b_H = compute_doppler_b(T_K, b_turb, isotope='H')
            grouped['H_I'].append({'v': v_H, 'N': 10**logN_H, 'b': b_H})
            
    elif model_name == 'M_D+H':
        # Physical D component + ordinary H interloper
        if theta_cand is not None and len(theta_cand) >= 5:
            logN_D, v_H, logN_H, T_K, b_turb = theta_cand[:5]
            b_D = compute_doppler_b(T_K, b_turb, isotope='D')
            b_H = compute_doppler_b(T_K, b_turb, isotope='H')
            v_D = parent_h_v - 81.6
            grouped['D_I'].append({'v': v_D, 'N': 10**logN_D, 'b': b_D})
            grouped['H_I'].append({'v': v_H, 'N': 10**logN_H, 'b': b_H})
            
    return grouped
