import numpy as np
from rb_eit import DoubleLambdaSystem
from rb_eit.visualization import plot_eit_spectrum, plot_comparison, plot_transmission_spectrum


def example_basic_spectrum():
    print("Generating basic EIT spectrum...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    plot_eit_spectrum(
        system,
        detuning_range=(-30e6, 30e6),
        output_file="eit_spectrum_rb87.png",
        show=False
    )
    print("Saved: eit_spectrum_rb87.png")


def example_comparison():
    print("\nGenerating comparison plot...")
    
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
    
    plot_comparison(
        systems=[system1, system2, system3],
        labels=['Pump: 5 MHz', 'Pump: 15 MHz', 'Pump: 30 MHz'],
        output_file="eit_comparison.png",
        show=False
    )
    print("Saved: eit_comparison.png")


def example_transmission():
    print("\nGenerating transmission spectrum...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 20e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    
    plot_transmission_spectrum(
        system,
        output_file="eit_transmission.png",
        show=False
    )
    print("Saved: eit_transmission.png")


def example_rb85_spectrum():
    print("\nGenerating Rb-85 spectrum...")
    
    system = DoubleLambdaSystem(
        isotope="Rb85",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    
    plot_eit_spectrum(
        system,
        output_file="eit_spectrum_rb85.png",
        show=False
    )
    print("Saved: eit_spectrum_rb85.png")


if __name__ == "__main__":
    example_basic_spectrum()
    example_comparison()
    example_transmission()
    example_rb85_spectrum()
    
    print("\n" + "=" * 60)
    print("All spectrum plots generated successfully!")
    print("=" * 60)
