from dataclasses import dataclass
from typing import Optional
import numpy as np
from .atomic_level import AtomicLevel


@dataclass
class Transition:
    lower: AtomicLevel
    upper: AtomicLevel
    dipole_moment: float
    frequency: Optional[float] = None
    wavelength: Optional[float] = None
    
    def __post_init__(self):
        self._validate()
        if self.frequency is None and self.wavelength is None:
            self.frequency = self._calculate_frequency()
        elif self.frequency is None:
            from .constants import C
            self.frequency = C / self.wavelength
        elif self.wavelength is None:
            from .constants import C
            self.wavelength = C / self.frequency
    
    def _validate(self):
        if self.lower.energy >= self.upper.energy:
            raise ValueError(f"Lower level energy must be less than upper level energy. "
                           f"Got lower={self.lower.energy:.3e}, upper={self.upper.energy:.3e}")
        
        dL = abs(self.upper.L - self.lower.L)
        if dL != 1:
            raise ValueError(f"Selection rule violation: ΔL must be ±1, got ΔL={dL}")
        
        dJ = abs(self.upper.J - self.lower.J)
        if dJ > 1:
            raise ValueError(f"Selection rule violation: ΔJ must be 0 or ±1, got ΔJ={dJ}")
        
        if self.upper.J == 0 and self.lower.J == 0:
            raise ValueError("Selection rule violation: J=0 → J=0 transition is forbidden")
        
        dF = abs(self.upper.F - self.lower.F)
        if dF > 1:
            raise ValueError(f"Selection rule violation: ΔF must be 0 or ±1, got ΔF={dF}")
        
        if self.upper.F == 0 and self.lower.F == 0:
            raise ValueError("Selection rule violation: F=0 → F=0 transition is forbidden")
        
        dmF = abs(self.upper.mF - self.lower.mF)
        if dmF > 1:
            raise ValueError(f"Selection rule violation: ΔmF must be 0 or ±1, got ΔmF={dmF}")
        
        if self.dipole_moment < 0:
            raise ValueError(f"Dipole moment must be non-negative, got {self.dipole_moment}")
    
    def _calculate_frequency(self):
        from .constants import HBAR
        return (self.upper.energy - self.lower.energy) / HBAR
    
    def rabi_frequency(self, electric_field_amplitude):
        from .constants import HBAR
        return self.dipole_moment * electric_field_amplitude / HBAR
    
    def __str__(self):
        return f"{self.lower.label} → {self.upper.label}"
    
    def __repr__(self):
        return f"Transition({self.lower.label} → {self.upper.label}, ν={self.frequency:.3e} Hz)"
    
    def __hash__(self):
        return hash((self.lower, self.upper))
    
    def __eq__(self, other):
        if not isinstance(other, Transition):
            return False
        return self.lower == other.lower and self.upper == other.upper
