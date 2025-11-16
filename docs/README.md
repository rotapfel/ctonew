# Documentation Index

Welcome to the Rb Double-Lambda EIT Atomic System Model documentation!

## Quick Navigation

### Getting Started
- **[Getting Started Guide](getting_started.md)** - Installation, first simulation, common tasks
- **[Main README](../README.md)** - Project overview and quick start

### Physics and Theory
- **[Physics Background](physics_background.md)** - EIT physics, double-lambda configuration, applications
- **[Optical Bloch Equations](optical_bloch_equations.md)** - Density matrix formalism, susceptibility calculations

### Reference
- **[API Reference](api_reference.md)** - Complete class and method documentation
- **[Parameter Sources](parameter_sources.md)** - Citations and validation of atomic data

## Documentation Structure

```
docs/
├── README.md                      # This file - documentation index
├── getting_started.md             # Tutorial for new users
├── physics_background.md          # EIT physics and theory
├── optical_bloch_equations.md     # Mathematical framework
├── api_reference.md               # API documentation
└── parameter_sources.md           # Data sources and citations
```

## By Topic

### For Physicists/Experimentalists

If you want to understand the **physics** behind EIT:
1. Start with [Physics Background](physics_background.md)
2. Learn the math in [Optical Bloch Equations](optical_bloch_equations.md)
3. Understand parameter choices in [Parameter Sources](parameter_sources.md)

### For Programmers/Engineers

If you want to **use the simulator** in your code:
1. Follow [Getting Started Guide](getting_started.md)
2. Reference [API Documentation](api_reference.md) as needed
3. Study the `examples/` directory

### For Students/Learners

If you're **learning about EIT**:
1. Read [Physics Background](physics_background.md) for concepts
2. Try the examples in [Getting Started](getting_started.md)
3. Run `examples/eit_spectrum_visualization.py` to see the phenomena
4. Dive into [Optical Bloch Equations](optical_bloch_equations.md) for theory

## Core Concepts

### Electromagnetically Induced Transparency (EIT)

EIT is a quantum interference effect where:
- A strong "pump" laser makes an atomic medium transparent to a weak "probe" laser
- Quantum coherence between ground states creates a "dark state"
- Absorption is suppressed, and light propagation is dramatically slowed

**Read more:** [Physics Background](physics_background.md)

### Double-Lambda Configuration

The double-Λ system involves:
- Two ground states (different hyperfine levels)
- One excited state
- Two optical transitions coupling to the same excited state

```
        |e⟩ (excited)
         /\
  Pump  /  \  Probe
       /    \
     |1⟩    |2⟩ (ground states)
```

**Read more:** [Physics Background - Double-Lambda Configuration](physics_background.md#the-double-lambda-configuration)

### Rubidium Isotopes

This simulator supports:
- **⁸⁷Rb**: Nuclear spin I=3/2, natural abundance 27.8%
- **⁸⁵Rb**: Nuclear spin I=5/2, natural abundance 72.2%

Both have well-characterized D1 (795 nm) and D2 (780 nm) transitions.

**Read more:** [Parameter Sources](parameter_sources.md)

## Key Classes

### `DoubleLambdaSystem`
Main class for EIT simulations. Creates complete double-lambda configuration with pump and probe lasers.

```python
from rb_eit import DoubleLambdaSystem
system = DoubleLambdaSystem(isotope="Rb87")
chi = system.eit_susceptibility(detunings)
```

**Documentation:** [API Reference - DoubleLambdaSystem](api_reference.md#doublelambdasystem)

### `Rb87System` and `Rb85System`
Pre-loaded atomic data for Rb-87 and Rb-85 with realistic parameters.

```python
from rb_eit import Rb87System
rb87 = Rb87System()
transition = rb87.get_transition("5S_1/2, F=2", "5P_3/2, F=3")
```

**Documentation:** [API Reference - Rb87System](api_reference.md#rb87system)

### `AtomicLevel`, `Transition`, `LaserField`
Building blocks for custom atomic systems.

**Documentation:** [API Reference](api_reference.md)

## Examples

### Basic EIT Spectrum

```python
import numpy as np
from rb_eit import DoubleLambdaSystem

system = DoubleLambdaSystem(
    isotope="Rb87",
    pump_rabi_frequency=2 * np.pi * 10e6,
    probe_rabi_frequency=2 * np.pi * 1e6
)

detunings = np.linspace(-20e6, 20e6, 200) * 2 * np.pi
chi = system.eit_susceptibility(detunings)

absorption = np.imag(chi)  # Shows transparency window
dispersion = np.real(chi)  # Shows steep slope (slow light)
```

**More examples:** [Getting Started](getting_started.md) and `examples/` directory

## Scientific Background

### Key Papers

**EIT Reviews:**
- Fleischhauer et al., *Rev. Mod. Phys.* 77, 633 (2005) - Comprehensive review
- Harris, *Physics Today* 50(7), 36 (1997) - Accessible introduction

**Rb Spectroscopy:**
- Steck, "Rubidium 87 D Line Data" (2021) - Standard reference
- Steck, "Rubidium 85 D Line Data" (2021) - Standard reference

**All citations:** [Parameter Sources](parameter_sources.md)

## How to Use This Documentation

### I want to...

**...understand what EIT is**
→ Read [Physics Background](physics_background.md)

**...run my first simulation**
→ Follow [Getting Started Guide](getting_started.md)

**...learn the theory**
→ Study [Optical Bloch Equations](optical_bloch_equations.md)

**...find a specific function**
→ Check [API Reference](api_reference.md)

**...verify parameter values**
→ See [Parameter Sources](parameter_sources.md)

**...create custom configurations**
→ See examples in [Getting Started](getting_started.md#common-tasks)

**...generate plots**
→ Run `examples/eit_spectrum_visualization.py`

**...cite this work**
→ See [Main README - Citation](../README.md#citation)

## Testing and Validation

All parameters are validated against literature:
- Hyperfine constants from Steck's alkali data
- Selection rules automatically enforced
- Physical constraints checked (e.g., positive frequencies)
- Comprehensive unit test suite

Run tests:
```bash
pytest tests/ -v
```

**Details:** [Parameter Sources - Validation](parameter_sources.md#validation-and-cross-checks)

## Contributing

Contributions welcome! Potential areas:
- Full optical Bloch equation solver (time-dependent)
- Doppler broadening for thermal atoms
- Maxwell-Bloch equations (propagation effects)
- Zeeman sublevels and magnetic fields
- Additional alkali species (Na, K, Cs)

## Support

- GitHub Issues: Report bugs or request features
- Email: Contact maintainers (see README)
- Examples: Study `examples/` directory
- Tests: Run `pytest tests/ -v` to verify installation

## License

MIT License - Free for academic and commercial use.

Atomic parameters from Steck's alkali data (public domain).

**Full license:** [Main README - License](../README.md#license)

---

**Navigation:**
- [↑ Back to main README](../README.md)
- [→ Getting Started](getting_started.md)
- [→ Physics Background](physics_background.md)
- [→ API Reference](api_reference.md)
