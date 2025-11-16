# Optical Bloch Equations for Double-Lambda EIT

## Density Matrix Formalism

The quantum state of the three-level system is described by the density matrix **ρ**, a 3×3 Hermitian matrix with elements ρ_ij representing:
- **Diagonal elements** (ρ_11, ρ_22, ρ_ee): Populations of states |1⟩, |2⟩, |e⟩
- **Off-diagonal elements** (ρ_12, ρ_1e, ρ_2e): Coherences between states

The density matrix evolves according to the Liouville-von Neumann equation:

**iℏ ∂ρ/∂t = [H, ρ] + iℏ(∂ρ/∂t)_decay**

## Hamiltonian

The total Hamiltonian in the rotating wave approximation (RWA) is:

**H = H₀ + H_int**

### Free Hamiltonian

```
H₀ = ℏω₁|1⟩⟨1| + ℏω₂|2⟩⟨2| + ℏω_e|e⟩⟨e|
```

### Interaction Hamiltonian (RWA)

In the rotating frame, removing fast oscillating terms:

```
H_int = -ℏ(Ω_pump e^(-iω_pump t) |e⟩⟨1| + Ω_probe e^(-iω_probe t) |e⟩⟨2| + h.c.)
```

where Ω_pump and Ω_probe are the Rabi frequencies and h.c. denotes Hermitian conjugate.

## Rotating Frame Transformation

Transform to a frame rotating at the laser frequencies:
- |1⟩ rotates at ω_pump
- |2⟩ rotates at ω_probe  
- |e⟩ is the reference

Define detunings:
- **Δ_pump = ω_pump - ω_e1** (pump detuning from |1⟩→|e⟩)
- **Δ_probe = ω_probe - ω_e2** (probe detuning from |2⟩→|e⟩)
- **δ = Δ_pump - Δ_probe** (two-photon detuning)

## Optical Bloch Equations (OBEs)

The OBEs describe the evolution of density matrix elements:

### Population Equations

```
∂ρ₁₁/∂t = -iΩ_pump/2(ρ_e1 - ρ_1e) + Γ_e1 ρ_ee

∂ρ₂₂/∂t = -iΩ_probe/2(ρ_e2 - ρ_2e) + Γ_e2 ρ_ee

∂ρ_ee/∂t = iΩ_pump/2(ρ_e1 - ρ_1e) + iΩ_probe/2(ρ_e2 - ρ_2e) - Γ_e ρ_ee
```

where:
- **Γ_e1, Γ_e2**: Branching ratios for decay |e⟩→|1⟩, |e⟩→|2⟩
- **Γ_e = Γ_e1 + Γ_e2**: Total excited state decay rate

### Coherence Equations

**Optical Coherences** (ρ_1e, ρ_2e):

```
∂ρ_1e/∂t = (iΔ_pump - γ_1e)ρ_1e + iΩ_pump/2(ρ_11 - ρ_ee) + iΩ_probe/2 ρ_12

∂ρ_2e/∂t = (iΔ_probe - γ_2e)ρ_2e + iΩ_probe/2(ρ_22 - ρ_ee) + iΩ_pump/2 ρ_21
```

where γ_1e and γ_2e are dephasing rates (typically γ ≈ Γ_e/2).

**Ground-State Coherence** (ρ_12):

```
∂ρ_12/∂t = -iδ ρ_12 - γ_12 ρ_12 + iΩ_pump/2 ρ_e2 - iΩ_probe/2 ρ_e1
```

where γ_12 is the ground-state decoherence rate (often very small, ~kHz).

### Conservation

The trace of the density matrix is conserved:

**ρ₁₁ + ρ₂₂ + ρ_ee = 1**

## Steady-State Solutions

For CW (continuous wave) lasers, set time derivatives to zero. The steady-state populations and coherences depend on:
- Rabi frequencies (Ω_pump, Ω_probe)
- Detunings (Δ_pump, Δ_probe, δ)
- Decay and decoherence rates (Γ_e, γ_12)

### Weak Probe Approximation

When Ω_probe ≪ Ω_pump, we can perturbatively solve for ρ_2e:

```
ρ_2e ≈ -iΩ_probe/2 × (ρ₂₂ - ρ_ee) / [Δ_probe - iγ_2e + Ω_pump²/(4(δ - iγ_12))]
```

This shows the EIT resonance structure: the denominator has a narrow feature at δ ≈ 0 with width ~Ω_pump²/γ_12.

## Susceptibility and Absorption

### Linear Susceptibility

The probe susceptibility is proportional to the coherence:

**χ⁽¹⁾ = -N|d₂e|² ρ_2e / (ε₀ E_probe)**

where:
- N is atomic density
- d₂e is dipole moment for |2⟩↔|e⟩
- ε₀ is vacuum permittivity

### Absorption Coefficient

The absorption coefficient is:

**α = Im(χ⁽¹⁾) × ω_probe / (c n₀)**

where n₀ is background refractive index.

In the EIT window (δ ≈ 0), the absorption is dramatically reduced:

**α_EIT ≈ α₀ × (γ_12/Ω_pump)²**

### Refractive Index

The real part of susceptibility gives the refractive index:

**n - 1 ≈ Re(χ⁽¹⁾) / 2**

Near the EIT resonance, the refractive index has steep dispersion, leading to slow light:

**Group velocity: v_g = c / (1 + ω ∂n/∂ω)**

## Nonlinear Susceptibility χ⁽³⁾

For four-wave mixing and other nonlinear processes, the third-order susceptibility is:

**χ⁽³⁾ ∝ N |d|⁴ / [ε₀² ℏ³ (Δ - iγ)(δ - iγ₁₂)]**

Near two-photon resonance (δ ≈ 0) and with small ground-state decoherence, χ⁽³⁾ can be enhanced by many orders of magnitude compared to non-resonant media.

### Enhancement Factor

```
|χ⁽³⁾_EIT| / |χ⁽³⁾_off| ≈ (γ/γ₁₂)
```

Since γ ~ MHz and γ₁₂ ~ kHz, enhancement factors of 10³-10⁶ are possible.

## Numerical Solution Methods

### Time-Dependent OBEs

For pulsed or transient phenomena, solve the coupled ODEs numerically:

```python
def rhs(t, y):
    # y = [ρ₁₁, ρ₂₂, ρ_ee, Re(ρ₁₂), Im(ρ₁₂), Re(ρ_1e), Im(ρ_1e), Re(ρ_2e), Im(ρ_2e)]
    # Return time derivatives according to OBEs
    return dydt

from scipy.integrate import solve_ivp
sol = solve_ivp(rhs, t_span, y0, method='RK45')
```

### Steady-State Solutions

For CW conditions, solve the algebraic system:

```python
from scipy.optimize import fsolve

def steady_state_equations(y):
    # Set all time derivatives to zero
    return residuals

y_ss = fsolve(steady_state_equations, y0_guess)
```

## Implementation in This Package

The `DoubleLambdaSystem` class implements a simplified EIT susceptibility calculation using the weak probe approximation:

```python
def eit_susceptibility(self, probe_detuning_scan):
    gamma = self.atomic_system.total_decay_rate(self.excited_state)
    omega_pump = self.pump.rabi_frequency
    omega_probe = self.probe.rabi_frequency
    delta_pump = self.pump.detuning
    
    for delta_probe in probe_detuning_scan:
        delta_2photon = delta_pump - delta_probe
        
        denominator = (delta_probe + 1j * gamma / 2) + (
            omega_pump**2 / (4 * (delta_2photon + 1j * 1e-6))
        )
        
        susceptibility = omega_probe**2 / denominator
```

This captures the essential EIT physics:
- Lorentzian absorption profile modified by pump field
- Narrow transparency window at two-photon resonance
- Steep dispersion for slow light

## Limitations and Extensions

### Current Implementation
- Weak probe approximation (Ω_probe ≪ Ω_pump)
- Neglects Doppler broadening
- Assumes homogeneous medium
- No propagation effects (solves local OBEs)

### Possible Extensions
1. **Full OBE solver**: Include strong probe, transient dynamics
2. **Doppler effects**: Average over thermal velocity distribution
3. **Propagation**: Couple OBEs with Maxwell equations (Maxwell-Bloch)
4. **Zeeman sublevels**: Include magnetic field and all m_F states
5. **Buffer gas**: Add collisional broadening and pressure shifts

## References

### Textbooks
- Meystre, P. & Sargent, M. "Elements of Quantum Optics" (Springer, 4th ed., 2007)
- Scully, M. O. & Zubairy, M. S. "Quantum Optics" (Cambridge, 1997)
- Shore, B. W. "The Theory of Coherent Atomic Excitation" (Wiley, 1990)

### Research Papers
- Fleischhauer, M., Imamoglu, A., & Marangos, J. P. "Electromagnetically induced transparency: Optics in coherent media." *Rev. Mod. Phys.* 77, 633 (2005)
- Harris, S. E., Field, J. E., & Imamoglu, A. "Nonlinear optical processes using electromagnetically induced transparency." *Phys. Rev. Lett.* 64, 1107 (1990)
- Kash, M. M., et al. "Ultraslow group velocity and enhanced nonlinear optical effects in a coherently driven hot atomic gas." *Phys. Rev. Lett.* 82, 5229 (1999)
- Hau, L. V., Harris, S. E., Dutton, Z., & Behroozi, C. H. "Light speed reduction to 17 metres per second in an ultracold atomic gas." *Nature* 397, 594 (1999)
