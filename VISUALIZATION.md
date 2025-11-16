# Visualization Suite Documentation

This document provides comprehensive documentation for the visualization capabilities of the Rb EIT package.

## Overview

The visualization suite provides both static (Matplotlib) and interactive (Plotly) plotting capabilities for analyzing and exploring EIT physics in Rubidium atomic systems.

## Table of Contents

1. [Static Plots (Matplotlib)](#static-plots-matplotlib)
2. [Interactive Plots (Plotly)](#interactive-plots-plotly)
3. [Energy Level Diagrams](#energy-level-diagrams)
4. [Parameter Space Exploration](#parameter-space-exploration)
5. [Command-Line Interface](#command-line-interface)
6. [Python API Examples](#python-api-examples)

---

## Static Plots (Matplotlib)

### EIT Spectrum

Generate absorption and dispersion spectra:

```python
from rb_eit import DoubleLambdaSystem
from rb_eit.visualization import plot_eit_spectrum

system = DoubleLambdaSystem(isotope="Rb87")
plot_eit_spectrum(
    system,
    detuning_range=(-30e6, 30e6),
    num_points=500,
    output_file="spectrum.png"
)
```

**Features:**
- Dual-panel plot showing absorption (top) and dispersion (bottom)
- Probe detuning scan range configurable
- Automatic labeling with system parameters
- Publication-quality output at 300 DPI

### Transmission Spectrum

Visualize the EIT transparency window:

```python
from rb_eit.visualization import plot_transmission_spectrum

plot_transmission_spectrum(
    system,
    output_file="transmission.png"
)
```

**Features:**
- Normalized transmission coefficient
- Clear visualization of transparency window
- Parameter annotations

### Comparison Plots

Compare multiple configurations:

```python
from rb_eit.visualization import plot_comparison

system1 = DoubleLambdaSystem(pump_rabi_frequency=2*np.pi*5e6)
system2 = DoubleLambdaSystem(pump_rabi_frequency=2*np.pi*15e6)
system3 = DoubleLambdaSystem(pump_rabi_frequency=2*np.pi*30e6)

plot_comparison(
    systems=[system1, system2, system3],
    labels=['5 MHz', '15 MHz', '30 MHz'],
    output_file="comparison.png"
)
```

**Features:**
- Overlay multiple spectra
- Color-coded traces with legend
- Shared axes for easy comparison

### Linewidth Analysis

Analyze EIT window width vs pump power:

```python
from rb_eit.visualization import plot_linewidth_vs_pump_power

plot_linewidth_vs_pump_power(
    system,
    pump_rabi_range=(1e6, 50e6),
    output_file="linewidth.png"
)
```

**Features:**
- FWHM calculation of transparency window
- Pump power dependence
- Power broadening visualization

---

## Interactive Plots (Plotly)

### Interactive Spectrum

Create interactive plots with parameter sliders:

```python
from rb_eit.visualization import create_interactive_eit_spectrum

create_interactive_eit_spectrum(
    system,
    pump_rabi_range=(1e6, 50e6),
    probe_rabi_range=(0.1e6, 10e6),
    output_file="interactive_spectrum.html"
)
```

**Features:**
- Dual sliders for pump and probe Rabi frequencies
- Real-time spectrum updates
- Zoomable, pannable plots
- Hover tooltips with values
- Export to HTML for sharing

### Interactive Heatmap

Explore parameter space interactively:

```python
from rb_eit.visualization import create_interactive_heatmap

create_interactive_heatmap(
    system,
    probe_detuning_range=(-30e6, 30e6),
    pump_rabi_range=(1e6, 50e6),
    output_file="interactive_heatmap.html"
)
```

**Features:**
- Color-coded absorption map
- Zoom and pan capabilities
- Hover for exact values
- Colorbar with units

### Interactive 3D Surface

Visualize parameter dependencies in 3D:

```python
from rb_eit.visualization import create_interactive_3d_surface

create_interactive_3d_surface(
    system,
    output_file="interactive_3d.html"
)
```

**Features:**
- Rotatable 3D surface
- Zoom and pan
- Color-coded height
- Camera angle controls

### Interactive Comparison

Compare multiple configurations interactively:

```python
from rb_eit.visualization import create_parameter_sweep_comparison

create_parameter_sweep_comparison(
    systems=[system1, system2, system3],
    labels=['Config 1', 'Config 2', 'Config 3'],
    output_file="interactive_comparison.html"
)
```

---

## Energy Level Diagrams

### Detailed Energy Diagram

Create comprehensive energy level diagrams:

```python
from rb_eit.visualization import plot_energy_level_diagram

plot_energy_level_diagram(
    system,
    output_file="energy_diagram.png"
)
```

**Features:**
- Energy levels with quantum numbers
- Laser coupling arrows (pump and probe)
- Rabi frequency and detuning labels
- Decay rate annotations
- Energy axis in MHz

### Simple Level Diagram

Create simplified schematic diagrams:

```python
from rb_eit.visualization import plot_simple_level_diagram

plot_simple_level_diagram(
    system,
    output_file="simple_diagram.png"
)
```

**Features:**
- Clean, minimalist design
- Focus on level structure
- Ideal for presentations

---

## Parameter Space Exploration

### 2D Heatmap

Visualize parameter dependencies:

```python
from rb_eit.visualization import plot_detuning_rabi_heatmap

plot_detuning_rabi_heatmap(
    system,
    probe_detuning_range=(-30e6, 30e6),
    pump_rabi_range=(1e6, 50e6),
    num_points=(100, 50),
    output_file="heatmap.png"
)
```

**Features:**
- Color-coded absorption map
- Contour lines for clarity
- Automatic axis labeling

### 3D Surface Plot

Create 3D surface visualizations:

```python
from rb_eit.visualization import plot_3d_surface

plot_3d_surface(
    system,
    output_file="surface_3d.png"
)
```

**Features:**
- 3D surface representation
- Configurable viewing angle
- Color-coded height
- High-quality rendering

### Two-Photon Resonance Map

Visualize two-photon resonance conditions:

```python
from rb_eit.visualization import plot_two_photon_resonance

plot_two_photon_resonance(
    system,
    pump_detuning_range=(-30e6, 30e6),
    probe_detuning_range=(-30e6, 30e6),
    output_file="two_photon.png"
)
```

**Features:**
- Pump vs probe detuning
- Two-photon resonance line
- Absorption map background

---

## Command-Line Interface

### Basic Usage

```bash
fwm-sim --help
```

### Generate Spectrum

```bash
fwm-sim spectrum \
    --isotope Rb87 \
    --pump-rabi 10.0 \
    --probe-rabi 1.0 \
    --detuning-min -30.0 \
    --detuning-max 30.0 \
    -o spectrum.png \
    --no-show
```

### Generate Energy Diagram

```bash
fwm-sim energy-diagram \
    --isotope Rb87 \
    --pump-rabi 10.0 \
    --probe-rabi 1.0 \
    -o energy.png
```

Use `--simple` flag for simplified diagram.

### Generate Heatmap

```bash
fwm-sim heatmap \
    --isotope Rb87 \
    --probe-rabi 1.0 \
    --pump-min 1.0 \
    --pump-max 50.0 \
    -o heatmap.png
```

### Generate 3D Surface

```bash
fwm-sim surface \
    --isotope Rb87 \
    --probe-rabi 1.0 \
    -o surface.png
```

### Generate Interactive Plot

```bash
fwm-sim interactive \
    --isotope Rb87 \
    --pump-rabi 10.0 \
    --probe-rabi 1.0 \
    --pump-min 1.0 \
    --pump-max 50.0 \
    -o interactive.html
```

### Using Configuration Files

Create a JSON configuration file:

```json
{
  "isotope": "Rb87",
  "pump_rabi_frequency": 62831853.071795866,
  "probe_rabi_frequency": 6283185.307179587,
  "pump_detuning": 0.0,
  "probe_detuning": 0.0
}
```

Use with CLI:

```bash
fwm-sim spectrum --config config.json -o output.png
```

---

## Python API Examples

### Complete Workflow Example

```python
import numpy as np
from rb_eit import DoubleLambdaSystem
from rb_eit.visualization import (
    plot_eit_spectrum,
    plot_energy_level_diagram,
    plot_detuning_rabi_heatmap,
    create_interactive_eit_spectrum
)

# Create system
system = DoubleLambdaSystem(
    isotope="Rb87",
    pump_rabi_frequency=2 * np.pi * 10e6,
    probe_rabi_frequency=2 * np.pi * 1e6,
    pump_detuning=0.0,
    probe_detuning=0.0
)

# Generate static plots
plot_eit_spectrum(system, output_file="spectrum.png", show=False)
plot_energy_level_diagram(system, output_file="energy.png", show=False)
plot_detuning_rabi_heatmap(system, output_file="heatmap.png", show=False)

# Generate interactive plot
create_interactive_eit_spectrum(system, output_file="interactive.html")

print("All visualizations generated!")
```

### Parameter Sweep Example

```python
import numpy as np
from rb_eit import DoubleLambdaSystem
from rb_eit.visualization import plot_comparison

# Create multiple systems with different pump powers
systems = []
labels = []
pump_powers = [5, 10, 15, 20, 30]

for power in pump_powers:
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * power * 1e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    systems.append(system)
    labels.append(f'Pump: {power} MHz')

# Create comparison plot
plot_comparison(
    systems=systems,
    labels=labels,
    output_file="pump_power_sweep.png",
    show=True
)
```

### Custom Figsize and Resolution

```python
from rb_eit.visualization import plot_eit_spectrum

plot_eit_spectrum(
    system,
    figsize=(12, 8),
    num_points=1000,
    output_file="high_res_spectrum.png",
    show=False
)
```

---

## Plot Customization

### Common Parameters

All plotting functions support:

- `output_file`: Path to save the plot (PNG, PDF, etc.)
- `show`: Whether to display the plot (default: True)
- `figsize`: Tuple (width, height) in inches
- `num_points`: Number of points for scans

### Matplotlib Plots

Additional parameters:
- `detuning_range`: Tuple (min, max) in Hz
- `cmap`: Colormap name for heatmaps

### Plotly Plots

Additional parameters:
- All output to HTML files
- Inherently interactive
- Support for sliders and dropdowns

---

## Performance Tips

1. **Reduce num_points for faster rendering**: Use fewer points for quick previews
2. **Use --no-show flag in CLI**: Skip display for batch processing
3. **Generate interactive plots last**: They take longer to compute
4. **Parallel processing**: Generate multiple plots in separate scripts

---

## Testing

Run visualization tests:

```bash
pytest tests/test_visualization.py -v
```

All tests verify:
- Functions execute without errors
- Files are created
- File sizes are reasonable
- HTML contains expected content

---

## Troubleshooting

### Issue: Plots not displaying

**Solution:** Use `show=True` or remove `--no-show` flag

### Issue: Low resolution plots

**Solution:** Increase DPI or use larger figsize:
```python
plot_eit_spectrum(system, figsize=(14, 10), output_file="output.png")
```

### Issue: Interactive plots too slow

**Solution:** Reduce num_points:
```python
create_interactive_eit_spectrum(system, num_points=200, output_file="output.html")
```

### Issue: Memory errors on large parameter sweeps

**Solution:** Reduce resolution:
```python
plot_detuning_rabi_heatmap(system, num_points=(50, 30), output_file="output.png")
```

---

## File Format Support

### Static Plots (Matplotlib)

Supported formats:
- PNG (default, recommended for web)
- PDF (vector, recommended for publications)
- SVG (vector, recommended for editing)
- JPG (compressed, not recommended)

Usage:
```python
plot_eit_spectrum(system, output_file="plot.pdf")
```

### Interactive Plots (Plotly)

Supported formats:
- HTML (default, interactive)
- PNG/PDF (static export, requires kaleido)

---

## Best Practices

1. **Publication-quality plots**: Use PDF format with figsize=(10, 6) or larger
2. **Web display**: Use PNG at 300 DPI
3. **Interactive exploration**: Use Plotly HTML exports
4. **Batch processing**: Use CLI with --no-show flag
5. **Documentation**: Use simple energy diagrams
6. **Research**: Use detailed energy diagrams with all parameters

---

## Additional Resources

- [Examples Directory](examples/): Complete working examples
- [Test Suite](tests/test_visualization.py): Usage examples in tests
- [CLI Help](cli.py): Command-line interface documentation
- [Main README](README.md): Package overview

---

## Contributing

When adding new visualization features:

1. Add function to appropriate module
2. Export in `__init__.py`
3. Add CLI command if applicable
4. Write tests in `test_visualization.py`
5. Update this documentation
6. Add example script

---

## Citation

If you use these visualization tools in your research, please cite:

```
Rb EIT Visualization Suite
https://github.com/yourusername/rb_eit
```
