# Rb Double-Lambda EIT Atomic System Model

A Python package for modeling Rubidium (Rb-87 and Rb-85) atomic systems in double-lambda Electromagnetically Induced Transparency (EIT) configurations.

## Features

- Data models for atomic levels, transitions, decay rates, and dipole moments
- Realistic Rb-87 and Rb-85 parameters with literature-based values
- Utilities for constructing double-lambda EIT configurations
- Parameter validation and consistency checking
- Comprehensive unit tests

## Installation

```bash
pip install -e .
```

## Usage

```python
from rb_eit import Rb87DoubleRho, LaserField

# Create an Rb-87 double-lambda system
system = Rb87DoubleRho()

# Configure pump and probe fields
pump = LaserField(
    rabi_frequency=2 * pi * 10e6,  # 10 MHz
    detuning=0.0
)
probe = LaserField(
    rabi_frequency=2 * pi * 1e6,  # 1 MHz
    detuning=0.0
)

# Access atomic parameters
print(system.ground_states)
print(system.excited_states)
print(system.decay_rates)
```

## References

- Steck, D. A. "Rubidium 87 D Line Data" (2001)
- Steck, D. A. "Rubidium 85 D Line Data" (2001)
- Fleischhauer, M., Imamoglu, A., & Marangos, J. P. "Electromagnetically induced transparency: Optics in coherent media" Rev. Mod. Phys. 77, 633 (2005)
