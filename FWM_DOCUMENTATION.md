# Four-Wave Mixing (FWM) Spectra Calculation

This module provides comprehensive tools for calculating Four-Wave Mixing (FWM) spectra in double-lambda EIT systems using Rubidium-87 and Rubidium-85 atoms.

## Overview

The FWM module consists of four main components:

1. **Bloch Equation Solver** (`bloch_equations.py`) - Solves steady-state optical Bloch equations for density matrix
2. **FWM Spectra Calculator** (`fwm_spectra.py`) - Computes third-order susceptibility χ^(3) and FWM intensities
3. **Parameter Sweep** (`parameter_sweep.py`) - Utilities for multi-parameter sweeps
4. **Data Exporters** (`exporters.py`) - CSV and JSON export with metadata

## Features

- ✅ Steady-state density matrix solver for double-lambda systems
- ✅ Third-order nonlinear susceptibility χ^(3) calculation
- ✅ FWM signal intensity computation
- ✅ 1D and 2D parameter sweeps (probe detuning, pump Rabi frequency, coupling detuning)
- ✅ CSV and JSON export with comprehensive metadata
- ✅ Data validation and consistency checking
- ✅ Support for both Rb-87 and Rb-85 isotopes
- ✅ Comprehensive unit and integration tests

## Quick Start

### Basic FWM Spectrum Calculation

```python
import numpy as np
from rb_eit import DoubleLambdaSystem, FWMSpectraCalculator

# Create a double-lambda system
system = DoubleLambdaSystem(
    isotope="Rb87",
    pump_rabi_frequency=2 * np.pi * 10e6,  # 10 MHz
    probe_rabi_frequency=2 * np.pi * 1e6,   # 1 MHz
)

# Initialize FWM calculator
calculator = FWMSpectraCalculator(
    system=system,
    number_density=1e17,      # atoms/m³
    interaction_length=0.01   # 1 cm
)

# Calculate χ^(3) spectrum
probe_detuning = np.linspace(-20e6, 20e6, 100) * 2 * np.pi
chi3_spectrum = calculator.compute_chi3_spectrum(probe_detuning)

# Calculate FWM intensity spectrum
intensity_spectrum = calculator.compute_fwm_intensity_spectrum(
    probe_detuning,
    pump_intensity=1e3,   # W/m²
    probe_intensity=1e2   # W/m²
)
```

### Parameter Sweeps

#### 1D Sweep: Probe Detuning

```python
from rb_eit import ParameterSweep

sweep = ParameterSweep(calculator)

result = sweep.sweep_probe_detuning(
    probe_detuning_min=-20e6 * 2 * np.pi,
    probe_detuning_max=20e6 * 2 * np.pi,
    num_points=100
)

print(f"Peak intensity: {np.max(result.intensity_values)}")
```

#### 1D Sweep: Pump Rabi Frequency

```python
result = sweep.sweep_pump_rabi_frequency(
    pump_rabi_min=2 * np.pi * 5e6,
    pump_rabi_max=2 * np.pi * 25e6,
    num_points=50
)
```

#### 1D Sweep: Coupling Detuning

```python
result = sweep.sweep_pump_detuning(
    pump_detuning_min=-30e6 * 2 * np.pi,
    pump_detuning_max=30e6 * 2 * np.pi,
    num_points=50
)
```

#### 2D Parameter Sweep

```python
probe_detuning_values = np.linspace(-10e6, 10e6, 25) * 2 * np.pi
pump_rabi_values = np.linspace(5e6, 20e6, 20) * 2 * np.pi

result = sweep.sweep_2d(
    param1_name='probe_detuning',
    param1_values=probe_detuning_values,
    param2_name='pump_rabi',
    param2_values=pump_rabi_values
)

# Result contains 2D arrays
print(f"Grid shape: {result.chi3_values.shape}")  # (25, 20)
```

### Data Export

#### Export to CSV

```python
from rb_eit import SpectraExporter

SpectraExporter.to_csv(result, "fwm_spectrum.csv")
```

CSV format includes:
- Metadata header with timestamp
- Parameter names and values
- Fixed parameters
- All spectral data (chi3 real/imag/magnitude/phase, FWM intensity)

#### Export to JSON

```python
SpectraExporter.to_json(result, "fwm_spectrum.json")
```

JSON format includes:
- Structured metadata
- Parameter arrays
- Fixed parameters dictionary
- Complete spectral data

#### Export to Multiple Formats

```python
filepaths = SpectraExporter.export_multiple_formats(
    result,
    "fwm_spectrum",
    formats=['csv', 'json']
)
# Returns: {'csv': 'fwm_spectrum.csv', 'json': 'fwm_spectrum.json'}
```

#### Load Exported Data

```python
data = SpectraExporter.from_json("fwm_spectrum.json")

# Access loaded data
parameter_values = data['parameter']['values']
chi3_complex = data['results']['chi3_complex']
intensity = data['results']['fwm_intensity']
metadata = data['metadata']
```

## API Reference

### FWMSpectraCalculator

```python
calculator = FWMSpectraCalculator(
    system: DoubleLambdaSystem,
    number_density: float = 1e17,
    interaction_length: float = 0.01,
    ground_dephasing_rate: float = 0.0
)
```

**Methods:**

- `compute_chi3_spectrum(probe_detuning_array, **params)` → χ^(3) array
- `compute_fwm_intensity_spectrum(probe_detuning_array, **params)` → intensity array
- `compute_pump_power_sweep(pump_rabi_array, **params)` → (rabi, chi3, intensity)
- `compute_coupling_detuning_sweep(pump_detuning_array, **params)` → (detuning, chi3, intensity)

### ParameterSweep

```python
sweep = ParameterSweep(calculator: FWMSpectraCalculator)
```

**Methods:**

- `sweep_probe_detuning(min, max, num_points, **params)` → ParameterSweepResult
- `sweep_pump_rabi_frequency(min, max, num_points, **params)` → ParameterSweepResult
- `sweep_pump_detuning(min, max, num_points, **params)` → ParameterSweepResult
- `sweep_2d(param1_name, param1_values, param2_name, param2_values, **params)` → ParameterSweepResult

### ParameterSweepResult

**Attributes:**

- `parameter_name`: str - Primary parameter name
- `parameter_values`: np.ndarray - Parameter values
- `chi3_values`: np.ndarray (complex) - χ^(3) values
- `intensity_values`: np.ndarray - FWM intensities
- `fixed_parameters`: dict - Fixed parameters
- `secondary_parameter_name`: str (optional) - For 2D sweeps
- `secondary_parameter_values`: np.ndarray (optional) - For 2D sweeps
- `metadata`: dict - Additional metadata

### SpectraExporter

**Static Methods:**

- `to_csv(result, filepath, include_metadata=True)` - Export to CSV
- `to_json(result, filepath, indent=2)` - Export to JSON
- `from_json(filepath)` → dict - Load from JSON
- `export_multiple_formats(result, base_filepath, formats=None)` → dict - Export to multiple formats

## Physical Background

### Third-Order Susceptibility

The third-order susceptibility χ^(3) describes the nonlinear response of the atomic medium to electromagnetic fields. In a double-lambda EIT system:

χ^(3) ∝ (n |μ|²/ε₀ℏ) × ρ₁₂ / (Δ + iΓ/2)Ω

where:
- n: atomic number density
- μ: dipole moment
- ρ₁₂: ground-state coherence
- Δ: detuning
- Γ: decay rate
- Ω: Rabi frequency

### FWM Signal Intensity

The FWM signal intensity is proportional to:

I_FWM ∝ |χ^(3)|² × I_pump² × I_probe × L²

where:
- I_pump: pump intensity
- I_probe: probe intensity
- L: interaction length

## Examples

See `examples/fwm_spectra_example.py` for comprehensive examples including:

1. χ^(3) spectrum calculation
2. FWM intensity spectrum
3. Pump power sweeps
4. Coupling detuning sweeps
5. 2D parameter sweeps
6. CSV export
7. JSON export
8. Multi-format export
9. Rb-85 system calculations

Run examples:
```bash
python examples/fwm_spectra_example.py
```

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test modules:
```bash
pytest tests/test_bloch_equations.py -v
pytest tests/test_fwm_spectra.py -v
pytest tests/test_parameter_sweep.py -v
pytest tests/test_exporters.py -v
```

## Performance Considerations

- Density matrix solver uses `scipy.optimize.fsolve` for robustness
- 1D sweeps: ~1-2 seconds for 100 points
- 2D sweeps: ~10-20 seconds for 25×20 grid
- Memory usage scales with grid size for 2D sweeps
- Consider using coarser grids for exploratory analysis

## Limitations

- Steady-state approximation (no time dynamics)
- Rotating wave approximation (RWA)
- No magnetic fields or Zeeman sublevels
- Simplified decay model (uniform decay rates)
- Weak probe approximation assumed in χ^(3) formula

## References

1. Boyd, R. W. "Nonlinear Optics" (2020)
2. Fleischhauer, M., Imamoglu, A., & Marangos, J. P. "Electromagnetically induced transparency: Optics in coherent media" Rev. Mod. Phys. 77, 633 (2005)
3. Steck, D. A. "Rubidium 87 D Line Data" (2001)
4. Steck, D. A. "Rubidium 85 D Line Data" (2001)

## Contributing

When adding new features:
1. Add comprehensive docstrings
2. Include unit tests with >90% coverage
3. Update this documentation
4. Follow existing code style conventions
5. Validate against physical expectations

## License

Same as parent project.
