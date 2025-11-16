import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List, Tuple
from ..double_lambda import DoubleLambdaSystem


def plot_eit_spectrum(
    system: DoubleLambdaSystem,
    detuning_range: Tuple[float, float] = (-30e6, 30e6),
    num_points: int = 500,
    output_file: Optional[str] = None,
    show: bool = True,
    figsize: Tuple[float, float] = (10, 6)
):
    detuning_scan = np.linspace(detuning_range[0], detuning_range[1], num_points) * 2 * np.pi
    susceptibility = system.eit_susceptibility(detuning_scan)
    
    absorption = -np.imag(susceptibility)
    dispersion = np.real(susceptibility)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    
    detuning_mhz = detuning_scan / (2 * np.pi * 1e6)
    
    ax1.plot(detuning_mhz, absorption, 'b-', linewidth=2)
    ax1.set_ylabel('Absorption (arb. units)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_title(f'EIT Spectrum: {system.isotope}', fontsize=14, fontweight='bold')
    
    ax2.plot(detuning_mhz, dispersion, 'r-', linewidth=2)
    ax2.set_xlabel('Probe Detuning (MHz)', fontsize=12)
    ax2.set_ylabel('Dispersion (arb. units)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    pump_rabi_mhz = system.pump.rabi_frequency / (2 * np.pi * 1e6)
    probe_rabi_mhz = system.probe.rabi_frequency / (2 * np.pi * 1e6)
    pump_det_mhz = system.pump.detuning / (2 * np.pi * 1e6)
    
    fig.text(0.15, 0.96, f'Pump: Ω={pump_rabi_mhz:.2f} MHz, Δ={pump_det_mhz:.2f} MHz',
             fontsize=10, verticalalignment='top')
    fig.text(0.15, 0.93, f'Probe: Ω={probe_rabi_mhz:.2f} MHz',
             fontsize=10, verticalalignment='top')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_comparison(
    systems: List[DoubleLambdaSystem],
    labels: List[str],
    detuning_range: Tuple[float, float] = (-30e6, 30e6),
    num_points: int = 500,
    output_file: Optional[str] = None,
    show: bool = True,
    figsize: Tuple[float, float] = (10, 6)
):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(systems)))
    
    for i, (system, label) in enumerate(zip(systems, labels)):
        detuning_scan = np.linspace(detuning_range[0], detuning_range[1], num_points) * 2 * np.pi
        susceptibility = system.eit_susceptibility(detuning_scan)
        
        absorption = -np.imag(susceptibility)
        dispersion = np.real(susceptibility)
        detuning_mhz = detuning_scan / (2 * np.pi * 1e6)
        
        ax1.plot(detuning_mhz, absorption, linewidth=2, color=colors[i], label=label)
        ax2.plot(detuning_mhz, dispersion, linewidth=2, color=colors[i], label=label)
    
    ax1.set_ylabel('Absorption (arb. units)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    ax1.set_title('EIT Spectrum Comparison', fontsize=14, fontweight='bold')
    
    ax2.set_xlabel('Probe Detuning (MHz)', fontsize=12)
    ax2.set_ylabel('Dispersion (arb. units)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved comparison plot to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_transmission_spectrum(
    system: DoubleLambdaSystem,
    detuning_range: Tuple[float, float] = (-30e6, 30e6),
    num_points: int = 500,
    output_file: Optional[str] = None,
    show: bool = True,
    figsize: Tuple[float, float] = (10, 6)
):
    detuning_scan = np.linspace(detuning_range[0], detuning_range[1], num_points) * 2 * np.pi
    susceptibility = system.eit_susceptibility(detuning_scan)
    
    absorption = -np.imag(susceptibility)
    absorption_normalized = (absorption - absorption.min()) / (absorption.max() - absorption.min())
    transmission = np.exp(-absorption_normalized * 3)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    detuning_mhz = detuning_scan / (2 * np.pi * 1e6)
    
    ax.plot(detuning_mhz, transmission, 'g-', linewidth=2.5)
    ax.set_xlabel('Probe Detuning (MHz)', fontsize=12)
    ax.set_ylabel('Transmission (normalized)', fontsize=12)
    ax.set_title(f'EIT Transmission Window: {system.isotope}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 1.1])
    
    pump_rabi_mhz = system.pump.rabi_frequency / (2 * np.pi * 1e6)
    probe_rabi_mhz = system.probe.rabi_frequency / (2 * np.pi * 1e6)
    pump_det_mhz = system.pump.detuning / (2 * np.pi * 1e6)
    
    textstr = f'Pump: Ω={pump_rabi_mhz:.2f} MHz, Δ={pump_det_mhz:.2f} MHz\nProbe: Ω={probe_rabi_mhz:.2f} MHz'
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved transmission spectrum to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_linewidth_vs_pump_power(
    system: DoubleLambdaSystem,
    pump_rabi_range: Tuple[float, float] = (1e6, 50e6),
    num_points: int = 50,
    output_file: Optional[str] = None,
    show: bool = True,
    figsize: Tuple[float, float] = (8, 6)
):
    pump_rabi_values = np.linspace(pump_rabi_range[0], pump_rabi_range[1], num_points) * 2 * np.pi
    linewidths = []
    
    original_pump_rabi = system.pump.rabi_frequency
    original_pump_det = system.pump.detuning
    
    for pump_rabi in pump_rabi_values:
        system.set_pump_parameters(pump_rabi, 0.0)
        
        detuning_scan = np.linspace(-20e6, 20e6, 300) * 2 * np.pi
        susceptibility = system.eit_susceptibility(detuning_scan)
        absorption = -np.imag(susceptibility)
        
        max_abs = absorption.max()
        half_max = max_abs / 2
        above_half = absorption > half_max
        indices = np.where(above_half)[0]
        
        if len(indices) > 1:
            fwhm = (detuning_scan[indices[-1]] - detuning_scan[indices[0]]) / (2 * np.pi * 1e6)
            linewidths.append(fwhm)
        else:
            linewidths.append(np.nan)
    
    system.set_pump_parameters(original_pump_rabi, original_pump_det)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    pump_rabi_mhz = pump_rabi_values / (2 * np.pi * 1e6)
    
    ax.plot(pump_rabi_mhz, linewidths, 'bo-', linewidth=2, markersize=4)
    ax.set_xlabel('Pump Rabi Frequency (MHz)', fontsize=12)
    ax.set_ylabel('EIT Linewidth (MHz, FWHM)', fontsize=12)
    ax.set_title('EIT Transparency Window vs Pump Power', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved linewidth plot to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig
