# Optical Bloch Equation Solver

This module implements optical Bloch equation solvers for computing steady-state density matrices of atomic systems under laser driving.

## Features

- **TwoLevelBlochSolver**: Analytical solver for two-level atoms with exact steady-state solutions
- **BlochSolver**: Numerical solver for three-level double-lambda EIT systems
- **Probe Detuning Sweeps**: Compute density matrices across a range of probe detunings
- **Susceptibility Calculations**: Calculate absorption and dispersion from density matrix coherences
- **Physical Validation**: Automatic checks for Hermiticity, trace normalization, and positive semidefiniteness

## Usage

### Two-Level System

```python
from rb_eit import TwoLevelBlochSolver
import numpy as np

# Create solver
solver = TwoLevelBlochSolver(
    rabi_frequency=2 * np.pi * 10e6,  # 10 MHz
    detuning=0.0,  # Resonant
    decay_rate=2 * np.pi * 6e6  # 6 MHz
)

# Solve for steady state
rho = solver.solve_steady_state()

# Validate density matrix
validation = solver.validate_density_matrix(rho)
print(f"Valid: {validation['valid']}")
```

### Three-Level Double-Lambda System

```python
from rb_eit import DoubleLambdaSystem, BlochSolver
import numpy as np

# Create double-lambda system
system = DoubleLambdaSystem(
    isotope="Rb87",
    pump_rabi_frequency=2 * np.pi * 10e6,
    probe_rabi_frequency=2 * np.pi * 1e6,
    pump_detuning=0.0,
    probe_detuning=0.0
)

# Create solver
solver = BlochSolver(system)

# Solve for steady state
rho = solver.solve_steady_state()

print(f"Ground state 1 population: {rho[0, 0].real:.4f}")
print(f"Ground state 2 population: {rho[1, 1].real:.4f}")
print(f"Excited state population: {rho[2, 2].real:.4f}")
```

### Probe Detuning Sweep

```python
import numpy as np

# Define detuning range (-30 to +30 MHz)
detuning_range = np.linspace(-30e6, 30e6, 100) * 2 * np.pi

# Sweep probe detuning
density_matrices, coherences = solver.sweep_probe_detuning(detuning_range)

# coherences[i] contains rho_23 (probe-excited coherence) at detuning_range[i]
# density_matrices[i] is the full 3x3 density matrix
```

### Susceptibility Calculation

```python
# Calculate absorption and dispersion
atom_density = 1e17  # atoms/m^3
absorption, dispersion = solver.compute_susceptibility(
    detuning_range,
    atom_density=atom_density
)

# absorption and dispersion are real arrays corresponding to detuning_range
```

## Implementation Details

### Optical Bloch Equations

The solver implements the optical Bloch equations for a three-level lambda system:

- **Level |1⟩**: Ground state 1
- **Level |2⟩**: Ground state 2  
- **Level |e⟩**: Excited state

The pump field couples |1⟩ ↔ |e⟩ with Rabi frequency Ω_p and detuning Δ_p.
The probe field couples |2⟩ ↔ |e⟩ with Rabi frequency Ω_c and detuning Δ_c.

The equations of motion for the density matrix elements are:

```
dρ₁₁/dt = Γₑ₁ρₑₑ + i(Ωₚ/2)(ρ₁ₑ - ρₑ₁)
dρ₂₂/dt = Γₑ₂ρₑₑ + i(Ωc/2)(ρ₂ₑ - ρₑ₂)
dρₑₑ/dt = -Γρₑₑ - i(Ωₚ/2)(ρ₁ₑ - ρₑ₁) - i(Ωc/2)(ρ₂ₑ - ρₑ₂)
dρ₁₂/dt = [i(Δₚ - Δc) - γ_deph]ρ₁₂ + i(Ωₚ/2)ρ₂ₑ* - i(Ωc/2)ρ₁ₑ
dρ₁ₑ/dt = [iΔₚ - Γ/2 - γ_deph]ρ₁ₑ + i(Ωₚ/2)(ρₑₑ - ρ₁₁) - i(Ωc/2)ρ₁₂
dρ₂ₑ/dt = [iΔc - Γ/2 - γ_deph]ρ₂ₑ + i(Ωc/2)(ρₑₑ - ρ₂₂) - i(Ωₚ/2)ρ₁₂
```

where:
- Γ is the total spontaneous emission rate from |e⟩
- Γₑ₁, Γₑ₂ are the decay rates to specific ground states
- γ_deph is an optional pure dephasing rate

### Numerical Method

The steady-state solution is found by solving the system of equations dρ/dt = 0 subject to the constraint Tr(ρ) = 1, using SciPy's `fsolve` function. The density matrix is then post-processed to ensure it remains physical:

1. **Hermiticity**: ρ = (ρ + ρ†)/2
2. **Trace normalization**: ρ = ρ/Tr(ρ)
3. **Positive semidefiniteness**: Eigenvalues are clamped to non-negative values

### Two-Level System

For the two-level case, analytical formulas are used:

```
ρₑₑ = (Ω²/2) / (δ² + (γ/2 + γ_deph)² + Ω²/2)
ρ_gg = 1 - ρₑₑ
ρ_ge = (-iΩ/2)(δ - i(γ/2 + γ_deph)) / (δ² + (γ/2 + γ_deph)² + Ω²/2)
```

## API Reference

### TwoLevelBlochSolver

```python
TwoLevelBlochSolver(
    rabi_frequency: float,
    detuning: float,
    decay_rate: float,
    dephasing_rate: float = 0.0
)
```

**Methods:**
- `solve_steady_state() -> np.ndarray`: Returns 2×2 density matrix
- `validate_density_matrix(rho, tol=1e-6) -> Dict[str, bool]`: Validates physical properties

### BlochSolver

```python
BlochSolver(
    system: DoubleLambdaSystem,
    dephasing_rate: float = 0.0
)
```

**Methods:**
- `solve_steady_state(probe_detuning: Optional[float] = None) -> np.ndarray`: Returns 3×3 density matrix
- `sweep_probe_detuning(detuning_range: np.ndarray) -> Tuple[np.ndarray, np.ndarray]`: Returns (density_matrices, coherences)
- `compute_susceptibility(detuning_range: np.ndarray, atom_density: float = 1e17) -> Tuple[np.ndarray, np.ndarray]`: Returns (absorption, dispersion)
- `validate_density_matrix(rho, tol=1e-6) -> Dict[str, bool]`: Validates physical properties

**Properties:**
- `decay_rates`: Dict containing 'gamma_total', 'gamma_e1', 'gamma_e2'
- `gamma_excited`: Total decay rate of excited state

## Testing

The solver includes comprehensive tests:

```bash
pytest tests/test_bloch_solver.py -v
```

Tests cover:
- Density matrix physical properties (Hermiticity, trace, positive semidefiniteness)
- Two-level system analytical comparisons
- Weak field limit behavior
- Strong detuning behavior
- Dephasing effects
- Numerical stability (large/small Rabi frequencies, large detunings)
- Probe detuning sweeps
- Both Rb87 and Rb85 isotopes

## Examples

Run the included example:

```bash
python examples/bloch_solver_example.py
```

This demonstrates:
1. Two-level system steady-state solution
2. Three-level double-lambda system
3. Probe detuning sweep
4. Susceptibility calculation

## Notes

- All frequencies and detunings are in angular frequency units (rad/s)
- The solver may emit warnings for slowly converging cases, but will still produce valid results
- For EIT transparency, use a strong pump field and weak probe field with both fields near resonance
- The three-level solver uses numerical root finding, which may be slower than analytical methods for simple cases

## Future Enhancements

Potential improvements:
- Add time-dependent density matrix evolution using ODE solvers
- Implement four-level N and ladder systems
- Add transient dynamics visualization
- Optimize numerical solver convergence
- Add magnetic field (Zeeman) effects
