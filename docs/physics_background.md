# Physics Background: Double-Lambda EIT System

## Introduction to Electromagnetically Induced Transparency (EIT)

Electromagnetically Induced Transparency (EIT) is a quantum interference effect that renders an otherwise opaque medium transparent to a weak probe laser by applying a strong coupling laser. This phenomenon arises from quantum coherence between atomic states and has profound implications for slow light, quantum memory, and nonlinear optics.

## The Double-Lambda Configuration

### Energy Level Structure

The double-lambda (or double-Λ) configuration involves:
- **Two ground states**: |1⟩ and |2⟩ (typically different hyperfine levels of the same electronic ground state)
- **One excited state**: |e⟩ (an electronic excited state)
- **Two optical transitions**: |1⟩ ↔ |e⟩ and |2⟩ ↔ |e⟩

```
        |e⟩ (5P_3/2, F')
         /\
        /  \
  Pump /    \ Probe
      /      \
     /        \
   |1⟩       |2⟩
(5S_1/2, F) (5S_1/2, F')
```

### Why Rubidium?

Rubidium (Rb) is an alkali metal ideal for EIT experiments due to:

1. **Accessible D-lines**: The D1 (795 nm) and D2 (780 nm) transitions are easily accessible with commercial diode lasers
2. **Simple electronic structure**: Single valence electron provides clean level structure
3. **Well-characterized parameters**: Comprehensive spectroscopic data available
4. **Two stable isotopes**: ⁸⁷Rb (I=3/2) and ⁸⁵Rb (I=5/2) offer different hyperfine structures

### Hyperfine Structure

The nuclear spin **I** couples with the electronic angular momentum **J** to produce total angular momentum **F**:

**F = J + I**

For ⁸⁷Rb (I = 3/2):
- Ground state 5S₁/₂ (J=1/2): F = 1, 2
- Excited state 5P₃/₂ (J=3/2): F' = 0, 1, 2, 3

For ⁸⁵Rb (I = 5/2):
- Ground state 5S₁/₂ (J=1/2): F = 2, 3
- Excited state 5P₃/₂ (J=3/2): F' = 1, 2, 3, 4

## EIT Physics

### Quantum Coherence

In the double-lambda configuration, the pump and probe lasers create a coherent superposition of the two ground states. This ground-state coherence interferes destructively with the excited state probability amplitude, preventing absorption of the probe beam.

### Dark States

Under two-photon resonance (Δ_pump - Δ_probe ≈ 0), the system evolves into a "dark state"—a coherent superposition of |1⟩ and |2⟩ that does not couple to the excited state:

|Dark⟩ = (Ω_probe |1⟩ - Ω_pump |2⟩) / √(Ω_pump² + Ω_probe²)

where Ω_pump and Ω_probe are the Rabi frequencies of the pump and probe fields.

### EIT Window

The transparency window has width proportional to the pump Rabi frequency:

**Transparency Width ≈ Ω_pump² / γ**

where γ is the excited state decay rate.

### Slow Light

Inside the EIT window, the group velocity of light is dramatically reduced:

**v_g ≈ (Ω_pump² / (N |d|² ω / ε₀ ℏ)) c**

where:
- N is atomic density
- d is transition dipole moment
- ω is optical frequency
- c is speed of light in vacuum

This can reduce light speed to meters per second or even stop light completely.

## Selection Rules

Dipole transitions must obey selection rules:
- **ΔL = ±1**: Electric dipole transitions change orbital angular momentum by ±1
- **ΔJ = 0, ±1** (but J=0 ↔ J'=0 forbidden)
- **ΔF = 0, ±1** (but F=0 ↔ F'=0 forbidden)
- **Δm_F = 0, ±1**: Depends on light polarization
  - Δm_F = 0 for π-polarized light (linear)
  - Δm_F = ±1 for σ± circularly polarized light

## Key Parameters

### Rabi Frequency

The Rabi frequency characterizes the strength of atom-light coupling:

**Ω = -⟨g|d·E|e⟩ / ℏ = d·E₀ / ℏ**

where:
- d is the transition dipole moment
- E₀ is the electric field amplitude

Typical values: 1-100 MHz for EIT experiments

### Detuning

The detuning Δ is the difference between laser frequency and atomic resonance:

**Δ = ω_laser - ω_atomic**

### Two-Photon Detuning

For double-lambda EIT, the critical parameter is the two-photon detuning:

**δ = Δ_pump - Δ_probe**

Maximum transparency occurs at δ ≈ 0 (two-photon resonance).

### Decay Rate

Natural linewidth of excited state:

**γ = 1/τ = 2π × 6.065 MHz** for Rb D-lines

where τ ≈ 26 ns is the excited state lifetime.

## Applications

1. **Quantum Memory**: Store and retrieve quantum states of light
2. **Nonlinear Optics**: Enhance χ⁽³⁾ susceptibility for four-wave mixing
3. **Precision Metrology**: Narrow resonances for atomic clocks
4. **Quantum Information**: Generate entanglement and single photons
5. **Optical Switching**: All-optical control of light propagation

## References

### Key EIT Papers
- Harris, S. E. "Electromagnetically Induced Transparency." *Physics Today* 50(7), 36 (1997)
- Fleischhauer, M., Imamoglu, A., & Marangos, J. P. "Electromagnetically induced transparency: Optics in coherent media." *Rev. Mod. Phys.* 77, 633 (2005)
- Lukin, M. D. "Colloquium: Trapping and manipulating photon states in atomic ensembles." *Rev. Mod. Phys.* 75, 457 (2003)

### Rubidium Spectroscopy
- Steck, D. A. "Rubidium 87 D Line Data" (revision 2.2.2, 2021) http://steck.us/alkalidata
- Steck, D. A. "Rubidium 85 D Line Data" (revision 2.2.2, 2021) http://steck.us/alkalidata
- Arimondo, E. "Coherent Population Trapping in Laser Spectroscopy." *Progress in Optics* 35, 257 (1996)
