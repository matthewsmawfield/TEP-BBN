"""Exact component cache respecting the full forward model's transition mask."""
from collections import OrderedDict
import numpy as np
from scipy.special import wofz
from scripts.lib.physical_rt_engine import c_kms,sigma_0
from scripts.lib.residual_engine import build_frozen_cache,compute_residuals_fast,_LYMAN

class ComponentCache:
    def __init__(self,engine):
        self.engine=engine;self.profiles=OrderedDict();self.full=None
    def __getattr__(self,name):return getattr(self.engine,name)
    def admitted(self,wave,name,components):
        if not components:return False
        tc=self.engine._get_transition_constants(name)
        velocities=[v['v'] for v in components];widths=[v['b'] for v in components]
        low=tc['lam_obs_center']*(1+min(velocities)/c_kms)
        high=tc['lam_obs_center']*(1+max(velocities)/c_kms)
        margin=max(low,high)*max(100*max(widths),5000)/c_kms
        return not(high+margin<wave[0] or low-margin>wave[-1])
    def profile(self,wave,name,component):
        key=(id(wave),name,float(component['v']),float(component['b']))
        if key in self.profiles:
            self.profiles.move_to_end(key);return self.profiles[key]
        tc=self.engine._get_transition_constants(name);width=component['b'];b_cgs=width*1e5
        center=tc['lam_obs_center']*(1+component['v']/c_kms)
        x=(c_kms*(wave-center)/center)/width
        damping=tc['gamma']*tc['lam_rest_cm']/(4*np.pi*b_cgs)
        value=(tc['f_osc']*tc['lam_rest_cm']*sigma_0/b_cgs)*wofz(x+1j*damping).real
        self.profiles[key]=value
        if len(self.profiles)>4096:self.profiles.popitem(last=False)
        return value
    def compute_optical_depth(self,wave,transitions,components):
        # The isotope caller uses the shared HI transitions. Identify the full
        # group through the evaluate() context rather than the variable subset.
        full=self.active_group
        total=np.zeros_like(wave)
        for name in transitions:
            if self.admitted(wave,name,full):
                total+=sum((v['N']*self.profile(wave,name,v) for v in components),np.zeros_like(wave))
        return total

def scaffold_evaluator(original,mutable,blocks,engine):
    """Cache fixed profiles separately per transition. Dynamic masks use all
    components, including fixed ones, exactly as compute_residuals does.
    """
    proxy=ComponentCache(engine)
    fixed={ion:[v for i,v in enumerate(values) if i not in mutable[ion]] for ion,values in original.items()}
    metals={ion:([] if ion in ['H_I','D_I'] else values) for ion,values in fixed.items()}
    base=build_frozen_cache(metals,blocks,engine)
    for cache in base:
        cache["x_norm_powers"]=np.column_stack([cache["x_norm"]**k for k in range(cache["n_cont"]-1)])
    fixed_tau=[]
    for block in blocks:
        wave=block['wave'];per_ion={}
        for ion in ['H_I','D_I']:
            per_ion[ion]={name:sum((v['N']*proxy.profile(wave,name,v) for v in fixed[ion]),np.zeros_like(wave)) for name in _LYMAN}
        fixed_tau.append(per_ion)
    class IsotopeProxy:
        def __getattr__(self,name):return getattr(engine,name)
        def compute_optical_depth(self,wave,transitions,components):
            # residual_engine calls H then D when each candidate group exists.
            ion=call_order.pop(0);proxy.active_group=current[ion]
            return proxy.compute_optical_depth(wave,transitions,components)
    wrapped=IsotopeProxy()
    def evaluate(grouped,data):
        nonlocal current,call_order
        current=grouped
        candidate={ion:[grouped[ion][i] for i in mutable[ion]]+grouped[ion][len(original[ion]):] for ion in ['H_I','D_I']}
        caches=[];call_order=[]
        for block,cache,per_ion in zip(blocks,base,fixed_tau):
            tau=cache['tau_frozen'].copy()
            for ion in ['H_I','D_I']:
                for name in _LYMAN:
                    if proxy.admitted(block['wave'],name,grouped[ion]):tau+=per_ion[ion][name]
                if candidate[ion]:call_order.append(ion)
            caches.append(dict(cache,tau_frozen=tau))
        return stable_residuals(candidate,data,wrapped,caches)
    current=None;call_order=[]
    return evaluate


def stable_residuals(candidate,blocks,engine,caches):
    """Solve the same weighted ridge continuum via an augmented least-squares
    system, avoiding the squared condition number of normal equations."""
    residuals=[]
    for block,cache in zip(blocks,caches):
        wave=block['wave'];tau=cache['tau_frozen'].copy()
        for ion in ['H_I','D_I']:
            if candidate[ion]:tau+=engine.compute_optical_depth(wave,_LYMAN,candidate[ion])
        transmission=np.maximum(np.exp(-tau),1e-300)
        basis=np.column_stack([engine.apply_convolution(cache['x_norm']**k*transmission,wave,block['vsig']) for k in range(cache['n_cont']-1)]+[np.ones_like(wave)])
        inv_error=1/np.maximum(block['err'],1e-10)
        system=np.vstack([basis*inv_error[:,None],1e-5*np.eye(cache['n_cont'])])
        target=np.r_[block['flux']*inv_error,np.zeros(cache['n_cont'])]
        try:
            coefficients=np.linalg.lstsq(system,target,rcond=None)[0]
            res=(block['flux']-basis@coefficients)*inv_error
            if not np.all(np.isfinite(res)):res=np.full_like(wave,np.inf)
        except np.linalg.LinAlgError:res=np.full_like(wave,np.inf)
        residuals.append(res)
    return np.concatenate(residuals)
