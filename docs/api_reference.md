# API Reference

## Core Classes

### AtomicLevel

Represents a quantum state of an atom.

```python
class AtomicLevel:
    def __init__(
        self,
        n: int,
        L: int,
        J: float,
        F: float,
        nuclear_spin: float,
        energy: float = 0.0,
        label: str = ""
    )
```

**Parameters:**
- `n` (int): Principal quantum number
- `L` (int): Orbital angular momentum quantum number (0=S, 1=P, 2=D, ...)
- `J` (float): Total electronic angular momentum
- `F` (float): Total angular momentum (J + I)
- `nuclear_spin` (float): Nuclear spin I
- `energy` (float): Energy of the level in Joules (default: 0.0)
- `label` (str): Human-readable label (e.g., "5S_1/2, F=2")

**Validation:**
- Enforces quantum number constraints (F in [|J-I|, J+I])
- Validates L, J, F are non-negative
- Ensures label uniqueness

**Example:**
```python
from rb_eit import AtomicLevel

ground_state = AtomicLevel(
    n=5,
    L=0,  # S orbital
    J=0.5,
    F=2,
    nuclear_spin=1.5,  # Rb-87
    energy=0.0,
    label="5S_1/2, F=2"
)
```

---

### Transition

Represents an atomic transition between two levels.

```python
class Transition:
    def __init__(
        self,
        lower: AtomicLevel,
        upper: AtomicLevel,
        dipole_moment: float,
        frequency: float
    )
```

**Parameters:**
- `lower` (AtomicLevel): Lower energy level
- `upper` (AtomicLevel): Upper energy level
- `dipole_moment` (float): Transition dipole moment in C·m
- `frequency` (float): Transition frequency in Hz

**Properties:**
- `wavelength`: Transition wavelength in meters (λ = c/ν)
- `energy`: Photon energy in Joules (E = hν)
- `angular_frequency`: Angular frequency in rad/s (ω = 2πν)

**Validation:**
- Enforces electric dipole selection rules (ΔL=±1, ΔJ=0,±1, ΔF=0,±1)
- Checks energy ordering (lower.energy < upper.energy)

**Example:**
```python
from rb_eit import Transition, AtomicLevel

transition = Transition(
    lower=ground_state,
    upper=excited_state,
    dipole_moment=3.584e-29,  # C·m for Rb D2 line
    frequency=384.23e12  # Hz
)

print(f"Wavelength: {transition.wavelength*1e9:.2f} nm")
```

---

### DecayChannel

Represents spontaneous decay from upper to lower level.

```python
class DecayChannel:
    def __init__(
        self,
        upper: AtomicLevel,
        lower: AtomicLevel,
        rate: float,
        branching_ratio: float = 1.0
    )
```

**Parameters:**
- `upper` (AtomicLevel): Upper (decaying) level
- `lower` (AtomicLevel): Lower (destination) level
- `rate` (float): Decay rate in rad/s
- `branching_ratio` (float): Branching ratio (default: 1.0)

**Validation:**
- Same selection rules as Transition
- Enforces 0 ≤ branching_ratio ≤ 1

**Example:**
```python
from rb_eit import DecayChannel

decay = DecayChannel(
    upper=excited_state,
    lower=ground_state,
    rate=2 * np.pi * 6.065e6,  # Natural linewidth
    branching_ratio=0.5
)
```

---

### LaserField

Represents laser field parameters.

```python
class LaserField:
    def __init__(
        self,
        rabi_frequency: float,
        detuning: float = 0.0,
        frequency: float = 0.0,
        phase: float = 0.0
    )
```

**Parameters:**
- `rabi_frequency` (float): Rabi frequency Ω in rad/s
- `detuning` (float): Detuning Δ from resonance in rad/s (default: 0.0)
- `frequency` (float): Laser frequency in Hz (default: 0.0)
- `phase` (float): Laser phase in radians (default: 0.0)

**Properties:**
- `intensity`: Proportional to Ω² (requires dipole moment for absolute units)

**Example:**
```python
from rb_eit import LaserField
import numpy as np

pump = LaserField(
    rabi_frequency=2 * np.pi * 10e6,  # 10 MHz
    detuning=2 * np.pi * 1e6,  # 1 MHz red detuning
    frequency=384.23e12  # Hz
)
```

---

### Rb87System

Pre-configured Rb-87 atomic system with realistic parameters.

```python
class Rb87System:
    def __init__(self)
```

**Attributes:**
- `nuclear_spin`: Nuclear spin I = 3/2
- `ground_states`: List of 5S₁/₂ hyperfine levels (F=1, 2)
- `excited_states_5p12`: List of 5P₁/₂ levels (D1 line)
- `excited_states_5p32`: List of 5P₃/₂ levels (D2 line)
- `transitions_d1`: D1 line transitions
- `transitions_d2`: D2 line transitions
- `decay_channels`: All spontaneous decay channels

**Methods:**
- `get_level(label: str) -> AtomicLevel`: Retrieve level by label
- `get_transition(lower_label: str, upper_label: str) -> Transition`: Get transition
- `total_decay_rate(level: AtomicLevel) -> float`: Sum of all decay rates from level

**Example:**
```python
from rb_eit import Rb87System

rb87 = Rb87System()
ground = rb87.get_level("5S_1/2, F=2")
excited = rb87.get_level("5P_3/2, F=3")
transition = rb87.get_transition("5S_1/2, F=2", "5P_3/2, F=3")

print(f"Transition frequency: {transition.frequency/1e12:.3f} THz")
```

---

### Rb85System

Pre-configured Rb-85 atomic system with realistic parameters.

```python
class Rb85System:
    def __init__(self)
```

**Attributes:**
- `nuclear_spin`: Nuclear spin I = 5/2
- `ground_states`: List of 5S₁/₂ hyperfine levels (F=2, 3)
- `excited_states_5p12`: List of 5P₁/₂ levels (D1 line)
- `excited_states_5p32`: List of 5P₃/₂ levels (D2 line)
- `transitions_d1`: D1 line transitions
- `transitions_d2`: D2 line transitions
- `decay_channels`: All spontaneous decay channels

**Methods:**
Same as `Rb87System`.

**Example:**
```python
from rb_eit import Rb85System

rb85 = Rb85System()
print(f"Nuclear spin: {rb85.nuclear_spin}")
print(f"Number of ground states: {len(rb85.ground_states)}")
```

---

### DoubleLambdaSystem

Complete double-lambda EIT configuration.

```python
class DoubleLambdaSystem:
    def __init__(
        self,
        isotope: str = "Rb87",
        ground_state_1_label: Optional[str] = None,
        ground_state_2_label: Optional[str] = None,
        excited_state_label: Optional[str] = None,
        pump_rabi_frequency: float = 2 * np.pi * 10e6,
        probe_rabi_frequency: float = 2 * np.pi * 1e6,
        pump_detuning: float = 0.0,
        probe_detuning: float = 0.0
    )
```

**Parameters:**
- `isotope` (str): "Rb87" or "Rb85"
- `ground_state_1_label` (str, optional): Label for |1⟩ (uses default if None)
- `ground_state_2_label` (str, optional): Label for |2⟩ (uses default if None)
- `excited_state_label` (str, optional): Label for |e⟩ (uses default if None)
- `pump_rabi_frequency` (float): Pump Rabi frequency in rad/s
- `probe_rabi_frequency` (float): Probe Rabi frequency in rad/s
- `pump_detuning` (float): Pump detuning in rad/s
- `probe_detuning` (float): Probe detuning in rad/s

**Default Configurations:**
- **Rb-87**: |1⟩ = F=1, |2⟩ = F=2, |e⟩ = F'=2
- **Rb-85**: |1⟩ = F=2, |2⟩ = F=3, |e⟩ = F'=3

**Attributes:**
- `atomic_system`: Underlying Rb87System or Rb85System
- `ground_state_1`, `ground_state_2`, `excited_state`: AtomicLevel objects
- `transition_1`, `transition_2`: Transition objects
- `pump`, `probe`: LaserField objects

**Methods:**

#### `two_photon_detuning() -> float`
Calculate two-photon detuning δ = Δ_pump - Δ_probe.

#### `eit_susceptibility(probe_detuning_scan: np.ndarray) -> np.ndarray`
Calculate EIT susceptibility vs probe detuning.

**Parameters:**
- `probe_detuning_scan` (np.ndarray): Array of probe detunings in rad/s

**Returns:**
- Complex susceptibility array (same shape as input)

#### `rabi_frequencies() -> Tuple[float, float]`
Return (pump_rabi, probe_rabi) in rad/s.

#### `detunings() -> Tuple[float, float]`
Return (pump_detuning, probe_detuning) in rad/s.

#### `set_pump_parameters(rabi_frequency: float, detuning: float)`
Update pump field parameters.

#### `set_probe_parameters(rabi_frequency: float, detuning: float)`
Update probe field parameters.

**Example:**
```python
from rb_eit import DoubleLambdaSystem
import numpy as np

system = DoubleLambdaSystem(
    isotope="Rb87",
    pump_rabi_frequency=2 * np.pi * 10e6,
    probe_rabi_frequency=2 * np.pi * 1e6
)

# Scan probe detuning
detunings = np.linspace(-20e6, 20e6, 200) * 2 * np.pi
susceptibility = system.eit_susceptibility(detunings)

# Plot absorption spectrum
import matplotlib.pyplot as plt
plt.plot(detunings / (2*np.pi*1e6), np.imag(susceptibility))
plt.xlabel('Probe Detuning (MHz)')
plt.ylabel('Im(χ) (absorption)')
plt.show()
```

---

## Constants Module

Physical constants and Rb-specific parameters.

```python
from rb_eit.constants import *
```

**Physical Constants:**
- `HBAR`: ℏ = 1.054571817×10⁻³⁴ J·s
- `C`: c = 299792458 m/s
- `EPSILON_0`: ε₀ = 8.854187812×10⁻¹² F/m
- `E_CHARGE`: e = 1.602176634×10⁻¹⁹ C
- `A_BOHR`: a₀ = 5.29177210903×10⁻¹¹ m
- `PI`: π

**Rb Nuclear Spins:**
- `RB87_NUCLEAR_SPIN`: 3/2
- `RB85_NUCLEAR_SPIN`: 5/2

**Rb D-line Properties:**
- `RB_D1_WAVELENGTH`: 794.979014933 nm
- `RB_D2_WAVELENGTH`: 780.241368271 nm
- `RB_D1_FREQUENCY`: D1 transition frequency (Hz)
- `RB_D2_FREQUENCY`: D2 transition frequency (Hz)
- `RB_D_LINE_DECAY_RATE`: 2π × 6.065 MHz

**Rb-87 Hyperfine Constants:**
- `RB87_GROUND_HFS_A`: 2π × 3.417341305 GHz
- `RB87_5P12_HFS_A`: 2π × 407.24 MHz
- `RB87_5P32_HFS_A`: 2π × 84.7185 MHz
- `RB87_5P32_HFS_B`: 2π × 12.4965 MHz

**Rb-85 Hyperfine Constants:**
- `RB85_GROUND_HFS_A`: 2π × 1.0119108130 GHz
- `RB85_5P12_HFS_A`: 2π × 120.640 MHz
- `RB85_5P32_HFS_A`: 2π × 25.0020 MHz
- `RB85_5P32_HFS_B`: 2π × 25.790 MHz

**Reduced Dipole Moments:**
- `RB_D1_REDUCED_DIPOLE`: 2.537×10⁻²⁹ C·m
- `RB_D2_REDUCED_DIPOLE`: 3.584×10⁻²⁹ C·m

---

## Units and Conventions

### Energy and Frequency
- **Energies**: Joules (J)
- **Frequencies**: Hertz (Hz)
- **Angular frequencies**: rad/s
- **Conversion**: E = ℏω = hν

### Angular Momentum
- All in units of ℏ (dimensionless quantum numbers)

### Electric Dipole Moment
- SI units: Coulomb-meters (C·m)
- Atomic unit: ea₀ ≈ 8.478×10⁻³⁰ C·m

### Typical Values
- **Rabi frequency**: 1-100 MHz → 2π × (1-100)×10⁶ rad/s
- **Detuning**: ±100 MHz → ±2π × 100×10⁶ rad/s
- **Decay rate**: 6 MHz → 2π × 6.065×10⁶ rad/s

**Note:** Always use angular frequencies (rad/s) for Rabi frequencies and detunings in calculations. Convert to ordinary frequency (Hz) by dividing by 2π for plotting/display.

---

## Error Handling

The package performs comprehensive validation:

**ValueError Exceptions:**
- Invalid quantum numbers
- Selection rule violations
- Negative or non-physical parameters
- Incompatible state configurations

**Example:**
```python
try:
    system = DoubleLambdaSystem(isotope="Rb99")
except ValueError as e:
    print(f"Error: {e}")
    # Output: "Unknown isotope: Rb99. Must be 'Rb87' or 'Rb85'"
```

Always check that:
1. Energy ordering is correct (ground < excited)
2. Selection rules are satisfied (ΔF = 0, ±1, etc.)
3. Nuclear spin matches isotope
4. Rabi frequencies and decay rates are positive
