import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional, Tuple
from ..double_lambda import DoubleLambdaSystem


def create_interactive_eit_spectrum(
    system: DoubleLambdaSystem,
    pump_rabi_range: Tuple[float, float] = (1e6, 50e6),
    probe_rabi_range: Tuple[float, float] = (0.1e6, 10e6),
    detuning_range: Tuple[float, float] = (-30e6, 30e6),
    num_points: int = 500,
    output_file: Optional[str] = None
):
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Absorption Spectrum', 'Dispersion Spectrum'),
        vertical_spacing=0.12
    )
    
    pump_rabi_values = np.linspace(pump_rabi_range[0], pump_rabi_range[1], 20) * 2 * np.pi
    probe_rabi_values = np.linspace(probe_rabi_range[0], probe_rabi_range[1], 15) * 2 * np.pi
    
    detuning_scan = np.linspace(detuning_range[0], detuning_range[1], num_points) * 2 * np.pi
    detuning_mhz = detuning_scan / (2 * np.pi * 1e6)
    
    default_pump_idx = len(pump_rabi_values) // 2
    default_probe_idx = len(probe_rabi_values) // 2
    
    for i, pump_rabi in enumerate(pump_rabi_values):
        for j, probe_rabi in enumerate(probe_rabi_values):
            system.set_pump_parameters(pump_rabi, 0.0)
            system.set_probe_parameters(probe_rabi, 0.0)
            
            susceptibility = system.eit_susceptibility(detuning_scan)
            absorption = -np.imag(susceptibility)
            dispersion = np.real(susceptibility)
            
            visible = (i == default_pump_idx and j == default_probe_idx)
            
            fig.add_trace(
                go.Scatter(
                    x=detuning_mhz,
                    y=absorption,
                    mode='lines',
                    name=f'Absorption',
                    visible=visible,
                    line=dict(color='blue', width=2)
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=detuning_mhz,
                    y=dispersion,
                    mode='lines',
                    name=f'Dispersion',
                    visible=visible,
                    line=dict(color='red', width=2)
                ),
                row=2, col=1
            )
    
    steps_pump = []
    for i, pump_rabi in enumerate(pump_rabi_values):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}],
            label=f"{pump_rabi / (2 * np.pi * 1e6):.1f}"
        )
        for j in range(len(probe_rabi_values)):
            idx = (i * len(probe_rabi_values) + j) * 2
            step["args"][0]["visible"][idx] = True
            step["args"][0]["visible"][idx + 1] = True
        steps_pump.append(step)
    
    steps_probe = []
    for j, probe_rabi in enumerate(probe_rabi_values):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}],
            label=f"{probe_rabi / (2 * np.pi * 1e6):.2f}"
        )
        for i in range(len(pump_rabi_values)):
            idx = (i * len(probe_rabi_values) + j) * 2
            step["args"][0]["visible"][idx] = True
            step["args"][0]["visible"][idx + 1] = True
        steps_probe.append(step)
    
    sliders = [
        dict(
            active=default_pump_idx,
            yanchor="top",
            y=1.15,
            xanchor="left",
            currentvalue=dict(prefix="Pump Rabi Frequency (MHz): ", visible=True, xanchor="right"),
            pad=dict(b=10, t=50),
            len=0.45,
            x=0.0,
            steps=steps_pump
        ),
        dict(
            active=default_probe_idx,
            yanchor="top",
            y=1.15,
            xanchor="right",
            currentvalue=dict(prefix="Probe Rabi Frequency (MHz): ", visible=True, xanchor="left"),
            pad=dict(b=10, t=50),
            len=0.45,
            x=0.55,
            steps=steps_probe
        )
    ]
    
    fig.update_xaxes(title_text="Probe Detuning (MHz)", row=2, col=1)
    fig.update_yaxes(title_text="Absorption (arb. units)", row=1, col=1)
    fig.update_yaxes(title_text="Dispersion (arb. units)", row=2, col=1)
    
    fig.update_layout(
        title=dict(
            text=f"Interactive EIT Spectrum: {system.isotope}",
            x=0.5,
            xanchor='center',
            font=dict(size=18)
        ),
        sliders=sliders,
        height=800,
        showlegend=False,
        hovermode='x unified'
    )
    
    if output_file:
        fig.write_html(output_file)
        print(f"Saved interactive plot to {output_file}")
    
    return fig


def create_interactive_heatmap(
    system: DoubleLambdaSystem,
    probe_detuning_range: Tuple[float, float] = (-30e6, 30e6),
    pump_rabi_range: Tuple[float, float] = (1e6, 50e6),
    num_points: Tuple[int, int] = (150, 100),
    output_file: Optional[str] = None
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
    
    fig = go.Figure(data=go.Heatmap(
        z=Z,
        x=X[0, :],
        y=Y[:, 0],
        colorscale='Hot',
        colorbar=dict(title="Absorption<br>(arb. units)")
    ))
    
    fig.update_layout(
        title=dict(
            text=f"Interactive EIT Parameter Space: {system.isotope}",
            x=0.5,
            xanchor='center',
            font=dict(size=18)
        ),
        xaxis_title="Probe Detuning (MHz)",
        yaxis_title="Pump Rabi Frequency (MHz)",
        height=700,
        hovermode='closest'
    )
    
    if output_file:
        fig.write_html(output_file)
        print(f"Saved interactive heatmap to {output_file}")
    
    return fig


def create_interactive_3d_surface(
    system: DoubleLambdaSystem,
    probe_detuning_range: Tuple[float, float] = (-30e6, 30e6),
    pump_rabi_range: Tuple[float, float] = (1e6, 50e6),
    num_points: Tuple[int, int] = (100, 80),
    output_file: Optional[str] = None
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
    
    fig = go.Figure(data=[go.Surface(
        z=Z,
        x=X[0, :],
        y=Y[:, 0],
        colorscale='Viridis',
        colorbar=dict(title="Absorption<br>(arb. units)")
    )])
    
    fig.update_layout(
        title=dict(
            text=f"Interactive 3D EIT Surface: {system.isotope}",
            x=0.5,
            xanchor='center',
            font=dict(size=18)
        ),
        scene=dict(
            xaxis_title="Probe Detuning (MHz)",
            yaxis_title="Pump Rabi Frequency (MHz)",
            zaxis_title="Absorption (arb. units)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        height=800
    )
    
    if output_file:
        fig.write_html(output_file)
        print(f"Saved interactive 3D surface to {output_file}")
    
    return fig


def create_parameter_sweep_comparison(
    systems: list,
    labels: list,
    detuning_range: Tuple[float, float] = (-30e6, 30e6),
    num_points: int = 500,
    output_file: Optional[str] = None
):
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Absorption Comparison', 'Dispersion Comparison'),
        vertical_spacing=0.12
    )
    
    detuning_scan = np.linspace(detuning_range[0], detuning_range[1], num_points) * 2 * np.pi
    detuning_mhz = detuning_scan / (2 * np.pi * 1e6)
    
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray']
    
    for i, (system, label) in enumerate(zip(systems, labels)):
        susceptibility = system.eit_susceptibility(detuning_scan)
        absorption = -np.imag(susceptibility)
        dispersion = np.real(susceptibility)
        
        color = colors[i % len(colors)]
        
        fig.add_trace(
            go.Scatter(
                x=detuning_mhz,
                y=absorption,
                mode='lines',
                name=label,
                line=dict(color=color, width=2),
                legendgroup=label
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=detuning_mhz,
                y=dispersion,
                mode='lines',
                name=label,
                line=dict(color=color, width=2),
                legendgroup=label,
                showlegend=False
            ),
            row=2, col=1
        )
    
    fig.update_xaxes(title_text="Probe Detuning (MHz)", row=2, col=1)
    fig.update_yaxes(title_text="Absorption (arb. units)", row=1, col=1)
    fig.update_yaxes(title_text="Dispersion (arb. units)", row=2, col=1)
    
    fig.update_layout(
        title=dict(
            text="Interactive EIT Comparison",
            x=0.5,
            xanchor='center',
            font=dict(size=18)
        ),
        height=800,
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )
    
    if output_file:
        fig.write_html(output_file)
        print(f"Saved interactive comparison to {output_file}")
    
    return fig
