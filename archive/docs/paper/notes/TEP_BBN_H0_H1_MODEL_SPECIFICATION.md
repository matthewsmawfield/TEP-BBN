# TEP-BBN H0/H1 Model Specification (Q1009)

## H0 (Conventional D I)
- **Baseline Source**: `model_6a.26`
- **D Components**: 
  - Contains exactly 3 D I subcomponents (A, B, C).
  - Velocity tied to exactly match the primary H I subcomponents A, B, and C respectively (offset by -81.6 km/s rest).
  - Doppler parameters ($b$) tied via thermal broadening relations to the corresponding H I components.
  - Column densities defined by the global D/H ratio tied to H I.
- **Interlopers**: No additional interlopers beyond those already defined in `model_6a.26`.

## H1 (Ordinary H I Kinematic)
- **Baseline Source**: `model_6a.26`
- **D Components Removed**: The 3 D I subcomponents (A, B, C) are entirely removed from the model.
- **Ordinary H I Added**: Introduced exactly **1** ordinary H I component (minimum physically coherent structure to model a localized interloper).
- **Priors and Bounds**:
  - $v$: Broadly bounded across the full non-D absorber velocity span ($\pm 100$ km/s around the absorption). It is NOT constrained to the isotope offset.
  - $\log N$: $[10, 16]$ (Lower bound effectively allows the component to vanish).
  - $b$: $[4.0, 20.0]$ km/s.

## Shared Properties
- **Shared Parameters**: All conventional interlopers, metal lines (C IV, C III, C II, Si IV), continuum parameters, zero levels, and all other H I components remain in the model with their published ties and freedom.
- **Instrumental Model**: Preserved from VPFIT regions.
- **Likelihood**: Frozen Student-t distribution derived from the baseline replay.
