#!/usr/bin/env python3
"""
Full Visualization Suite Demonstration

This script demonstrates all visualization capabilities of the rb_eit package.
It generates:
- Static plots with Matplotlib (PNG)
- Interactive plots with Plotly (HTML)
- Energy level diagrams
- Parameter space visualizations
- Comparison plots
"""

import numpy as np
from rb_eit import DoubleLambdaSystem
from rb_eit.visualization import (
    plot_eit_spectrum,
    plot_comparison,
    plot_transmission_spectrum,
    plot_linewidth_vs_pump_power,
    plot_energy_level_diagram,
    plot_simple_level_diagram,
    plot_detuning_rabi_heatmap,
    plot_3d_surface,
    plot_two_photon_resonance,
    create_interactive_eit_spectrum,
    create_interactive_heatmap,
    create_interactive_3d_surface,
    create_parameter_sweep_comparison
)


def banner(text):
    """Print a formatted banner"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def main():
    print("\n" + "=" * 70)
    print("  Rb EIT Visualization Suite - Full Demonstration")
    print("=" * 70)
    
    # Create main system
    banner("Creating Rb-87 Double-Lambda EIT System")
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6,
        pump_detuning=0.0,
        probe_detuning=0.0
    )
    print(system)
    
    # Static Matplotlib Plots
    banner("Generating Static Plots (Matplotlib)")
    
    print("\n1. EIT Spectrum (absorption and dispersion)...")
    plot_eit_spectrum(
        system,
        detuning_range=(-30e6, 30e6),
        output_file="demo_eit_spectrum.png",
        show=False
    )
    print("   ✓ Saved: demo_eit_spectrum.png")
    
    print("\n2. Transmission Spectrum...")
    plot_transmission_spectrum(
        system,
        output_file="demo_transmission.png",
        show=False
    )
    print("   ✓ Saved: demo_transmission.png")
    
    print("\n3. Comparing different pump powers...")
    systems_pump = [
        DoubleLambdaSystem(isotope="Rb87", pump_rabi_frequency=2*np.pi*5e6, probe_rabi_frequency=2*np.pi*1e6),
        DoubleLambdaSystem(isotope="Rb87", pump_rabi_frequency=2*np.pi*15e6, probe_rabi_frequency=2*np.pi*1e6),
        DoubleLambdaSystem(isotope="Rb87", pump_rabi_frequency=2*np.pi*30e6, probe_rabi_frequency=2*np.pi*1e6),
    ]
    plot_comparison(
        systems=systems_pump,
        labels=['Pump: 5 MHz', 'Pump: 15 MHz', 'Pump: 30 MHz'],
        output_file="demo_pump_comparison.png",
        show=False
    )
    print("   ✓ Saved: demo_pump_comparison.png")
    
    print("\n4. Linewidth vs Pump Power...")
    plot_linewidth_vs_pump_power(
        system,
        pump_rabi_range=(1e6, 50e6),
        num_points=30,
        output_file="demo_linewidth_vs_pump.png",
        show=False
    )
    print("   ✓ Saved: demo_linewidth_vs_pump.png")
    
    # Energy Level Diagrams
    banner("Generating Energy Level Diagrams")
    
    print("\n5. Detailed energy level diagram...")
    plot_energy_level_diagram(
        system,
        output_file="demo_energy_detailed.png",
        show=False
    )
    print("   ✓ Saved: demo_energy_detailed.png")
    
    print("\n6. Simple energy level diagram...")
    plot_simple_level_diagram(
        system,
        output_file="demo_energy_simple.png",
        show=False
    )
    print("   ✓ Saved: demo_energy_simple.png")
    
    # Parameter Space Visualizations
    banner("Generating Parameter Space Visualizations")
    
    print("\n7. 2D Heatmap (Detuning vs Pump Rabi)...")
    plot_detuning_rabi_heatmap(
        system,
        probe_detuning_range=(-30e6, 30e6),
        pump_rabi_range=(1e6, 50e6),
        num_points=(80, 40),
        output_file="demo_heatmap.png",
        show=False
    )
    print("   ✓ Saved: demo_heatmap.png")
    
    print("\n8. 3D Surface Plot...")
    plot_3d_surface(
        system,
        probe_detuning_range=(-30e6, 30e6),
        pump_rabi_range=(1e6, 50e6),
        num_points=(60, 30),
        output_file="demo_3d_surface.png",
        show=False
    )
    print("   ✓ Saved: demo_3d_surface.png")
    
    print("\n9. Two-Photon Resonance Map...")
    plot_two_photon_resonance(
        system,
        pump_detuning_range=(-30e6, 30e6),
        probe_detuning_range=(-30e6, 30e6),
        num_points=(80, 80),
        output_file="demo_two_photon.png",
        show=False
    )
    print("   ✓ Saved: demo_two_photon.png")
    
    # Interactive Plotly Visualizations
    banner("Generating Interactive Visualizations (Plotly/HTML)")
    
    print("\n10. Interactive EIT Spectrum with sliders...")
    create_interactive_eit_spectrum(
        system,
        pump_rabi_range=(1e6, 50e6),
        probe_rabi_range=(0.1e6, 10e6),
        num_points=300,
        output_file="demo_interactive_spectrum.html"
    )
    print("   ✓ Saved: demo_interactive_spectrum.html")
    
    print("\n11. Interactive Heatmap...")
    create_interactive_heatmap(
        system,
        probe_detuning_range=(-30e6, 30e6),
        pump_rabi_range=(1e6, 50e6),
        num_points=(100, 60),
        output_file="demo_interactive_heatmap.html"
    )
    print("   ✓ Saved: demo_interactive_heatmap.html")
    
    print("\n12. Interactive 3D Surface...")
    create_interactive_3d_surface(
        system,
        probe_detuning_range=(-30e6, 30e6),
        pump_rabi_range=(1e6, 50e6),
        num_points=(80, 50),
        output_file="demo_interactive_3d.html"
    )
    print("   ✓ Saved: demo_interactive_3d.html")
    
    print("\n13. Interactive Comparison...")
    create_parameter_sweep_comparison(
        systems=systems_pump,
        labels=['Pump: 5 MHz', 'Pump: 15 MHz', 'Pump: 30 MHz'],
        num_points=300,
        output_file="demo_interactive_comparison.html"
    )
    print("   ✓ Saved: demo_interactive_comparison.html")
    
    # Rb-85 Examples
    banner("Generating Rb-85 Examples")
    
    print("\n14. Rb-85 EIT Spectrum...")
    system_rb85 = DoubleLambdaSystem(
        isotope="Rb85",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    plot_eit_spectrum(
        system_rb85,
        output_file="demo_rb85_spectrum.png",
        show=False
    )
    print("   ✓ Saved: demo_rb85_spectrum.png")
    
    print("\n15. Rb-85 Energy Diagram...")
    plot_energy_level_diagram(
        system_rb85,
        output_file="demo_rb85_energy.png",
        show=False
    )
    print("   ✓ Saved: demo_rb85_energy.png")
    
    # Summary
    banner("Summary")
    print("\nGenerated 15 visualizations:")
    print("  • 9 static plots (PNG)")
    print("  • 4 interactive visualizations (HTML)")
    print("  • 2 Rb-85 examples")
    print("\nStatic plots are publication-quality (300 DPI)")
    print("Interactive plots can be opened in any web browser")
    print("\nAll files are prefixed with 'demo_' for easy identification.")
    
    print("\n" + "=" * 70)
    print("  Demonstration Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
