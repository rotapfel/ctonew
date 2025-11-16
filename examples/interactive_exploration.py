import numpy as np
from rb_eit import DoubleLambdaSystem
from rb_eit.visualization import (
    create_interactive_eit_spectrum,
    create_interactive_heatmap,
    create_interactive_3d_surface,
    create_parameter_sweep_comparison
)


def example_interactive_spectrum():
    print("Generating interactive EIT spectrum...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    create_interactive_eit_spectrum(
        system,
        pump_rabi_range=(1e6, 50e6),
        probe_rabi_range=(0.1e6, 10e6),
        output_file="interactive_spectrum.html"
    )
    print("Saved: interactive_spectrum.html")


def example_interactive_heatmap():
    print("\nGenerating interactive heatmap...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    create_interactive_heatmap(
        system,
        probe_detuning_range=(-30e6, 30e6),
        pump_rabi_range=(1e6, 50e6),
        output_file="interactive_heatmap.html"
    )
    print("Saved: interactive_heatmap.html")


def example_interactive_3d():
    print("\nGenerating interactive 3D surface...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    create_interactive_3d_surface(
        system,
        probe_detuning_range=(-30e6, 30e6),
        pump_rabi_range=(1e6, 50e6),
        output_file="interactive_surface_3d.html"
    )
    print("Saved: interactive_surface_3d.html")


def example_interactive_comparison():
    print("\nGenerating interactive comparison...")
    
    system1 = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 5e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    system2 = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    system3 = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 30e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    create_parameter_sweep_comparison(
        systems=[system1, system2, system3],
        labels=['Pump: 5 MHz', 'Pump: 15 MHz', 'Pump: 30 MHz'],
        output_file="interactive_comparison.html"
    )
    print("Saved: interactive_comparison.html")


def example_rb85_interactive():
    print("\nGenerating Rb-85 interactive spectrum...")
    
    system = DoubleLambdaSystem(
        isotope="Rb85",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    
    create_interactive_eit_spectrum(
        system,
        pump_rabi_range=(1e6, 50e6),
        probe_rabi_range=(0.1e6, 10e6),
        output_file="interactive_spectrum_rb85.html"
    )
    print("Saved: interactive_spectrum_rb85.html")


if __name__ == "__main__":
    example_interactive_spectrum()
    example_interactive_heatmap()
    example_interactive_3d()
    example_interactive_comparison()
    example_rb85_interactive()
    
    print("\n" + "=" * 60)
    print("All interactive visualizations generated successfully!")
    print("Open the HTML files in a web browser to explore.")
    print("=" * 60)
