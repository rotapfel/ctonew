from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class LaserField:
    rabi_frequency: float
    detuning: float = 0.0
    frequency: Optional[float] = None
    wavelength: Optional[float] = None
    intensity: Optional[float] = None
    phase: float = 0.0
    polarization: str = "linear"
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        if self.rabi_frequency < 0:
            raise ValueError(f"Rabi frequency must be non-negative, got {self.rabi_frequency}")
        
        if self.polarization not in ["linear", "sigma_plus", "sigma_minus", "circular"]:
            raise ValueError(f"Polarization must be 'linear', 'sigma_plus', 'sigma_minus', or 'circular', "
                           f"got '{self.polarization}'")
        
        if self.intensity is not None and self.intensity < 0:
            raise ValueError(f"Intensity must be non-negative, got {self.intensity}")
        
        if not (0 <= self.phase < 2 * np.pi):
            self.phase = self.phase % (2 * np.pi)
    
    def electric_field_amplitude(self, dipole_moment):
        from .constants import HBAR
        return self.rabi_frequency * HBAR / dipole_moment
    
    def on_resonance_rabi_frequency(self):
        return self.rabi_frequency
    
    def effective_rabi_frequency(self):
        return np.sqrt(self.rabi_frequency**2 + self.detuning**2)
    
    def set_intensity(self, intensity, dipole_moment, transition_frequency):
        from .constants import EPSILON_0, C, HBAR
        electric_field = np.sqrt(2 * intensity / (EPSILON_0 * C))
        self.rabi_frequency = dipole_moment * electric_field / HBAR
        self.intensity = intensity
    
    def get_intensity(self, dipole_moment):
        from .constants import EPSILON_0, C, HBAR
        electric_field = self.rabi_frequency * HBAR / dipole_moment
        return 0.5 * EPSILON_0 * C * electric_field**2
    
    def __str__(self):
        return f"LaserField(Ω={self.rabi_frequency:.3e}, Δ={self.detuning:.3e})"
    
    def __repr__(self):
        return (f"LaserField(rabi_frequency={self.rabi_frequency:.3e}, "
                f"detuning={self.detuning:.3e}, polarization='{self.polarization}')")
