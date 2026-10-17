"""Equivalent total-Doppler-width coordinates for single-isotope fits."""
import numpy as np
from scipy.optimize import minimize
from scripts.lib.doppler_physics import KB_OVER_MP,compute_doppler_b

def minimize_width(objective, x0, bounds, isotope, **kwargs):
    """Remove the unidentifiable T/b_turb direction, preserving its entire
    allowed total-width interval. Remaining scaffold variables are untouched.
    The returned x uses the original parameter layout and one allowed T/b split.
    This is a likelihood coordinate change, not a temperature measurement.
    """
    t_index = 1 if isotope == 'D' else 2
    b_index = t_index+1
    coefficient = KB_OVER_MP * (1 if isotope == 'D' else 2)
    t_min,t_max = bounds[t_index]
    b_min,b_max = bounds[b_index]
    if t_min<0 or b_min<0:raise ValueError('Require nonnegative thermal/turbulent bounds')
    width_min = np.sqrt(b_min*b_min+coefficient*t_min)
    width_max = np.sqrt(b_max*b_max+coefficient*t_max)
    q0 = np.r_[x0[:t_index],compute_doppler_b(x0[t_index],x0[b_index],isotope),x0[b_index+1:]]
    qbounds = list(bounds[:t_index])+[(width_min,width_max)]+list(bounds[b_index+1:])
    def expand(q):
        width = q[t_index]
        temperature = np.clip((width*width-b_min*b_min)/coefficient,t_min,t_max)
        turbulent = np.sqrt(max(b_min*b_min,width*width-coefficient*temperature))
        turbulent = np.clip(turbulent,b_min,b_max)
        return np.r_[q[:t_index],temperature,turbulent,q[t_index+1:]]
    kwargs.setdefault("jac","3-point")
    result = minimize(lambda q:objective(expand(q)),q0,bounds=qbounds,**kwargs)
    result.x_width_coordinates = result.x.copy()
    result.x = expand(result.x)
    return result

def hydrogen_start_from_deuterium(d_params,velocity,h_bounds):
    """Map the fitted D profile and scaffold to an allowed identical H profile.
    Returns None if the H bounds do not contain that width or velocity."""
    width=compute_doppler_b(d_params[1],d_params[2],'D')
    t_min,t_max=h_bounds[2];b_min,b_max=h_bounds[3]
    if not h_bounds[0][0]<=velocity<=h_bounds[0][1]:return None
    if not b_min*b_min+2*KB_OVER_MP*t_min<=width*width<=b_max*b_max+2*KB_OVER_MP*t_max:return None
    temperature=np.clip((width*width-b_min*b_min)/(2*KB_OVER_MP),t_min,t_max)
    turbulent=np.sqrt(max(b_min*b_min,width*width-2*KB_OVER_MP*temperature))
    return np.r_[velocity,d_params[0],temperature,turbulent,d_params[3:]]
