import numpy as np
from rb_eit import DoubleLambdaSystem, BlochSolver, TwoLevelBlochSolver

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def example_two_level_system():
    print("=" * 60)
    print("Two-Level System Example")
    print("=" * 60)
    
    omega = 2 * np.pi * 10e6
    delta = 0.0
    gamma = 2 * np.pi * 6e6
    
    solver = TwoLevelBlochSolver(
        rabi_frequency=omega,
        detuning=delta,
        decay_rate=gamma
    )
    
    rho = solver.solve_steady_state()
    
    print(f"\nRabi frequency: {omega / (2 * np.pi) / 1e6:.2f} MHz")
    print(f"Detuning: {delta / (2 * np.pi) / 1e6:.2f} MHz")
    print(f"Decay rate: {gamma / (2 * np.pi) / 1e6:.2f} MHz")
    print(f"\nGround state population: {rho[0, 0].real:.4f}")
    print(f"Excited state population: {rho[1, 1].real:.4f}")
    print(f"Coherence magnitude: {abs(rho[0, 1]):.4f}")
    
    validation = solver.validate_density_matrix(rho)
    print(f"\nDensity matrix validation:")
    for key, value in validation.items():
        print(f"  {key}: {value}")


def example_three_level_system():
    print("\n" + "=" * 60)
    print("Three-Level Double-Lambda System Example")
    print("=" * 60)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6,
        pump_detuning=0.0,
        probe_detuning=0.0
    )
    
    print(f"\nSystem configuration:")
    print(f"  Ground state 1: {system.ground_state_1.label}")
    print(f"  Ground state 2: {system.ground_state_2.label}")
    print(f"  Excited state: {system.excited_state.label}")
    print(f"  Pump Rabi frequency: {system.pump.rabi_frequency / (2 * np.pi) / 1e6:.2f} MHz")
    print(f"  Probe Rabi frequency: {system.probe.rabi_frequency / (2 * np.pi) / 1e6:.2f} MHz")
    
    solver = BlochSolver(system)
    
    print(f"\nDecay rates:")
    print(f"  Total: {solver.decay_rates['gamma_total'] / (2 * np.pi) / 1e6:.2f} MHz")
    print(f"  To state 1: {solver.decay_rates['gamma_e1'] / (2 * np.pi) / 1e6:.2f} MHz")
    print(f"  To state 2: {solver.decay_rates['gamma_e2'] / (2 * np.pi) / 1e6:.2f} MHz")
    
    rho = solver.solve_steady_state()
    
    print(f"\nSteady-state populations:")
    print(f"  Ground state 1: {rho[0, 0].real:.6f}")
    print(f"  Ground state 2: {rho[1, 1].real:.6f}")
    print(f"  Excited state: {rho[2, 2].real:.6f}")
    
    print(f"\nCoherences:")
    print(f"  |rho_12|: {abs(rho[0, 1]):.6e}")
    print(f"  |rho_13|: {abs(rho[0, 2]):.6e}")
    print(f"  |rho_23|: {abs(rho[1, 2]):.6e}")
    
    validation = solver.validate_density_matrix(rho)
    print(f"\nDensity matrix validation:")
    for key, value in validation.items():
        print(f"  {key}: {value}")


def example_probe_detuning_sweep():
    print("\n" + "=" * 60)
    print("Probe Detuning Sweep Example")
    print("=" * 60)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6,
        pump_detuning=0.0,
        probe_detuning=0.0
    )
    
    solver = BlochSolver(system)
    
    detuning_range = np.linspace(-30e6, 30e6, 61) * 2 * np.pi
    density_matrices, coherences = solver.sweep_probe_detuning(detuning_range)
    
    print(f"\nSwept probe detuning from -30 to +30 MHz with 61 points")
    print(f"Number of density matrices computed: {len(density_matrices)}")
    print(f"All matrices valid: {all([solver.validate_density_matrix(rho)['valid'] for rho in density_matrices])}")
    
    print(f"\nCoherence statistics:")
    print(f"  Mean |rho_23|: {np.mean(np.abs(coherences)):.6e}")
    print(f"  Max |rho_23|: {np.max(np.abs(coherences)):.6e}")
    print(f"  Min |rho_23|: {np.min(np.abs(coherences)):.6e}")
    
    if HAS_MATPLOTLIB:
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            
            detuning_MHz = detuning_range / (2 * np.pi) / 1e6
            
            ax1.plot(detuning_MHz, np.abs(coherences), 'b-', linewidth=2)
            ax1.set_xlabel('Probe Detuning (MHz)')
            ax1.set_ylabel('|ρ₂₃|')
            ax1.set_title('Probe-Excited State Coherence vs Detuning')
            ax1.grid(True, alpha=0.3)
            
            populations_1 = np.array([rho[0, 0].real for rho in density_matrices])
            populations_2 = np.array([rho[1, 1].real for rho in density_matrices])
            populations_e = np.array([rho[2, 2].real for rho in density_matrices])
            
            ax2.plot(detuning_MHz, populations_1, 'r-', label='Ground state 1', linewidth=2)
            ax2.plot(detuning_MHz, populations_2, 'g-', label='Ground state 2', linewidth=2)
            ax2.plot(detuning_MHz, populations_e, 'b-', label='Excited state', linewidth=2)
            ax2.set_xlabel('Probe Detuning (MHz)')
            ax2.set_ylabel('Population')
            ax2.set_title('State Populations vs Detuning')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('probe_sweep_example.png', dpi=150)
            print(f"\nPlot saved to: probe_sweep_example.png")
        except Exception as e:
            print(f"\nCould not create plot: {e}")
    else:
        print(f"\nMatplotlib not available, skipping plots")


def example_susceptibility():
    print("\n" + "=" * 60)
    print("Susceptibility Calculation Example")
    print("=" * 60)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6,
        pump_detuning=0.0,
        probe_detuning=0.0
    )
    
    solver = BlochSolver(system)
    
    detuning_range = np.linspace(-30e6, 30e6, 61) * 2 * np.pi
    atom_density = 1e17
    
    absorption, dispersion = solver.compute_susceptibility(detuning_range, atom_density)
    
    print(f"\nComputed susceptibility for atom density: {atom_density:.2e} m⁻³")
    print(f"\nAbsorption statistics:")
    print(f"  Mean: {np.mean(absorption):.6e}")
    print(f"  Max: {np.max(absorption):.6e}")
    print(f"  Min: {np.min(absorption):.6e}")
    
    print(f"\nDispersion statistics:")
    print(f"  Mean: {np.mean(dispersion):.6e}")
    print(f"  Max: {np.max(dispersion):.6e}")
    print(f"  Min: {np.min(dispersion):.6e}")


if __name__ == "__main__":
    example_two_level_system()
    example_three_level_system()
    example_probe_detuning_sweep()
    example_susceptibility()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
