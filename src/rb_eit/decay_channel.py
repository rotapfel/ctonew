from dataclasses import dataclass
from typing import Optional
from .atomic_level import AtomicLevel


@dataclass
class DecayChannel:
    upper: AtomicLevel
    lower: AtomicLevel
    decay_rate: float
    branching_ratio: Optional[float] = None
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        if self.upper.energy <= self.lower.energy:
            raise ValueError(f"Upper level energy must be greater than lower level energy. "
                           f"Got upper={self.upper.energy:.3e}, lower={self.lower.energy:.3e}")
        
        if self.decay_rate < 0:
            raise ValueError(f"Decay rate must be non-negative, got {self.decay_rate}")
        
        if self.branching_ratio is not None:
            if not (0 <= self.branching_ratio <= 1):
                raise ValueError(f"Branching ratio must be between 0 and 1, got {self.branching_ratio}")
        
        dL = abs(self.upper.L - self.lower.L)
        if dL != 1:
            raise ValueError(f"Selection rule violation: ΔL must be ±1 for electric dipole decay, got ΔL={dL}")
        
        dJ = abs(self.upper.J - self.lower.J)
        if dJ > 1:
            raise ValueError(f"Selection rule violation: ΔJ must be 0 or ±1, got ΔJ={dJ}")
        
        dF = abs(self.upper.F - self.lower.F)
        if dF > 1:
            raise ValueError(f"Selection rule violation: ΔF must be 0 or ±1, got ΔF={dF}")
        
        dmF = abs(self.upper.mF - self.lower.mF)
        if dmF > 1:
            raise ValueError(f"Selection rule violation: ΔmF must be 0 or ±1, got ΔmF={dmF}")
    
    def __str__(self):
        return f"{self.upper.label} → {self.lower.label} (Γ={self.decay_rate:.3e})"
    
    def __repr__(self):
        br_str = f", BR={self.branching_ratio:.3f}" if self.branching_ratio is not None else ""
        return f"DecayChannel({self.upper.label} → {self.lower.label}, Γ={self.decay_rate:.3e}{br_str})"
    
    def __hash__(self):
        return hash((self.upper, self.lower))
    
    def __eq__(self, other):
        if not isinstance(other, DecayChannel):
            return False
        return self.upper == other.upper and self.lower == other.lower
