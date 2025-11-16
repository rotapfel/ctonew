import numpy as np
from rb_eit import DoubleLambdaSystem
from rb_eit.visualization import (
    plot_detuning_rabi_heatmap,
    plot_3d_surface,
    plot_two_photon_resonance,
    plot_linewidth_vs_pump_power
)


def example_heatmap():
    print("Generating parameter space heatmap...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    plot_detuning_rabi_heatmap(
        system,
        probe_detuning_range=(-30e6, 30e6),
        pump_rabi_range=(1e6, 50e6),
        output_file="parameter_heatmap.png",
        show=False
    )
    print("Saved: parameter_heatmap.png")


def example_3d_surface():
    print("\nGenerating 3D surface plot...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    plot_3d_surface(
        system,
        probe_detuning_range=(-30e6, 30e6),
        pump_rabi_range=(1e6, 50e6),
        output_file="parameter_surface_3d.png",
        show=False
    )
    print("Saved: parameter_surface_3d.png")


def example_two_photon():
    print("\nGenerating two-photon resonance map...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    plot_two_photon_resonance(
        system,
        pump_detuning_range=(-30e6, 30e6),
        probe_detuning_range=(-30e6, 30e6),
        output_file="two_photon_resonance.png",
        show=False
    )
    print("Saved: two_photon_resonance.png")


def example_linewidth_vs_power():
    print("\nGenerating linewidth vs pump power plot...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    plot_linewidth_vs_pump_power(
        system,
        pump_rabi_range=(1e6, 50e6),
        output_file="linewidth_vs_pump.png",
        show=False
    )
    print("Saved: linewidth_vs_pump.png")


def example_rb85_heatmap():
    print("\nGenerating Rb-85 parameter heatmap...")
    
    system = DoubleLambdaSystem(
        isotope="Rb85",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    
    plot_detuning_rabi_heatmap(
        system,
        probe_detuning_range=(-30e6, 30e6),
        pump_rabi_range=(1e6, 50e6),
        output_file="parameter_heatmap_rb85.png",
        show=False
    )
    print("Saved: parameter_heatmap_rb85.png")


if __name__ == "__main__":
    example_heatmap()
    example_3d_surface()
    example_two_photon()
    example_linewidth_vs_power()
    example_rb85_heatmap()
    
    print("\n" + "=" * 60)
    print("All parameter sweep plots generated successfully!")
    print("=" * 60)
