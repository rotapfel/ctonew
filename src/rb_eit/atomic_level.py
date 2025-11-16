from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class AtomicLevel:
    n: int
    L: int
    J: float
    F: float
    mF: float = 0.0
    energy: float = 0.0
    label: Optional[str] = None
    nuclear_spin: Optional[float] = None
    
    def __post_init__(self):
        self._validate()
        if self.label is None:
            self.label = self._generate_label()
    
    def _validate(self):
        if self.n < 1:
            raise ValueError(f"Principal quantum number n must be >= 1, got {self.n}")
        
        if self.L < 0 or self.L >= self.n:
            raise ValueError(f"Angular momentum L must be 0 <= L < n, got L={self.L}, n={self.n}")
        
        if not (abs(self.L - 0.5) <= self.J <= self.L + 0.5):
            raise ValueError(f"Total angular momentum J must satisfy |L-S| <= J <= L+S, got J={self.J}, L={self.L}")
        
        if self.nuclear_spin is not None:
            allowed_F_values = self._get_allowed_F_values()
            if not any(np.isclose(self.F, allowed_F) for allowed_F in allowed_F_values):
                raise ValueError(f"Total angular momentum F must be in {allowed_F_values}, got {self.F}")
        
        if not (-self.F <= self.mF <= self.F):
            raise ValueError(f"Magnetic quantum number mF must satisfy -F <= mF <= F, got mF={self.mF}, F={self.F}")
        
        if not np.isclose(self.mF, round(self.mF)):
            raise ValueError(f"Magnetic quantum number mF must be integer or half-integer, got {self.mF}")
    
    def _get_allowed_F_values(self):
        if self.nuclear_spin is None:
            return []
        I = self.nuclear_spin
        F_min = abs(self.J - I)
        F_max = self.J + I
        return [F_min + i for i in range(int(F_max - F_min) + 1)]
    
    def _generate_label(self):
        L_labels = ['S', 'P', 'D', 'F', 'G', 'H', 'I']
        L_str = L_labels[self.L] if self.L < len(L_labels) else f"L{self.L}"
        return f"{self.n}{L_str}_{{{int(2*self.J)}/2}}, F={int(self.F) if self.F.is_integer() else f'{int(2*self.F)}/2'}"
    
    def __str__(self):
        return self.label
    
    def __repr__(self):
        return f"AtomicLevel({self.label}, mF={self.mF}, E={self.energy:.3e})"
    
    def __hash__(self):
        return hash((self.n, self.L, self.J, self.F, self.mF))
    
    def __eq__(self, other):
        if not isinstance(other, AtomicLevel):
            return False
        return (self.n == other.n and 
                self.L == other.L and 
                np.isclose(self.J, other.J) and
                np.isclose(self.F, other.F) and
                np.isclose(self.mF, other.mF))
