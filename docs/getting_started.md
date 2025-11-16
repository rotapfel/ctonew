# Getting Started Guide

This guide will help you get up and running with the Rb EIT simulator quickly.

## Installation

### Basic Installation

Install the package with core dependencies:

```bash
git clone https://github.com/yourusername/rb_eit.git
cd rb_eit
pip install -e .
```

### With Visualization Support

To run the plotting examples, install with matplotlib:

```bash
pip install -e ".[viz]"
```

### Development Installation

For development with testing tools:

```bash
pip install -e ".[dev]"
```

### All Features

Install everything:

```bash
pip install -e ".[dev,viz]"
```

## Verify Installation

Test that the package is installed correctly:

```python
import rb_eit
print(f"rb_eit version: {rb_eit.__version__}")

from rb_eit import DoubleLambdaSystem
system = DoubleLambdaSystem(isotope="Rb87")
print(system)
```

Expected output:
```
rb_eit version: 0.1.0
Double-Lambda EIT Configuration (Rb87):
  Ground State 1: 5S_1/2, F=1
  Ground State 2: 5S_1/2, F=2
  Excited State:  5P_3/2, F=2
  Pump:  Ω=10.00 MHz, Δ=0.00 MHz
  Probe: Ω=1.00 MHz, Δ=0.00 MHz
```

## Your First EIT Simulation

### Step 1: Import Required Modules

```python
import numpy as np
from rb_eit import DoubleLambdaSystem
```

### Step 2: Create an EIT System

```python
system = DoubleLambdaSystem(
    isotope="Rb87",                          # Rb-87 or Rb-85
    pump_rabi_frequency=2 * np.pi * 10e6,   # 10 MHz pump
    probe_rabi_frequency=2 * np.pi * 1e6,   # 1 MHz probe
)
```

### Step 3: Calculate EIT Spectrum

```python
# Create detuning array (in rad/s)
detunings = np.linspace(-20e6, 20e6, 200) * 2 * np.pi

# Calculate susceptibility
chi = system.eit_susceptibility(detunings)

# Extract absorption and dispersion
absorption = np.imag(chi)
dispersion = np.real(chi)
```

### Step 4: Visualize Results (Optional)

```python
import matplotlib.pyplot as plt

# Convert detunings to MHz for plotting
det_mhz = detunings / (2 * np.pi * 1e6)

plt.figure(figsize=(10, 4))

plt.subplot(121)
plt.plot(det_mhz, absorption)
plt.xlabel('Probe Detuning (MHz)')
plt.ylabel('Absorption (arb.)')
plt.title('EIT Transparency Window')
plt.grid(True)

plt.subplot(122)
plt.plot(det_mhz, dispersion)
plt.xlabel('Probe Detuning (MHz)')
plt.ylabel('Dispersion (arb.)')
plt.title('Steep Dispersion (Slow Light)')
plt.grid(True)

plt.tight_layout()
plt.show()
```

## Common Tasks

### Access Atomic Parameters

```python
from rb_eit import Rb87System

rb87 = Rb87System()

# Get a specific level
ground = rb87.get_level("5S_1/2, F=2")
print(f"Ground state energy: {ground.energy} J")

# Get a transition
trans = rb87.get_transition("5S_1/2, F=2", "5P_3/2, F=3")
print(f"Wavelength: {trans.wavelength*1e9:.4f} nm")
print(f"Dipole moment: {trans.dipole_moment:.3e} C·m")

# Calculate decay rate
excited = rb87.get_level("5P_3/2, F=3")
gamma = rb87.total_decay_rate(excited)
print(f"Natural linewidth: {gamma/(2*np.pi*1e6):.3f} MHz")
```

### Use Different Hyperfine Levels

```python
system = DoubleLambdaSystem(
    isotope="Rb87",
    ground_state_1_label="5S_1/2, F=1",    # Lower ground state
    ground_state_2_label="5S_1/2, F=2",    # Upper ground state
    excited_state_label="5P_3/2, F=1",     # Choose excited state
)
```

### Scan Pump Power

```python
pump_powers = [5, 10, 20, 40]  # MHz
detunings = np.linspace(-30e6, 30e6, 400) * 2 * np.pi

for pump_mhz in pump_powers:
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * pump_mhz * 1e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    chi = system.eit_susceptibility(detunings)
    # Process and plot...
```

### Update Laser Parameters

```python
system = DoubleLambdaSystem(isotope="Rb87")

# Update pump
system.set_pump_parameters(
    rabi_frequency=2 * np.pi * 15e6,  # 15 MHz
    detuning=2 * np.pi * 2e6           # 2 MHz red detuning
)

# Update probe
system.set_probe_parameters(
    rabi_frequency=2 * np.pi * 2e6,
    detuning=0.0
)

# Check current values
pump_rabi, probe_rabi = system.rabi_frequencies()
print(f"Pump Rabi: {pump_rabi/(2*np.pi*1e6):.2f} MHz")
```

### Work with Rb-85

```python
from rb_eit import Rb85System, DoubleLambdaSystem

# Create Rb-85 system
system = DoubleLambdaSystem(isotope="Rb85")

# Access Rb-85 specific data
rb85 = Rb85System()
print(f"Nuclear spin: {rb85.nuclear_spin}")  # 5/2

# List available levels
for level in rb85.ground_states:
    print(level)
# Output:
# 5S_1/2, F=2 (E=0.000e+00 J)
# 5S_1/2, F=3 (E=5.046e-25 J)
```

## Understanding Units

The package uses **SI units** internally. Here's a quick reference:

| Quantity | Internal Unit | Common Unit | Conversion |
|----------|--------------|-------------|------------|
| Energy | Joules (J) | eV | 1 eV = 1.602×10⁻¹⁹ J |
| Frequency | Hertz (Hz) | MHz | 1 MHz = 10⁶ Hz |
| Angular frequency | rad/s | MHz | ω = 2π × f |
| Wavelength | meters (m) | nm | 1 nm = 10⁻⁹ m |
| Dipole moment | C·m | ea₀ | 1 ea₀ = 8.478×10⁻³⁰ C·m |

### Converting Between Frequencies

```python
import numpy as np

# Frequency in MHz to angular frequency in rad/s
freq_mhz = 10.0  # MHz
omega = 2 * np.pi * freq_mhz * 1e6  # rad/s

# Angular frequency back to MHz
freq_mhz = omega / (2 * np.pi * 1e6)

# Energy to frequency
from rb_eit.constants import HBAR
energy_joules = 1e-24  # J
omega = energy_joules / HBAR  # rad/s
freq_hz = omega / (2 * np.pi)
```

## Running Examples

The `examples/` directory contains demonstration scripts:

### Basic Usage

```bash
python examples/basic_usage.py
```

Shows:
- Creating Rb-87 and Rb-85 systems
- Accessing atomic parameters
- Building double-lambda configurations
- Computing EIT susceptibility

### Visualization

```bash
python examples/eit_spectrum_visualization.py
```

Generates publication-quality plots:
- EIT absorption and dispersion spectra
- Pump power dependence
- Two-photon detuning effects
- Isotope comparison
- Energy level diagram

## Next Steps

Now that you're set up, explore:

1. **[Physics Background](physics_background.md)**: Understand the theory behind EIT
2. **[Optical Bloch Equations](optical_bloch_equations.md)**: Learn the mathematical framework
3. **[API Reference](api_reference.md)**: Detailed documentation of all classes
4. **[Parameter Sources](parameter_sources.md)**: Citations for atomic data

## Troubleshooting

### Import Error: No module named 'rb_eit'

Make sure you've installed the package:
```bash
cd /path/to/rb_eit
pip install -e .
```

### matplotlib not found

Install visualization dependencies:
```bash
pip install matplotlib
# or
pip install -e ".[viz]"
```

### Selection Rule Violations

If you get errors about selection rules, check that your chosen hyperfine levels satisfy ΔF = 0, ±1:

```python
# This will fail (ΔF = 2):
system = DoubleLambdaSystem(
    isotope="Rb87",
    ground_state_1_label="5S_1/2, F=1",
    excited_state_label="5P_3/2, F=3"  # F=1 to F=3 not allowed!
)

# This works (ΔF = 1):
system = DoubleLambdaSystem(
    isotope="Rb87",
    ground_state_1_label="5S_1/2, F=1",
    excited_state_label="5P_3/2, F=2"  # OK
)
```

### Unexpected Results

- Check that Rabi frequencies and detunings are in **rad/s**, not Hz
- Ensure pump is stronger than probe (Ω_pump > Ω_probe)
- For EIT, set pump_detuning ≈ probe_detuning for two-photon resonance

## Getting Help

- Check the [API Reference](api_reference.md) for detailed class documentation
- Look at example scripts in `examples/`
- Run tests to verify installation: `pytest tests/ -v`
- Open an issue on GitHub for bugs or questions

Happy simulating! 🔬
