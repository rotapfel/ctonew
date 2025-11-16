# Rb Double-Lambda EIT Atomic System Model

A Python package for modeling Rubidium (Rb-87 and Rb-85) atomic systems in double-lambda Electromagnetically Induced Transparency (EIT) configurations with Four-Wave Mixing (FWM) spectra calculations.

## Features

- Data models for atomic levels, transitions, decay rates, and dipole moments
- Realistic Rb-87 and Rb-85 parameters with literature-based values
- Utilities for constructing double-lambda EIT configurations
- **Four-Wave Mixing (FWM) spectra calculation**
- **Optical Bloch equation solver for steady-state density matrices**
- **Third-order nonlinear susceptibility χ^(3) computation**
- **Multi-parameter sweep utilities (1D and 2D)**
- **CSV and JSON export with metadata**
- Parameter validation and consistency checking
- Comprehensive unit tests (155 passing tests)

## Installation

```bash
pip install -e .
```

## Usage

### Basic Double-Lambda System

```python
import numpy as np
from rb_eit import DoubleLambdaSystem

# Create an Rb-87 double-lambda system
system = DoubleLambdaSystem(
    isotope="Rb87",
    pump_rabi_frequency=2 * np.pi * 10e6,  # 10 MHz
    probe_rabi_frequency=2 * np.pi * 1e6,   # 1 MHz
)

# Access atomic parameters
print(system.ground_state_1)
print(system.ground_state_2)
print(system.excited_state)
print(system.transition_1)
print(system.transition_2)
```

### FWM Spectra Calculation

```python
from rb_eit import FWMSpectraCalculator, ParameterSweep, SpectraExporter

# Initialize FWM calculator
calculator = FWMSpectraCalculator(
    system=system,
    number_density=1e17,
    interaction_length=0.01
)

# Calculate χ^(3) spectrum
probe_detuning = np.linspace(-20e6, 20e6, 100) * 2 * np.pi
chi3_spectrum = calculator.compute_chi3_spectrum(probe_detuning)

# Calculate FWM intensity spectrum
intensity_spectrum = calculator.compute_fwm_intensity_spectrum(probe_detuning)

# Perform parameter sweep
sweep = ParameterSweep(calculator)
result = sweep.sweep_probe_detuning(-20e6 * 2 * np.pi, 20e6 * 2 * np.pi, num_points=100)

# Export results
SpectraExporter.export_multiple_formats(result, "fwm_spectrum")
```

For detailed FWM documentation, see [FWM_DOCUMENTATION.md](FWM_DOCUMENTATION.md).

## References

- Steck, D. A. "Rubidium 87 D Line Data" (2001)
- Steck, D. A. "Rubidium 85 D Line Data" (2001)
- Fleischhauer, M., Imamoglu, A., & Marangos, J. P. "Electromagnetically induced transparency: Optics in coherent media" Rev. Mod. Phys. 77, 633 (2005)
