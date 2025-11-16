#!/usr/bin/env python3
"""
EIT Spectrum Visualization Example

This script demonstrates end-to-end EIT simulation and visualization for Rb-87.
It generates publication-quality plots showing:
1. EIT absorption spectrum (transparency window)
2. Dispersion spectrum (slow light)
3. Two-photon resonance features
4. Pump power dependence

Run with: python examples/eit_spectrum_visualization.py
"""

import numpy as np
import matplotlib.pyplot as plt
from rb_eit import DoubleLambdaSystem

def plot_basic_eit_spectrum():
    """
    Generate basic EIT absorption and dispersion spectra.
    Shows the characteristic transparency window and steep dispersion.
    """
    print("=" * 70)
    print("Example 1: Basic EIT Spectrum")
    print("=" * 70)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 0.5e6,
        pump_detuning=0.0,
        probe_detuning=0.0
    )
    
    print(f"\n{system}")
    print(f"\nConfiguration:")
    print(f"  Pump Rabi frequency: {system.pump.rabi_frequency/(2*np.pi*1e6):.2f} MHz")
    print(f"  Probe Rabi frequency: {system.probe.rabi_frequency/(2*np.pi*1e6):.2f} MHz")
    
    detuning_mhz = np.linspace(-30, 30, 600)
    detuning_rad = detuning_mhz * 1e6 * 2 * np.pi
    
    susceptibility = system.eit_susceptibility(detuning_rad)
    absorption = np.imag(susceptibility)
    dispersion = np.real(susceptibility)
    
    absorption_norm = absorption / np.max(np.abs(absorption))
    dispersion_norm = dispersion / np.max(np.abs(dispersion))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.plot(detuning_mhz, absorption_norm, linewidth=2, color='#2E86AB')
    ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.axvline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.set_xlabel('Probe Detuning (MHz)', fontsize=12)
    ax1.set_ylabel('Absorption (normalized)', fontsize=12)
    ax1.set_title('EIT Transparency Window', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-30, 30)
    
    ax2.plot(detuning_mhz, dispersion_norm, linewidth=2, color='#A23B72')
    ax2.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax2.axvline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax2.set_xlabel('Probe Detuning (MHz)', fontsize=12)
    ax2.set_ylabel('Dispersion (normalized)', fontsize=12)
    ax2.set_title('Steep Dispersion (Slow Light)', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(-30, 30)
    
    plt.tight_layout()
    plt.savefig('eit_basic_spectrum.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ Plot saved: eit_basic_spectrum.png")
    plt.show()
    
    return system, detuning_mhz, absorption_norm, dispersion_norm


def plot_pump_power_dependence():
    """
    Show how EIT window width depends on pump Rabi frequency.
    Demonstrates the scaling: Transparency width ∝ Ω_pump²/γ
    """
    print("\n" + "=" * 70)
    print("Example 2: Pump Power Dependence")
    print("=" * 70)
    
    pump_powers = [5, 10, 20, 40]
    detuning_mhz = np.linspace(-40, 40, 800)
    detuning_rad = detuning_mhz * 1e6 * 2 * np.pi
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(pump_powers)))
    
    print(f"\nScanning pump Rabi frequency:")
    
    for i, pump_mhz in enumerate(pump_powers):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * pump_mhz * 1e6,
            probe_rabi_frequency=2 * np.pi * 0.5e6
        )
        
        print(f"  Ω_pump = {pump_mhz} MHz")
        
        susceptibility = system.eit_susceptibility(detuning_rad)
        absorption = np.imag(susceptibility)
        
        absorption_norm = absorption / np.max(np.abs(absorption))
        
        ax1.plot(detuning_mhz, absorption_norm, 
                linewidth=2, color=colors[i], 
                label=f'{pump_mhz} MHz')
        
        zoom_idx = np.abs(detuning_mhz) < 20
        ax2.plot(detuning_mhz[zoom_idx], absorption_norm[zoom_idx],
                linewidth=2, color=colors[i],
                label=f'{pump_mhz} MHz')
    
    ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.axvline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.set_xlabel('Probe Detuning (MHz)', fontsize=12)
    ax1.set_ylabel('Absorption (normalized)', fontsize=12)
    ax1.set_title('Full Spectrum', fontsize=13, fontweight='bold')
    ax1.legend(title='Pump Ω', fontsize=10, loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-40, 40)
    
    ax2.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax2.axvline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax2.set_xlabel('Probe Detuning (MHz)', fontsize=12)
    ax2.set_ylabel('Absorption (normalized)', fontsize=12)
    ax2.set_title('EIT Window Detail', fontsize=13, fontweight='bold')
    ax2.legend(title='Pump Ω', fontsize=10, loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(-20, 20)
    
    plt.suptitle('Pump Power Dependence of EIT Window', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('eit_pump_dependence.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ Plot saved: eit_pump_dependence.png")
    plt.show()


def plot_two_photon_detuning():
    """
    Show the effect of two-photon detuning on EIT resonance.
    Maximum transparency occurs at δ = Δ_pump - Δ_probe = 0
    """
    print("\n" + "=" * 70)
    print("Example 3: Two-Photon Detuning Effect")
    print("=" * 70)
    
    two_photon_detunings = [-5, -2.5, 0, 2.5, 5]
    detuning_mhz = np.linspace(-30, 30, 600)
    detuning_rad = detuning_mhz * 1e6 * 2 * np.pi
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    colors = plt.cm.coolwarm(np.linspace(0, 1, len(two_photon_detunings)))
    
    print(f"\nScanning two-photon detuning δ = Δ_pump - Δ_probe:")
    
    for i, delta_2p in enumerate(two_photon_detunings):
        pump_det = delta_2p * 1e6 * 2 * np.pi
        
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 0.5e6,
            pump_detuning=pump_det,
            probe_detuning=0.0
        )
        
        print(f"  δ = {delta_2p:+.1f} MHz")
        
        susceptibility = system.eit_susceptibility(detuning_rad)
        absorption = np.imag(susceptibility)
        absorption_norm = absorption / np.max(np.abs(absorption))
        
        linestyle = '-' if delta_2p == 0 else '--'
        linewidth = 3 if delta_2p == 0 else 2
        
        ax.plot(detuning_mhz, absorption_norm,
               linewidth=linewidth, linestyle=linestyle,
               color=colors[i], label=f'δ = {delta_2p:+.1f} MHz')
    
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.axvline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.set_xlabel('Probe Detuning (MHz)', fontsize=12)
    ax.set_ylabel('Absorption (normalized)', fontsize=12)
    ax.set_title('Two-Photon Detuning Effect on EIT', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-30, 30)
    
    plt.tight_layout()
    plt.savefig('eit_two_photon_detuning.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ Plot saved: eit_two_photon_detuning.png")
    plt.show()


def plot_rb87_vs_rb85():
    """
    Compare EIT spectra for Rb-87 and Rb-85 isotopes.
    Different nuclear spins lead to different hyperfine structure.
    """
    print("\n" + "=" * 70)
    print("Example 4: Rb-87 vs Rb-85 Comparison")
    print("=" * 70)
    
    detuning_mhz = np.linspace(-30, 30, 600)
    detuning_rad = detuning_mhz * 1e6 * 2 * np.pi
    
    system_rb87 = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 0.5e6
    )
    
    system_rb85 = DoubleLambdaSystem(
        isotope="Rb85",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 0.5e6
    )
    
    print(f"\nRb-87 System:")
    print(f"  {system_rb87.ground_state_1.label} ↔ {system_rb87.excited_state.label}")
    print(f"  {system_rb87.ground_state_2.label} ↔ {system_rb87.excited_state.label}")
    
    print(f"\nRb-85 System:")
    print(f"  {system_rb85.ground_state_1.label} ↔ {system_rb85.excited_state.label}")
    print(f"  {system_rb85.ground_state_2.label} ↔ {system_rb85.excited_state.label}")
    
    susc_rb87 = system_rb87.eit_susceptibility(detuning_rad)
    susc_rb85 = system_rb85.eit_susceptibility(detuning_rad)
    
    abs_rb87 = np.imag(susc_rb87) / np.max(np.abs(np.imag(susc_rb87)))
    abs_rb85 = np.imag(susc_rb85) / np.max(np.abs(np.imag(susc_rb85)))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    
    ax1.plot(detuning_mhz, abs_rb87, linewidth=2, color='#E63946', label='⁸⁷Rb (I=3/2)')
    ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.axvline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.set_ylabel('Absorption (normalized)', fontsize=12)
    ax1.set_title('⁸⁷Rb: F=1,2 → F\'=2', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(detuning_mhz, abs_rb85, linewidth=2, color='#457B9D', label='⁸⁵Rb (I=5/2)')
    ax2.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax2.axvline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax2.set_xlabel('Probe Detuning (MHz)', fontsize=12)
    ax2.set_ylabel('Absorption (normalized)', fontsize=12)
    ax2.set_title('⁸⁵Rb: F=2,3 → F\'=3', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Isotope Comparison: EIT in Rb-87 vs Rb-85',
                fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('eit_rb87_vs_rb85.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ Plot saved: eit_rb87_vs_rb85.png")
    plt.show()


def plot_level_diagram():
    """
    Create a simplified energy level diagram for Rb-87 double-lambda EIT.
    """
    print("\n" + "=" * 70)
    print("Example 5: Energy Level Diagram")
    print("=" * 70)
    
    system = DoubleLambdaSystem(isotope="Rb87")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ground1_e = 0
    ground2_e = 6834.682611
    excited_e = 384230406.373e6 + 200e6
    
    ground1_pos = 0.3
    ground2_pos = 0.7
    excited_pos = 0.5
    
    level_width = 0.25
    
    ax.plot([ground1_pos - level_width/2, ground1_pos + level_width/2], 
           [ground1_e, ground1_e], 'k-', linewidth=2)
    ax.plot([ground2_pos - level_width/2, ground2_pos + level_width/2], 
           [ground2_e, ground2_e], 'k-', linewidth=2)
    ax.plot([excited_pos - level_width/2, excited_pos + level_width/2], 
           [excited_e, excited_e], 'k-', linewidth=2)
    
    ax.annotate('', xy=(excited_pos-0.05, excited_e), 
               xytext=(ground1_pos+0.05, ground1_e+500),
               arrowprops=dict(arrowstyle='->', lw=2, color='#E63946'))
    ax.text(ground1_pos+0.12, excited_e/2 - 50e6, 'Pump\nΩ$_p$', 
           fontsize=11, color='#E63946', ha='center', fontweight='bold')
    
    ax.annotate('', xy=(excited_pos+0.05, excited_e), 
               xytext=(ground2_pos-0.05, ground2_e+500),
               arrowprops=dict(arrowstyle='->', lw=2, color='#457B9D'))
    ax.text(ground2_pos-0.12, excited_e/2 - 50e6, 'Probe\nΩ$_c$', 
           fontsize=11, color='#457B9D', ha='center', fontweight='bold')
    
    ax.text(ground1_pos, ground1_e - 30e6, f'|1⟩ = {system.ground_state_1.label}',
           fontsize=11, ha='center', va='top', fontweight='bold')
    ax.text(ground2_pos, ground2_e + 30e6, f'|2⟩ = {system.ground_state_2.label}',
           fontsize=11, ha='center', va='bottom', fontweight='bold')
    ax.text(excited_pos, excited_e + 30e6, f'|e⟩ = {system.excited_state.label}',
           fontsize=11, ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-50e6, excited_e + 80e6)
    ax.axis('off')
    ax.set_title('⁸⁷Rb Double-Lambda EIT Configuration', 
                fontsize=14, fontweight='bold', pad=20)
    
    ax.text(0.5, -40e6, 'Ground State Hyperfine Splitting: 6.835 GHz',
           ha='center', fontsize=10, style='italic')
    
    plt.tight_layout()
    plt.savefig('eit_level_diagram.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ Plot saved: eit_level_diagram.png")
    plt.show()


def print_summary():
    """
    Print summary information about the simulation.
    """
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    decay_rate = system.atomic_system.total_decay_rate(system.excited_state)
    
    print(f"\nPhysical Parameters:")
    print(f"  Natural linewidth γ: {decay_rate/(2*np.pi*1e6):.3f} MHz")
    print(f"  D2 wavelength: {system.transition_1.wavelength*1e9:.4f} nm")
    print(f"  Transition frequency: {system.transition_1.frequency/1e12:.6f} THz")
    
    print(f"\nEIT Window Width:")
    omega_pump = system.pump.rabi_frequency
    width_estimate = omega_pump**2 / decay_rate
    print(f"  Estimated: Ω²/γ ≈ {width_estimate/(2*np.pi*1e6):.2f} MHz")
    
    print(f"\nGenerated Plots:")
    print(f"  1. eit_basic_spectrum.png - Basic absorption and dispersion")
    print(f"  2. eit_pump_dependence.png - Pump power scan")
    print(f"  3. eit_two_photon_detuning.png - Two-photon resonance")
    print(f"  4. eit_rb87_vs_rb85.png - Isotope comparison")
    print(f"  5. eit_level_diagram.png - Energy level diagram")
    
    print(f"\n{'=' * 70}")
    print("All visualizations completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EIT SPECTRUM VISUALIZATION")
    print("Rb Double-Lambda Electromagnetically Induced Transparency")
    print("=" * 70)
    
    try:
        import matplotlib
        matplotlib.use('Agg')
    except ImportError:
        print("\nWarning: matplotlib not available. Install with:")
        print("  pip install matplotlib")
        exit(1)
    
    plot_basic_eit_spectrum()
    plot_pump_power_dependence()
    plot_two_photon_detuning()
    plot_rb87_vs_rb85()
    plot_level_diagram()
    print_summary()
