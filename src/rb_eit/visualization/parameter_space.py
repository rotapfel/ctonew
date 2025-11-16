import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from typing import Optional, Tuple, Callable
from ..double_lambda import DoubleLambdaSystem


def plot_2d_heatmap(
    system: DoubleLambdaSystem,
    param1_name: str,
    param1_range: Tuple[float, float],
    param2_name: str,
    param2_range: Tuple[float, float],
    metric_func: Callable,
    num_points: Tuple[int, int] = (50, 50),
    output_file: Optional[str] = None,
    show: bool = True,
    figsize: Tuple[float, float] = (10, 8),
    cmap: str = 'viridis'
):
    param1_values = np.linspace(param1_range[0], param1_range[1], num_points[0])
    param2_values = np.linspace(param2_range[0], param2_range[1], num_points[1])
    
    X, Y = np.meshgrid(param1_values, param2_values)
    Z = np.zeros_like(X)
    
    for i in range(num_points[1]):
        for j in range(num_points[0]):
            Z[i, j] = metric_func(system, param1_values[j], param2_values[i])
    
    fig, ax = plt.subplots(figsize=figsize)
    
    im = ax.pcolormesh(X, Y, Z, cmap=cmap, shading='auto')
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Metric Value', fontsize=12)
    
    ax.set_xlabel(param1_name, fontsize=12)
    ax.set_ylabel(param2_name, fontsize=12)
    ax.set_title('Parameter Space Heatmap', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved heatmap to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_detuning_rabi_heatmap(
    system: DoubleLambdaSystem,
    probe_detuning_range: Tuple[float, float] = (-30e6, 30e6),
    pump_rabi_range: Tuple[float, float] = (1e6, 50e6),
    num_points: Tuple[int, int] = (100, 50),
    output_file: Optional[str] = None,
    show: bool = True,
    figsize: Tuple[float, float] = (12, 8)
):
    probe_detunings = np.linspace(probe_detuning_range[0], probe_detuning_range[1], num_points[0]) * 2 * np.pi
    pump_rabi_freqs = np.linspace(pump_rabi_range[0], pump_rabi_range[1], num_points[1]) * 2 * np.pi
    
    X, Y = np.meshgrid(probe_detunings / (2 * np.pi * 1e6), pump_rabi_freqs / (2 * np.pi * 1e6))
    Z = np.zeros_like(X)
    
    original_pump_rabi = system.pump.rabi_frequency
    original_pump_det = system.pump.detuning
    
    for i, pump_rabi in enumerate(pump_rabi_freqs):
        system.set_pump_parameters(pump_rabi, 0.0)
        susceptibility = system.eit_susceptibility(probe_detunings)
        Z[i, :] = -np.imag(susceptibility)
    
    system.set_pump_parameters(original_pump_rabi, original_pump_det)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    im = ax.pcolormesh(X, Y, Z, cmap='hot', shading='auto')
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Absorption (arb. units)', fontsize=12)
    
    ax.set_xlabel('Probe Detuning (MHz)', fontsize=12)
    ax.set_ylabel('Pump Rabi Frequency (MHz)', fontsize=12)
    ax.set_title(f'EIT Parameter Space: {system.isotope}', fontsize=14, fontweight='bold')
    
    contours = ax.contour(X, Y, Z, levels=10, colors='cyan', alpha=0.4, linewidths=0.5)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved detuning-Rabi heatmap to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_3d_surface(
    system: DoubleLambdaSystem,
    probe_detuning_range: Tuple[float, float] = (-30e6, 30e6),
    pump_rabi_range: Tuple[float, float] = (1e6, 50e6),
    num_points: Tuple[int, int] = (80, 40),
    output_file: Optional[str] = None,
    show: bool = True,
    figsize: Tuple[float, float] = (14, 10)
):
    probe_detunings = np.linspace(probe_detuning_range[0], probe_detuning_range[1], num_points[0]) * 2 * np.pi
    pump_rabi_freqs = np.linspace(pump_rabi_range[0], pump_rabi_range[1], num_points[1]) * 2 * np.pi
    
    X, Y = np.meshgrid(probe_detunings / (2 * np.pi * 1e6), pump_rabi_freqs / (2 * np.pi * 1e6))
    Z = np.zeros_like(X)
    
    original_pump_rabi = system.pump.rabi_frequency
    original_pump_det = system.pump.detuning
    
    for i, pump_rabi in enumerate(pump_rabi_freqs):
        system.set_pump_parameters(pump_rabi, 0.0)
        susceptibility = system.eit_susceptibility(probe_detunings)
        Z[i, :] = -np.imag(susceptibility)
    
    system.set_pump_parameters(original_pump_rabi, original_pump_det)
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0, antialiased=True, alpha=0.9)
    
    ax.set_xlabel('Probe Detuning (MHz)', fontsize=11, labelpad=10)
    ax.set_ylabel('Pump Rabi Frequency (MHz)', fontsize=11, labelpad=10)
    ax.set_zlabel('Absorption (arb. units)', fontsize=11, labelpad=10)
    ax.set_title(f'EIT 3D Surface: {system.isotope}', fontsize=14, fontweight='bold', pad=20)
    
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Absorption')
    
    ax.view_init(elev=25, azim=45)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved 3D surface plot to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_two_photon_resonance(
    system: DoubleLambdaSystem,
    pump_detuning_range: Tuple[float, float] = (-30e6, 30e6),
    probe_detuning_range: Tuple[float, float] = (-30e6, 30e6),
    num_points: Tuple[int, int] = (100, 100),
    output_file: Optional[str] = None,
    show: bool = True,
    figsize: Tuple[float, float] = (10, 9)
):
    pump_detunings = np.linspace(pump_detuning_range[0], pump_detuning_range[1], num_points[0]) * 2 * np.pi
    probe_detunings = np.linspace(probe_detuning_range[0], probe_detuning_range[1], num_points[1]) * 2 * np.pi
    
    X, Y = np.meshgrid(pump_detunings / (2 * np.pi * 1e6), probe_detunings / (2 * np.pi * 1e6))
    Z = np.zeros_like(X)
    
    original_pump_det = system.pump.detuning
    
    for i, pump_det in enumerate(pump_detunings):
        system.pump.detuning = pump_det
        susceptibility = system.eit_susceptibility(probe_detunings)
        Z[i, :] = -np.imag(susceptibility)
    
    system.pump.detuning = original_pump_det
    
    fig, ax = plt.subplots(figsize=figsize)
    
    im = ax.pcolormesh(X, Y, Z, cmap='RdYlBu_r', shading='auto')
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Absorption (arb. units)', fontsize=12)
    
    ax.plot(X[0, :], X[0, :], 'w--', linewidth=2, label='Two-photon resonance')
    
    ax.set_xlabel('Pump Detuning (MHz)', fontsize=12)
    ax.set_ylabel('Probe Detuning (MHz)', fontsize=12)
    ax.set_title(f'Two-Photon Resonance Map: {system.isotope}', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved two-photon resonance map to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig
