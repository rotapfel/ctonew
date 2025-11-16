import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from typing import Optional, Tuple
from ..double_lambda import DoubleLambdaSystem
from ..constants import HBAR


def plot_energy_level_diagram(
    system: DoubleLambdaSystem,
    output_file: Optional[str] = None,
    show: bool = True,
    figsize: Tuple[float, float] = (10, 8)
):
    fig, ax = plt.subplots(figsize=figsize)
    
    g1_energy = system.ground_state_1.energy
    g2_energy = system.ground_state_2.energy
    e_energy = system.excited_state.energy
    
    energy_offset = min(g1_energy, g2_energy)
    g1_energy_rel = (g1_energy - energy_offset) / HBAR / (2 * np.pi * 1e6)
    g2_energy_rel = (g2_energy - energy_offset) / HBAR / (2 * np.pi * 1e6)
    e_energy_rel = (e_energy - energy_offset) / HBAR / (2 * np.pi * 1e6)
    
    level_width = 0.3
    level_thickness = 3
    
    ax.hlines(g1_energy_rel, -level_width, 0, colors='blue', linewidth=level_thickness)
    ax.hlines(g2_energy_rel, 0, level_width, colors='blue', linewidth=level_thickness)
    ax.hlines(e_energy_rel, -level_width, level_width, colors='red', linewidth=level_thickness)
    
    g1_label = f'|1⟩: {system.ground_state_1.label}\nF={system.ground_state_1.F:.0f}'
    g2_label = f'|2⟩: {system.ground_state_2.label}\nF={system.ground_state_2.F:.0f}'
    e_label = f'|e⟩: {system.excited_state.label}\nF={system.excited_state.F:.0f}'
    
    ax.text(-level_width - 0.05, g1_energy_rel, g1_label, 
            fontsize=11, ha='right', va='center',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax.text(level_width + 0.05, g2_energy_rel, g2_label,
            fontsize=11, ha='left', va='center',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax.text(level_width + 0.05, e_energy_rel, e_label,
            fontsize=11, ha='left', va='center',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    
    pump_arrow_x = -level_width / 2
    pump_arrow = FancyArrowPatch(
        (pump_arrow_x, g1_energy_rel), (pump_arrow_x, e_energy_rel),
        arrowstyle='<->', mutation_scale=20, linewidth=2.5, color='green',
        label='Pump'
    )
    ax.add_patch(pump_arrow)
    
    pump_rabi_mhz = system.pump.rabi_frequency / (2 * np.pi * 1e6)
    pump_det_mhz = system.pump.detuning / (2 * np.pi * 1e6)
    pump_label = f'Pump\nΩ={pump_rabi_mhz:.1f} MHz\nΔ={pump_det_mhz:.1f} MHz'
    ax.text(pump_arrow_x - 0.08, (g1_energy_rel + e_energy_rel) / 2, pump_label,
            fontsize=9, ha='right', va='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    probe_arrow_x = level_width / 2
    probe_arrow = FancyArrowPatch(
        (probe_arrow_x, g2_energy_rel), (probe_arrow_x, e_energy_rel),
        arrowstyle='<->', mutation_scale=20, linewidth=2.5, color='purple',
        label='Probe'
    )
    ax.add_patch(probe_arrow)
    
    probe_rabi_mhz = system.probe.rabi_frequency / (2 * np.pi * 1e6)
    probe_det_mhz = system.probe.detuning / (2 * np.pi * 1e6)
    probe_label = f'Probe\nΩ={probe_rabi_mhz:.1f} MHz\nΔ={probe_det_mhz:.1f} MHz'
    ax.text(probe_arrow_x + 0.08, (g2_energy_rel + e_energy_rel) / 2, probe_label,
            fontsize=9, ha='left', va='center',
            bbox=dict(boxstyle='round', facecolor='plum', alpha=0.7))
    
    gamma = system.atomic_system.total_decay_rate(system.excited_state)
    gamma_mhz = gamma / (2 * np.pi * 1e6)
    
    for decay_x in [-0.18, 0.18]:
        decay_arrow = FancyArrowPatch(
            (decay_x, e_energy_rel - 10), (decay_x, g1_energy_rel + 10 if decay_x < 0 else g2_energy_rel + 10),
            arrowstyle='->', mutation_scale=15, linewidth=1.5, 
            color='orange', linestyle='--', alpha=0.6
        )
        ax.add_patch(decay_arrow)
    
    ax.text(0, e_energy_rel + 50, f'Γ = {gamma_mhz:.1f} MHz',
            fontsize=10, ha='center', va='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
    
    ax.set_ylabel('Energy (MHz)', fontsize=13)
    ax.set_title(f'Double-Lambda EIT Configuration: {system.isotope}', 
                 fontsize=15, fontweight='bold', pad=20)
    
    ax.set_xlim(-0.6, 0.6)
    y_range = e_energy_rel - min(g1_energy_rel, g2_energy_rel)
    ax.set_ylim(min(g1_energy_rel, g2_energy_rel) - y_range * 0.1,
                e_energy_rel + y_range * 0.15)
    
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved energy diagram to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_simple_level_diagram(
    system: DoubleLambdaSystem,
    output_file: Optional[str] = None,
    show: bool = True,
    figsize: Tuple[float, float] = (8, 6)
):
    fig, ax = plt.subplots(figsize=figsize)
    
    g1_y, g2_y, e_y = 0, 0.1, 1.0
    
    ax.hlines(g1_y, 0, 0.4, colors='black', linewidth=3)
    ax.hlines(g2_y, 0.6, 1.0, colors='black', linewidth=3)
    ax.hlines(e_y, 0, 1.0, colors='black', linewidth=3)
    
    ax.text(-0.05, g1_y, f'|1⟩\n{system.ground_state_1.label}', 
            fontsize=11, ha='right', va='center')
    ax.text(1.05, g2_y, f'|2⟩\n{system.ground_state_2.label}',
            fontsize=11, ha='left', va='center')
    ax.text(1.05, e_y, f'|e⟩\n{system.excited_state.label}',
            fontsize=11, ha='left', va='center')
    
    ax.annotate('', xy=(0.2, e_y), xytext=(0.2, g1_y),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2.5))
    ax.text(0.12, (g1_y + e_y) / 2, 'Pump', fontsize=10, ha='right', va='center',
            rotation=90, color='green', fontweight='bold')
    
    ax.annotate('', xy=(0.8, e_y), xytext=(0.8, g2_y),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=2.5))
    ax.text(0.88, (g2_y + e_y) / 2, 'Probe', fontsize=10, ha='left', va='center',
            rotation=90, color='purple', fontweight='bold')
    
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(-0.2, 1.2)
    ax.axis('off')
    
    ax.set_title(f'Double-Lambda Configuration: {system.isotope}',
                 fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved simple diagram to {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig
