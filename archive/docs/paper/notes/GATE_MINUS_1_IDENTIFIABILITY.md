# Identifiability of Proper-Time Shear in D/H Absorption Systems

## Purpose
Show what TEP predicts that ordinary H I velocity blending cannot mimic. This note serves as the controlling document before any further spectral claim.

## The Identifiability Problem
For each absorber component $i$, the observed velocity can be written as:

$$ v_{\rm obs,i} = v_{\rm kin,i} + c\delta a_i $$

where:

$$ \delta a_i = \ln A_i - \overline{\ln A} $$

The fundamental problem is that $v_{\rm kin,i}$ and $c\delta a_i$ are observationally degenerate unless $\delta a_i$ is predicted independently. Therefore, TEP-BBN must not fit $\delta a_i$ freely. It must predict:

$$ \delta a_i = \alpha g_i $$

where $g_i$ is a feature vector fixed *before* fitting the D line.

## Candidate Proper-Time Features

### Candidate A — Column-density/screening feature
Define $g_i = S(N_{{\rm HI},i})$ or $g_i = S(n_i)$, where $S$ is a TEP screening function. This is close to the Mode A pipeline, but remains weak unless the screening function is derived from TEP rather than invented.

### Candidate B — Metal-line coherence feature (Strongest)
If proper-time shear is real, the shifted component should leave correlated residual structure in metal lines (O I, Si II, C II, Fe II). Ordinary H I interlopers do not have to produce the same correlated metal-line pattern.

We define $g_i = g({\rm O\ I, Si\ II, C\ II, Fe\ II\ component\ alignment})$.

The key question is: *Does the D-like absorption occur where the TEP feature predicts a proper-time offset, and do metals show the corresponding component structure?*

### Candidate C — Multi-Lyman residual coherence
A real proper-time interpretation must fit the same component displacement across multiple Lyman transitions (Ly$\alpha$, Ly$\beta$, Ly$\gamma$, etc.) with the same $\delta a_i$.

### Candidate D — Environment / halo feature
The shear should depend on metallicity, component complexity, $N_{\rm HI}$, velocity width, and proximity to galaxy/halo if known.

## Gate -1 Pass/Fail Matrix

| Feature | Independent of D fit? | Beats velocity degeneracy? | Ready for Mode B? |
| :--- | :---: | :---: | :---: |
| Column-density feature | Partial | Weak | Not alone |
| Metal-line coherence | Yes | Stronger | Yes, if metals available |
| Multi-Lyman coherence | Yes | Medium/strong | Yes |
| Environment feature | Yes | Strong in sample | Later |
| Free $\delta a_i$ | No | No | **Reject** |

**The key rule:** A free component-level proper-time shift is not a TEP detection. It is just velocity fitting.
