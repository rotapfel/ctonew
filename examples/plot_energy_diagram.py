import numpy as np
from rb_eit import DoubleLambdaSystem
from rb_eit.visualization import plot_energy_level_diagram, plot_simple_level_diagram


def example_detailed_diagram():
    print("Generating detailed energy level diagram...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6,
        pump_detuning=2 * np.pi * 5e6,
        probe_detuning=2 * np.pi * 2e6
    )
    
    plot_energy_level_diagram(
        system,
        output_file="energy_diagram_detailed.png",
        show=False
    )
    print("Saved: energy_diagram_detailed.png")


def example_simple_diagram():
    print("\nGenerating simple energy level diagram...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    
    plot_simple_level_diagram(
        system,
        output_file="energy_diagram_simple.png",
        show=False
    )
    print("Saved: energy_diagram_simple.png")


def example_rb85_diagram():
    print("\nGenerating Rb-85 energy diagram...")
    
    system = DoubleLambdaSystem(
        isotope="Rb85",
        pump_rabi_frequency=2 * np.pi * 20e6,
        probe_rabi_frequency=2 * np.pi * 3e6,
        pump_detuning=0.0,
        probe_detuning=0.0
    )
    
    plot_energy_level_diagram(
        system,
        output_file="energy_diagram_rb85.png",
        show=False
    )
    print("Saved: energy_diagram_rb85.png")


def example_custom_config():
    print("\nGenerating custom configuration diagram...")
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        ground_state_1_label="5S_1/2, F=1",
        ground_state_2_label="5S_1/2, F=2",
        excited_state_label="5P_3/2, F=1",
        pump_rabi_frequency=2 * np.pi * 25e6,
        probe_rabi_frequency=2 * np.pi * 5e6,
        pump_detuning=2 * np.pi * 10e6,
        probe_detuning=2 * np.pi * 5e6
    )
    
    plot_energy_level_diagram(
        system,
        output_file="energy_diagram_custom.png",
        show=False
    )
    print("Saved: energy_diagram_custom.png")


if __name__ == "__main__":
    example_detailed_diagram()
    example_simple_diagram()
    example_rb85_diagram()
    example_custom_config()
    
    print("\n" + "=" * 60)
    print("All energy diagrams generated successfully!")
    print("=" * 60)
