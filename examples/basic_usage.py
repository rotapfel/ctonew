import numpy as np
from rb_eit import DoubleLambdaSystem, Rb87System, Rb85System

def example_rb87_system():
    print("=" * 60)
    print("Rb-87 Atomic System Example")
    print("=" * 60)
    
    system = Rb87System()
    print(f"\n{system}")
    print(f"Nuclear spin I = {system.nuclear_spin}")
    print(f"\nGround states:")
    for state in system.ground_states:
        print(f"  {state}")
    
    print(f"\nExcited states (5P_3/2):")
    for state in system.excited_states_5p32:
        print(f"  {state}")
    
    print(f"\nSample D2 transitions:")
    for trans in system.transitions_d2[:3]:
        print(f"  {trans}")
        print(f"    Dipole moment: {trans.dipole_moment:.3e} C·m")
        print(f"    Frequency: {trans.frequency/1e12:.3f} THz")

def example_rb85_system():
    print("\n" + "=" * 60)
    print("Rb-85 Atomic System Example")
    print("=" * 60)
    
    system = Rb85System()
    print(f"\n{system}")
    print(f"Nuclear spin I = {system.nuclear_spin}")
    print(f"\nGround states:")
    for state in system.ground_states:
        print(f"  {state}")

def example_double_lambda_rb87():
    print("\n" + "=" * 60)
    print("Rb-87 Double-Lambda EIT Configuration")
    print("=" * 60)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6,
        pump_detuning=0.0,
        probe_detuning=0.0
    )
    
    print(f"\n{system}")
    
    print(f"\nTransition 1: {system.transition_1}")
    print(f"  Dipole moment: {system.transition_1.dipole_moment:.3e} C·m")
    
    print(f"\nTransition 2: {system.transition_2}")
    print(f"  Dipole moment: {system.transition_2.dipole_moment:.3e} C·m")
    
    print(f"\nTwo-photon detuning: {system.two_photon_detuning()/1e6/2/np.pi:.3f} MHz")
    
    total_decay = system.atomic_system.total_decay_rate(system.excited_state)
    print(f"Total decay rate: {total_decay/1e6/2/np.pi:.3f} MHz")

def example_double_lambda_rb85():
    print("\n" + "=" * 60)
    print("Rb-85 Double-Lambda EIT Configuration")
    print("=" * 60)
    
    system = DoubleLambdaSystem(
        isotope="Rb85",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    
    print(f"\n{system}")

def example_custom_configuration():
    print("\n" + "=" * 60)
    print("Custom Rb-87 Configuration")
    print("=" * 60)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        ground_state_1_label="5S_1/2, F=1",
        ground_state_2_label="5S_1/2, F=2",
        excited_state_label="5P_3/2, F=1",
        pump_rabi_frequency=2 * np.pi * 20e6,
        probe_rabi_frequency=2 * np.pi * 5e6,
        pump_detuning=2 * np.pi * 2e6,
        probe_detuning=2 * np.pi * 1e6
    )
    
    print(f"\n{system}")
    
    system.set_pump_parameters(2 * np.pi * 25e6, 0.0)
    print("\nAfter updating pump parameters:")
    pump_rabi, probe_rabi = system.rabi_frequencies()
    print(f"  Pump Rabi frequency: {pump_rabi/1e6/2/np.pi:.2f} MHz")
    print(f"  Probe Rabi frequency: {probe_rabi/1e6/2/np.pi:.2f} MHz")

def example_eit_susceptibility():
    print("\n" + "=" * 60)
    print("EIT Susceptibility Calculation")
    print("=" * 60)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    detuning_scan = np.linspace(-20e6, 20e6, 100) * 2 * np.pi
    susceptibility = system.eit_susceptibility(detuning_scan)
    
    print(f"\nCalculated EIT susceptibility over {len(detuning_scan)} detuning points")
    print(f"Detuning range: {detuning_scan[0]/1e6/2/np.pi:.1f} to {detuning_scan[-1]/1e6/2/np.pi:.1f} MHz")
    print(f"Susceptibility at resonance: {susceptibility[50]:.3e}")

if __name__ == "__main__":
    example_rb87_system()
    example_rb85_system()
    example_double_lambda_rb87()
    example_double_lambda_rb85()
    example_custom_configuration()
    example_eit_susceptibility()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
