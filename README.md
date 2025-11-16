# Rb Double-Lambda EIT Atomic System Model

A Python package for modeling Rubidium (Rb-87 and Rb-85) atomic systems in double-lambda Electromagnetically Induced Transparency (EIT) configurations. This simulator provides realistic atomic parameters, quantum state modeling, and EIT susceptibility calculations for atomic physics research and education.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Features

- 📊 **Realistic Atomic Data**: Literature-based parameters from Steck's alkali data compilation
- 🔬 **Complete Level Structure**: Hyperfine levels for ground and excited states
- 🌈 **D1 and D2 Transitions**: Full transition data with dipole moments and decay rates
- 🔄 **Double-Lambda EIT**: Pre-configured systems for common EIT configurations
- ✅ **Validation**: Automatic checking of selection rules and quantum number constraints
- 📈 **Susceptibility Calculation**: Compute EIT absorption and dispersion spectra
- 🧪 **Two Isotopes**: Support for both ⁸⁷Rb and ⁸⁵Rb
- 🧮 **Unit Testing**: Comprehensive test suite ensuring physical correctness

## Physics Background

Electromagnetically Induced Transparency (EIT) is a quantum interference effect where a strong "pump" laser makes an atomic medium transparent to a weak "probe" laser. In the double-lambda (Λ) configuration:

- Two ground states (different hyperfine levels) couple to one common excited state
- Quantum coherence between ground states creates a "dark state" 
- Probe absorption is suppressed near two-photon resonance
- Group velocity is dramatically reduced (slow light)
- Nonlinear susceptibility χ⁽³⁾ is enhanced

See [docs/physics_background.md](docs/physics_background.md) for detailed physics explanation.

## Installation

### From Source

```bash
git clone https://github.com/yourusername/rb_eit.git
cd rb_eit
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

### Requirements

- Python 3.8 or higher
- NumPy >= 1.20.0
- SciPy >= 1.7.0
- matplotlib (optional, for visualization examples)

## Quick Start

### Basic Usage

```python
import numpy as np
from rb_eit import DoubleLambdaSystem

# Create Rb-87 double-lambda EIT system with default configuration
# |1⟩ = 5S_1/2 F=1, |2⟩ = 5S_1/2 F=2, |e⟩ = 5P_3/2 F=2
system = DoubleLambdaSystem(
    isotope="Rb87",
    pump_rabi_frequency=2 * np.pi * 10e6,   # 10 MHz pump
    probe_rabi_frequency=2 * np.pi * 1e6,   # 1 MHz probe
    pump_detuning=0.0,                       # On resonance
    probe_detuning=0.0
)

print(system)
```

### Computing EIT Spectra

```python
# Scan probe detuning from -20 to +20 MHz
detuning_scan = np.linspace(-20e6, 20e6, 400) * 2 * np.pi  # rad/s
susceptibility = system.eit_susceptibility(detuning_scan)

# Extract absorption (imaginary part) and dispersion (real part)
absorption = np.imag(susceptibility)
dispersion = np.real(susceptibility)

# Plot (requires matplotlib)
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 4))
plt.subplot(121)
plt.plot(detuning_scan / (2*np.pi*1e6), absorption)
plt.xlabel('Probe Detuning (MHz)')
plt.ylabel('Absorption (arb. units)')
plt.title('EIT Absorption Spectrum')

plt.subplot(122)
plt.plot(detuning_scan / (2*np.pi*1e6), dispersion)
plt.xlabel('Probe Detuning (MHz)')
plt.ylabel('Dispersion (arb. units)')
plt.title('EIT Dispersion (Slow Light)')

plt.tight_layout()
plt.show()
```

### Custom Configuration

```python
# Specify custom hyperfine levels
system = DoubleLambdaSystem(
    isotope="Rb87",
    ground_state_1_label="5S_1/2, F=1",
    ground_state_2_label="5S_1/2, F=2",
    excited_state_label="5P_3/2, F=1",  # Different excited state
    pump_rabi_frequency=2 * np.pi * 15e6,
    probe_rabi_frequency=2 * np.pi * 2e6
)
```

### Accessing Atomic Parameters

```python
from rb_eit import Rb87System

# Load Rb-87 atomic data
rb87 = Rb87System()

# Access levels and transitions
ground = rb87.get_level("5S_1/2, F=2")
excited = rb87.get_level("5P_3/2, F=3")
transition = rb87.get_transition("5S_1/2, F=2", "5P_3/2, F=3")

print(f"Transition frequency: {transition.frequency/1e12:.4f} THz")
print(f"Wavelength: {transition.wavelength*1e9:.4f} nm")
print(f"Dipole moment: {transition.dipole_moment:.3e} C·m")

# Get total decay rate
decay_rate = rb87.total_decay_rate(excited)
print(f"Excited state linewidth: {decay_rate/(2*np.pi*1e6):.3f} MHz")
```

## Examples

The `examples/` directory contains demonstration scripts:

- **`basic_usage.py`**: Comprehensive examples of all package features

Run examples:
```bash
python examples/basic_usage.py
```

For visualization examples with plots:
```bash
python examples/eit_spectrum_visualization.py
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Physics Background](docs/physics_background.md)**: EIT theory and double-lambda configuration
- **[Optical Bloch Equations](docs/optical_bloch_equations.md)**: Density matrix formalism and susceptibility derivation
- **[API Reference](docs/api_reference.md)**: Complete API documentation for all classes
- **[Parameter Sources](docs/parameter_sources.md)**: Citations and validation of atomic data

## Physical Units

This package uses **SI units** internally:

- **Energy**: Joules (J)
- **Frequency**: Hertz (Hz)
- **Angular frequency**: rad/s
- **Length**: meters (m)
- **Dipole moment**: Coulomb-meters (C·m)

**Important:** Rabi frequencies and detunings are in **rad/s**, not Hz. Convert using:
```python
omega_rad_per_s = 2 * pi * frequency_Hz
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=rb_eit --cov-report=html
```

All examples are also validated:

```bash
pytest tests/test_examples.py -v
```

## Project Structure

```
rb_eit/
├── src/rb_eit/          # Main package
│   ├── atomic_level.py      # AtomicLevel data class
│   ├── transition.py        # Transition between levels
│   ├── decay_channel.py     # Spontaneous decay
│   ├── laser_field.py       # Laser field parameters
│   ├── rb87_system.py       # Rb-87 atomic data
│   ├── rb85_system.py       # Rb-85 atomic data
│   ├── double_lambda.py     # Double-lambda EIT system
│   └── constants.py         # Physical constants
├── tests/               # Unit tests
├── examples/            # Usage examples
├── docs/                # Documentation
└── README.md
```

## Scientific Background

### Key References

**EIT Theory:**
- Fleischhauer, M., Imamoglu, A., & Marangos, J. P. "Electromagnetically induced transparency: Optics in coherent media." *Rev. Mod. Phys.* 77, 633 (2005)
- Harris, S. E. "Electromagnetically Induced Transparency." *Physics Today* 50(7), 36 (1997)

**Atomic Parameters:**
- Steck, D. A. "Rubidium 87 D Line Data" (revision 2.2.2, 2021) http://steck.us/alkalidata
- Steck, D. A. "Rubidium 85 D Line Data" (revision 2.2.2, 2021) http://steck.us/alkalidata

See [docs/parameter_sources.md](docs/parameter_sources.md) for complete citations.

## Contributing

Contributions are welcome! Areas for improvement:

- Full optical Bloch equation solver (time-dependent dynamics)
- Doppler broadening for thermal atoms
- Maxwell-Bloch equations (light propagation)
- Zeeman sublevel structure and magnetic fields
- Additional alkali species (Na, K, Cs)

Please open an issue or pull request on GitHub.

## License

MIT License

Copyright (c) 2024 CTO.new

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**Note on Atomic Data:** Spectroscopic parameters are derived from Steck's alkali data compilation, which is in the public domain. No restrictions apply to academic or commercial use.

## Citation

If you use this package in published research, please cite:

```bibtex
@software{rb_eit_2024,
  title = {Rb Double-Lambda EIT Atomic System Model},
  author = {CTO.new},
  year = {2024},
  version = {0.1.0},
  url = {https://github.com/yourusername/rb_eit}
}
```

Also cite the atomic parameter source:

```bibtex
@misc{steck2021rb87,
  author = {Steck, Daniel A.},
  title = {Rubidium 87 {D} Line Data},
  year = {2021},
  note = {Revision 2.2.2},
  url = {http://steck.us/alkalidata}
}
```

## Contact

For questions, issues, or collaboration opportunities, please open an issue on GitHub or contact the maintainers.

## Acknowledgments

- Daniel Steck for comprehensive Rb spectroscopic data
- The atomic physics community for EIT theoretical foundations
- Contributors and users of this package

---

**Happy simulating!** 🔬✨
