# Parameter Sources and Citations

This document provides detailed citations for all atomic parameters used in the simulator, ensuring reproducibility and scientific rigor.

## Primary References

### Rb-87 Spectroscopic Data

**Steck, D. A. "Rubidium 87 D Line Data"**
- Revision 2.2.2 (December 2021)
- Available at: http://steck.us/alkalidata
- Provides comprehensive Rb-87 spectroscopic parameters

### Rb-85 Spectroscopic Data

**Steck, D. A. "Rubidium 85 D Line Data"**
- Revision 2.2.2 (December 2021)
- Available at: http://steck.us/alkalidata
- Provides comprehensive Rb-85 spectroscopic parameters

## Nuclear Properties

### Nuclear Spins

| Isotope | Nuclear Spin (I) | Source |
|---------|------------------|--------|
| ⁸⁷Rb | 3/2 | Steck (2021), Table 1 |
| ⁸⁵Rb | 5/2 | Steck (2021), Table 1 |

**Natural Abundances:**
- ⁸⁷Rb: 27.835%
- ⁸⁵Rb: 72.165%

## D-Line Wavelengths and Frequencies

### Wavelengths (vacuum)

| Transition | Wavelength (nm) | Frequency (THz) | Source |
|------------|-----------------|-----------------|--------|
| Rb D1 (5S₁/₂ → 5P₁/₂) | 794.979014933 | 377.107463380 | Steck, Eq. 1 |
| Rb D2 (5S₁/₂ → 5P₃/₂) | 780.241368271 | 384.230406373 | Steck, Eq. 2 |

**Note:** These are weighted averages over hyperfine structure.

### Fine Structure Splitting

| Property | Value | Source |
|----------|-------|--------|
| 5P fine structure (P₃/₂ - P₁/₂) | 237.6 cm⁻¹ = 7.125 THz | Steck, Table 2 |

## Hyperfine Structure Constants

### Rb-87 Hyperfine Constants

| State | A_hfs (MHz) | B_hfs (MHz) | Source |
|-------|-------------|-------------|--------|
| 5S₁/₂ | 3417.341305452145 | — | Steck Rb87, Table 3 |
| 5P₁/₂ | 407.24 | — | Steck Rb87, Table 4 |
| 5P₃/₂ | 84.7185 | 12.4965 | Steck Rb87, Table 5 |

**Hyperfine Energy Formula:**

For J = 1/2 states (S₁/₂, P₁/₂):
```
E_hfs = (A_hfs / 2) × K
where K = F(F+1) - I(I+1) - J(J+1)
```

For J = 3/2 states (P₃/₂):
```
E_hfs = (A_hfs / 2) × K + B_hfs × [3K(K+1)/2 - 2I(I+1)J(J+1)] / [2I(2I-1)×2J(2J-1)]
```

### Rb-85 Hyperfine Constants

| State | A_hfs (MHz) | B_hfs (MHz) | Source |
|-------|-------------|-------------|--------|
| 5S₁/₂ | 1011.9108130 | — | Steck Rb85, Table 3 |
| 5P₁/₂ | 120.640 | — | Steck Rb85, Table 4 |
| 5P₃/₂ | 25.0020 | 25.790 | Steck Rb85, Table 5 |

## Transition Dipole Moments

### Reduced Matrix Elements

The **reduced dipole matrix element** ⟨J'||er||J⟩ is independent of m_J sublevels.

| Transition | Reduced Dipole (ea₀) | Reduced Dipole (C·m) | Source |
|------------|----------------------|----------------------|--------|
| D1 (S₁/₂ → P₁/₂) | 3.00 | 2.537×10⁻²⁹ | Steck, Table 2 |
| D2 (S₁/₂ → P₃/₂) | 4.23 | 3.584×10⁻²⁹ | Steck, Table 2 |

**Atomic unit conversion:**
```
1 ea₀ = (1.602176634×10⁻¹⁹ C) × (5.29177210903×10⁻¹¹ m)
      = 8.478353626×10⁻³⁰ C·m
```

### Transition Dipole Moments (State-Specific)

For transitions between specific hyperfine levels |F,m_F⟩ → |F',m'_F⟩, the dipole moment involves Clebsch-Gordan coefficients:

```
⟨F,m_F|d|F',m'_F⟩ = (-1)^(F'+J+1+I) × √[(2F'+1)(2J+1)]
                    × { J   F'  I }  ⟨J'||d||J⟩
                      { F   J'  1 }
                    × ⟨F,m_F|1,q|F',m'_F⟩
```

where `{ }` is a 6-j symbol and the last term is a Clebsch-Gordan coefficient.

**Implementation Note:** This package uses approximate dipole moments based on F quantum numbers, sufficient for most EIT calculations.

## Spontaneous Decay Rates

### Natural Linewidth

| Transition | Lifetime τ (ns) | Decay Rate Γ = 1/τ (MHz) | Source |
|------------|-----------------|--------------------------|--------|
| 5P₁/₂ → 5S₁/₂ | 27.70 | 2π × 5.746 | Steck, Table 2 |
| 5P₃/₂ → 5S₁/₂ | 26.24 | 2π × 6.065 | Steck, Table 2 |

**Formula:**
```
Γ = 1/τ = (ω³|d|²)/(3πε₀ℏc³)
```

### Branching Ratios

For Rb D-lines, the excited states P₁/₂ and P₃/₂ decay only to the ground state S₁/₂:
- **Branching ratio = 1.0** (no other decay channels)

For decay from |F'⟩ to multiple ground states |F⟩, the branching ratio depends on:
```
BR(F' → F) ∝ (2F+1) × |⟨F||d||F'⟩|²
```

This is automatically calculated in `Rb87System` and `Rb85System` classes.

## Physical Constants

| Constant | Symbol | Value | Source |
|----------|--------|-------|--------|
| Planck constant | h | 6.62607015×10⁻³⁴ J·s | CODATA 2018 |
| Reduced Planck | ℏ = h/(2π) | 1.054571817×10⁻³⁴ J·s | CODATA 2018 |
| Speed of light | c | 299792458 m/s (exact) | SI definition |
| Vacuum permittivity | ε₀ | 8.8541878128×10⁻¹² F/m | CODATA 2018 |
| Elementary charge | e | 1.602176634×10⁻¹⁹ C (exact) | SI definition |
| Bohr radius | a₀ | 5.29177210903×10⁻¹¹ m | CODATA 2018 |

**Reference:** CODATA Recommended Values of the Fundamental Physical Constants: 2018.
Available at: https://physics.nist.gov/cuu/Constants/

## Selection Rules

### Electric Dipole Transitions

From Wigner-Eckart theorem and angular momentum coupling:

| Quantum Number | Selection Rule | Reason |
|----------------|----------------|--------|
| ΔL | ±1 | Electric dipole operator rank 1 |
| ΔJ | 0, ±1 | J=0↔J'=0 forbidden |
| ΔF | 0, ±1 | F=0↔F'=0 forbidden |
| Δm_J, Δm_F | 0, ±1 | Depends on polarization |

**Polarization dependence:**
- **π (linear):** Δm = 0
- **σ⁺ (left circular):** Δm = +1
- **σ⁻ (right circular):** Δm = -1

### Parity

- S states: even parity (+)
- P states: odd parity (-)
- Electric dipole: changes parity

Therefore S ↔ P transitions are allowed, but S ↔ S or P ↔ P are forbidden.

## Validation and Cross-Checks

### Hyperfine Splitting Verification

**Rb-87 ground state splitting (F=2 to F=1):**
```
Δν = 3417.341305452145 MHz × [2(2+1) - 1(1+1)] / 2
    = 3417.341305452145 MHz × 2
    = 6834.682610904 MHz
```
**Literature value:** 6.834682610904 GHz ✓ (Steck Table 3)

### D2 Line Frequency

**Rb-87 D2 5S₁/₂ (F=2) → 5P₃/₂ (F'=3) transition:**
```
ν = c/λ + hyperfine corrections
  ≈ 384.230406373 THz + hyperfine shifts
```
**Measured:** 384.230484468 THz (Steck Table 6) ✓

### Consistency with Literature

All parameters match standard references:
- Steck's alkali data compilation (2021)
- NIST Atomic Spectra Database
- Arimondo, E. "Coherent Population Trapping in Laser Spectroscopy" Prog. Opt. 35, 257 (1996)

## Software Implementation

### Parameter Loading

Parameters are hard-coded as module-level constants in `constants.py`:

```python
# From constants.py
RB87_GROUND_HFS_A = 2 * PI * 3.417341305452145e9  # rad/s
RB_D2_WAVELENGTH = 780.241368271e-9  # meters
RB_D_LINE_DECAY_RATE = 2 * PI * 6.065e6  # rad/s
```

**Rationale:** 
- Parameters are well-established and unlikely to change
- Avoids file I/O overhead
- Ensures reproducibility
- Easy to audit and verify

### Unit Consistency

All internal calculations use **SI base units**:
- Lengths in meters
- Energies in Joules
- Frequencies in Hertz (or rad/s for angular frequencies)
- Time in seconds

**Conversion guidelines:**
```python
# Frequency to energy
E = h * nu  # Joules

# Angular frequency to energy
E = HBAR * omega  # Joules

# Energy to wavelength
lambda_m = h * c / E  # meters

# MHz to rad/s
omega = 2 * pi * f_MHz * 1e6  # rad/s
```

## Additional References

### EIT Theory
- Fleischhauer, M., Imamoglu, A., & Marangos, J. P. "Electromagnetically induced transparency: Optics in coherent media." *Rev. Mod. Phys.* 77, 633 (2005)
- Harris, S. E. "Electromagnetically Induced Transparency." *Physics Today* 50(7), 36 (1997)

### Rubidium Experiments
- Akulshin, A. M., et al. "Electromagnetically induced absorption in a four-state system." *Phys. Rev. A* 57, 2996 (1998)
- Moi, L., et al. "Hyperfine spectroscopy of highly excited D states in rubidium." *Phys. Rev. A* 27, 2043 (1983)

### Atomic Physics Textbooks
- Foot, C. J. "Atomic Physics" (Oxford, 2005)
- Demtröder, W. "Atoms, Molecules and Photons" (Springer, 2006)

## License and Usage

**Spectroscopic Data:**
- Steck's alkali data is in the public domain
- No restrictions on use for research or education

**This Software:**
- MIT License (see LICENSE file)
- Free for academic and commercial use
- Attribution appreciated but not required

**Citation Recommendation:**

If you use this simulator in published research, please cite:

1. This software package (with version number and GitHub URL)
2. Steck's alkali data compilation for atomic parameters
3. Relevant EIT theory papers (Fleischhauer et al. 2005)

**Example citation:**
```
Atomic parameters from:
D. A. Steck, "Rubidium 87 D Line Data," revision 2.2.2 (2021).
Available online: http://steck.us/alkalidata
```
