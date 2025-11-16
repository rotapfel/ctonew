# Rb Double-Lambda EIT Atomic System Model

A Python package for modeling Rubidium (Rb-87 and Rb-85) atomic systems in double-lambda Electromagnetically Induced Transparency (EIT) configurations, with comprehensive visualization capabilities.

## Features

- Data models for atomic levels, transitions, decay rates, and dipole moments
- Realistic Rb-87 and Rb-85 parameters with literature-based values
- Utilities for constructing double-lambda EIT configurations
- Parameter validation and consistency checking
- **Publication-quality visualization suite with Matplotlib**
- **Interactive visualizations with Plotly (HTML exports)**
- **Energy level diagrams with laser coupling arrows**
- **2D heatmaps and 3D surfaces for parameter space exploration**
- **Command-line interface (CLI) for quick plot generation**
- Comprehensive unit tests

## Installation

```bash
pip install -e .
```

This will install the package along with all dependencies including Matplotlib, Plotly, and Click for CLI support.

## Quick Start

### Python API

```python
import numpy as np
from rb_eit import DoubleLambdaSystem
from rb_eit.visualization import plot_eit_spectrum, plot_energy_level_diagram

# Create an Rb-87 double-lambda system
system = DoubleLambdaSystem(
    isotope="Rb87",
    pump_rabi_frequency=2 * np.pi * 10e6,  # 10 MHz
    probe_rabi_frequency=2 * np.pi * 1e6,   # 1 MHz
)

# Generate EIT spectrum plot
plot_eit_spectrum(system, output_file="eit_spectrum.png")

# Generate energy level diagram
plot_energy_level_diagram(system, output_file="energy_diagram.png")
```

### Command-Line Interface

```bash
# Generate EIT spectrum
fwm-sim spectrum --isotope Rb87 --pump-rabi 10.0 --probe-rabi 1.0 -o spectrum.png

# Generate energy level diagram
fwm-sim energy-diagram --isotope Rb87 --pump-rabi 10.0 -o energy.png

# Generate parameter space heatmap
fwm-sim heatmap --isotope Rb87 --probe-rabi 1.0 -o heatmap.png

# Generate interactive visualization (HTML)
fwm-sim interactive --isotope Rb87 --pump-rabi 10.0 -o interactive.html
```

## Visualization Capabilities

### Static Plots (Matplotlib)

- **EIT Spectra**: Absorption and dispersion vs probe detuning
- **Transmission Spectra**: Transparency window visualization
- **Comparison Plots**: Multiple configurations side-by-side
- **Energy Level Diagrams**: Detailed atomic structure with laser couplings
- **Parameter Heatmaps**: 2D parameter space visualization
- **3D Surfaces**: Parameter dependencies in 3D
- **Two-Photon Resonance Maps**: Pump-probe detuning correlation
- **Linewidth Analysis**: EIT window vs pump power

### Interactive Plots (Plotly)

- **Interactive Spectra**: Real-time parameter adjustment with sliders
- **Interactive Heatmaps**: Zoomable, hoverable parameter space
- **Interactive 3D Surfaces**: Rotatable 3D visualizations
- **Comparison Tools**: Toggle between multiple configurations

## Examples

The `examples/` directory contains comprehensive demonstration scripts:

- `plot_eit_spectrum.py` - Static spectrum plots
- `plot_energy_diagram.py` - Energy level diagrams
- `parameter_sweep.py` - Parameter space exploration
- `interactive_exploration.py` - Interactive Plotly visualizations
- `cli_usage_examples.sh` - CLI command examples

Run any example:
```bash
python examples/plot_eit_spectrum.py
```

## CLI Commands

The `fwm-sim` command provides several subcommands:

- `spectrum` - Generate EIT spectrum plots
- `energy-diagram` - Generate energy level diagrams
- `heatmap` - Generate parameter space heatmaps
- `surface` - Generate 3D surface plots
- `interactive` - Generate interactive spectrum with sliders
- `interactive-heatmap` - Generate interactive heatmap
- `interactive-surface` - Generate interactive 3D surface

Use `fwm-sim --help` or `fwm-sim <command> --help` for detailed options.

## Configuration Files

You can use JSON configuration files with the CLI:

```json
{
  "isotope": "Rb87",
  "pump_rabi_frequency": 62831853.071795866,
  "probe_rabi_frequency": 6283185.307179587,
  "pump_detuning": 0.0,
  "probe_detuning": 0.0
}
```

Then use: `fwm-sim spectrum --config config.json -o output.png`

## References

- Steck, D. A. "Rubidium 87 D Line Data" (2001)
- Steck, D. A. "Rubidium 85 D Line Data" (2001)
- Fleischhauer, M., Imamoglu, A., & Marangos, J. P. "Electromagnetically induced transparency: Optics in coherent media" Rev. Mod. Phys. 77, 633 (2005)
