#!/bin/bash

# CLI Usage Examples for fwm-sim

echo "==================================================================="
echo "FWM-SIM CLI Usage Examples"
echo "==================================================================="

# Basic spectrum plot
echo -e "\n1. Generating basic EIT spectrum..."
fwm-sim spectrum --isotope Rb87 --pump-rabi 10.0 --probe-rabi 1.0 \
    --output cli_spectrum_basic.png --no-show

# Spectrum with custom detuning range
echo -e "\n2. Generating spectrum with custom detuning range..."
fwm-sim spectrum --isotope Rb87 --pump-rabi 15.0 --probe-rabi 2.0 \
    --detuning-min -50.0 --detuning-max 50.0 \
    --output cli_spectrum_wide.png --no-show

# Energy diagram (detailed)
echo -e "\n3. Generating detailed energy level diagram..."
fwm-sim energy-diagram --isotope Rb87 --pump-rabi 10.0 --probe-rabi 1.0 \
    --output cli_energy_detailed.png --no-show

# Energy diagram (simple)
echo -e "\n4. Generating simple energy level diagram..."
fwm-sim energy-diagram --isotope Rb87 --pump-rabi 10.0 --probe-rabi 1.0 \
    --simple --output cli_energy_simple.png --no-show

# Parameter space heatmap
echo -e "\n5. Generating parameter space heatmap..."
fwm-sim heatmap --isotope Rb87 --probe-rabi 1.0 \
    --detuning-min -30.0 --detuning-max 30.0 \
    --pump-min 1.0 --pump-max 50.0 \
    --output cli_heatmap.png --no-show

# 3D surface plot
echo -e "\n6. Generating 3D surface plot..."
fwm-sim surface --isotope Rb87 --probe-rabi 1.0 \
    --detuning-min -30.0 --detuning-max 30.0 \
    --pump-min 1.0 --pump-max 50.0 \
    --output cli_surface_3d.png --no-show

# Interactive spectrum with sliders
echo -e "\n7. Generating interactive spectrum (HTML)..."
fwm-sim interactive --isotope Rb87 --pump-rabi 10.0 --probe-rabi 1.0 \
    --pump-min 1.0 --pump-max 50.0 \
    --probe-min 0.1 --probe-max 10.0 \
    --output cli_interactive_spectrum.html

# Interactive heatmap
echo -e "\n8. Generating interactive heatmap (HTML)..."
fwm-sim interactive-heatmap --isotope Rb87 --probe-rabi 1.0 \
    --detuning-min -30.0 --detuning-max 30.0 \
    --pump-min 1.0 --pump-max 50.0 \
    --output cli_interactive_heatmap.html

# Interactive 3D surface
echo -e "\n9. Generating interactive 3D surface (HTML)..."
fwm-sim interactive-surface --isotope Rb87 --probe-rabi 1.0 \
    --detuning-min -30.0 --detuning-max 30.0 \
    --pump-min 1.0 --pump-max 50.0 \
    --output cli_interactive_surface.html

# Using configuration file
echo -e "\n10. Generating spectrum from config file..."
fwm-sim spectrum --config config_rb87.json \
    --output cli_spectrum_from_config.png --no-show

# Rb-85 examples
echo -e "\n11. Generating Rb-85 spectrum..."
fwm-sim spectrum --isotope Rb85 --pump-rabi 15.0 --probe-rabi 2.0 \
    --output cli_spectrum_rb85.png --no-show

echo -e "\n12. Generating Rb-85 energy diagram..."
fwm-sim energy-diagram --isotope Rb85 --pump-rabi 15.0 --probe-rabi 2.0 \
    --output cli_energy_rb85.png --no-show

echo -e "\n==================================================================="
echo "All CLI examples completed!"
echo "Check the generated PNG and HTML files."
echo "==================================================================="
