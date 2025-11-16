from typing import Optional, Tuple
import numpy as np
from .atomic_level import AtomicLevel
from .transition import Transition
from .laser_field import LaserField
from .rb87_system import Rb87System
from .rb85_system import Rb85System


class DoubleLambdaSystem:
    
    def __init__(
        self,
        isotope: str = "Rb87",
        ground_state_1_label: Optional[str] = None,
        ground_state_2_label: Optional[str] = None,
        excited_state_label: Optional[str] = None,
        pump_rabi_frequency: float = 2 * np.pi * 10e6,
        probe_rabi_frequency: float = 2 * np.pi * 1e6,
        pump_detuning: float = 0.0,
        probe_detuning: float = 0.0,
    ):
        if isotope == "Rb87":
            self.atomic_system = Rb87System()
            default_g1 = "5S_1/2, F=1"
            default_g2 = "5S_1/2, F=2"
            default_e = "5P_3/2, F=2"
        elif isotope == "Rb85":
            self.atomic_system = Rb85System()
            default_g1 = "5S_1/2, F=2"
            default_g2 = "5S_1/2, F=3"
            default_e = "5P_3/2, F=3"
        else:
            raise ValueError(f"Unknown isotope: {isotope}. Must be 'Rb87' or 'Rb85'")
        
        self.isotope = isotope
        
        self.ground_state_1 = self.atomic_system.get_level(
            ground_state_1_label if ground_state_1_label else default_g1
        )
        self.ground_state_2 = self.atomic_system.get_level(
            ground_state_2_label if ground_state_2_label else default_g2
        )
        self.excited_state = self.atomic_system.get_level(
            excited_state_label if excited_state_label else default_e
        )
        
        self.transition_1 = self.atomic_system.get_transition(
            self.ground_state_1.label, self.excited_state.label
        )
        self.transition_2 = self.atomic_system.get_transition(
            self.ground_state_2.label, self.excited_state.label
        )
        
        self.pump = LaserField(
            rabi_frequency=pump_rabi_frequency,
            detuning=pump_detuning,
            frequency=self.transition_1.frequency
        )
        
        self.probe = LaserField(
            rabi_frequency=probe_rabi_frequency,
            detuning=probe_detuning,
            frequency=self.transition_2.frequency
        )
        
        self._validate()
    
    def _validate(self):
        if self.ground_state_1 == self.ground_state_2:
            raise ValueError("Ground states must be different for double-lambda configuration")
        
        if self.ground_state_1.energy >= self.excited_state.energy:
            raise ValueError("Ground state 1 energy must be less than excited state energy")
        
        if self.ground_state_2.energy >= self.excited_state.energy:
            raise ValueError("Ground state 2 energy must be less than excited state energy")
        
        if self.ground_state_1.L != self.ground_state_2.L:
            raise ValueError("Both ground states should have same L for typical double-lambda")
        
        if abs(self.ground_state_1.J - self.ground_state_2.J) > 0.01:
            raise ValueError("Both ground states should have same J for typical double-lambda")
    
    def two_photon_detuning(self) -> float:
        return self.pump.detuning - self.probe.detuning
    
    def eit_susceptibility(self, probe_detuning_scan: np.ndarray) -> np.ndarray:
        gamma = self.atomic_system.total_decay_rate(self.excited_state)
        omega_pump = self.pump.rabi_frequency
        omega_probe = self.probe.rabi_frequency
        delta_pump = self.pump.detuning
        
        susceptibility = np.zeros(len(probe_detuning_scan), dtype=complex)
        
        for i, delta_probe in enumerate(probe_detuning_scan):
            delta_2photon = delta_pump - delta_probe
            
            denominator = (delta_probe + 1j * gamma / 2) + (
                omega_pump**2 / (4 * (delta_2photon + 1j * 1e-6))
            )
            
            susceptibility[i] = omega_probe**2 / denominator
        
        return susceptibility
    
    def rabi_frequencies(self) -> Tuple[float, float]:
        return (self.pump.rabi_frequency, self.probe.rabi_frequency)
    
    def detunings(self) -> Tuple[float, float]:
        return (self.pump.detuning, self.probe.detuning)
    
    def set_pump_parameters(self, rabi_frequency: float, detuning: float):
        self.pump.rabi_frequency = rabi_frequency
        self.pump.detuning = detuning
    
    def set_probe_parameters(self, rabi_frequency: float, detuning: float):
        self.probe.rabi_frequency = rabi_frequency
        self.probe.detuning = detuning
    
    def __repr__(self):
        return (f"DoubleLambdaSystem({self.isotope}, "
                f"|1⟩={self.ground_state_1.label}, "
                f"|2⟩={self.ground_state_2.label}, "
                f"|e⟩={self.excited_state.label})")
    
    def __str__(self):
        return (f"Double-Lambda EIT Configuration ({self.isotope}):\n"
                f"  Ground State 1: {self.ground_state_1.label}\n"
                f"  Ground State 2: {self.ground_state_2.label}\n"
                f"  Excited State:  {self.excited_state.label}\n"
                f"  Pump:  Ω={self.pump.rabi_frequency/1e6/2/np.pi:.2f} MHz, "
                f"Δ={self.pump.detuning/1e6/2/np.pi:.2f} MHz\n"
                f"  Probe: Ω={self.probe.rabi_frequency/1e6/2/np.pi:.2f} MHz, "
                f"Δ={self.probe.detuning/1e6/2/np.pi:.2f} MHz")
