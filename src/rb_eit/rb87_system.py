from typing import List, Dict
import numpy as np
from .atomic_level import AtomicLevel
from .transition import Transition
from .decay_channel import DecayChannel
from .constants import (
    HBAR, PI,
    RB87_GROUND_HFS_A, RB87_5P12_HFS_A, RB87_5P32_HFS_A, RB87_5P32_HFS_B,
    RB_D1_REDUCED_DIPOLE, RB_D2_REDUCED_DIPOLE,
    RB_D_LINE_DECAY_RATE, RB87_NUCLEAR_SPIN
)


class Rb87System:
    
    def __init__(self):
        self.nuclear_spin = RB87_NUCLEAR_SPIN
        self.ground_states = self._create_ground_states()
        self.excited_states_5p12 = self._create_5p12_states()
        self.excited_states_5p32 = self._create_5p32_states()
        self.all_excited_states = self.excited_states_5p12 + self.excited_states_5p32
        self.transitions_d1 = self._create_d1_transitions()
        self.transitions_d2 = self._create_d2_transitions()
        self.all_transitions = self.transitions_d1 + self.transitions_d2
        self.decay_channels = self._create_decay_channels()
    
    def _hyperfine_energy(self, A, B, I, J, F):
        K = F * (F + 1) - I * (I + 1) - J * (J + 1)
        if J == 0.5:
            omega = 0.5 * A * K
        else:
            term1 = 0.5 * A * K
            term2 = B * (1.5 * K * (K + 1) - 2 * I * (I + 1) * J * (J + 1))
            term2 /= (2 * I * (2 * I - 1) * 2 * J * (2 * J - 1))
            omega = term1 + term2
        return HBAR * omega
    
    def _create_ground_states(self):
        I = self.nuclear_spin
        J = 0.5
        F_values = [1, 2]
        
        states = []
        for F in F_values:
            energy = self._hyperfine_energy(RB87_GROUND_HFS_A, 0, I, J, F)
            level = AtomicLevel(
                n=5, L=0, J=J, F=float(F), mF=0.0,
                energy=energy,
                label=f"5S_1/2, F={F}",
                nuclear_spin=I
            )
            states.append(level)
        
        return states
    
    def _create_5p12_states(self):
        I = self.nuclear_spin
        J = 0.5
        F_values = [1, 2]
        
        from .constants import C, RB_D1_WAVELENGTH
        h = 6.62607015e-34
        base_energy = h * C / RB_D1_WAVELENGTH
        
        states = []
        for F in F_values:
            hf_energy = self._hyperfine_energy(RB87_5P12_HFS_A, 0, I, J, F)
            energy = base_energy + hf_energy
            level = AtomicLevel(
                n=5, L=1, J=J, F=float(F), mF=0.0,
                energy=energy,
                label=f"5P_1/2, F={F}",
                nuclear_spin=I
            )
            states.append(level)
        
        return states
    
    def _create_5p32_states(self):
        I = self.nuclear_spin
        J = 1.5
        F_values = [0, 1, 2, 3]
        
        from .constants import C, RB_D2_WAVELENGTH
        h = 6.62607015e-34
        base_energy = h * C / RB_D2_WAVELENGTH
        
        states = []
        for F in F_values:
            hf_energy = self._hyperfine_energy(RB87_5P32_HFS_A, RB87_5P32_HFS_B, I, J, F)
            energy = base_energy + hf_energy
            level = AtomicLevel(
                n=5, L=1, J=J, F=float(F), mF=0.0,
                energy=energy,
                label=f"5P_3/2, F={F}",
                nuclear_spin=I
            )
            states.append(level)
        
        return states
    
    def _calculate_clebsch_gordan_squared(self, F_lower, F_upper, J_lower, J_upper):
        dF = abs(F_upper - F_lower)
        if dF > 1:
            return 0.0
        
        if J_lower == 0.5 and J_upper == 0.5:
            if F_upper == F_lower:
                return 0.5
            else:
                return 0.5
        elif J_lower == 0.5 and J_upper == 1.5:
            F_max = max(F_lower, F_upper)
            F_min = min(F_lower, F_upper)
            return (2 * F_max + 1) / (2 * J_upper + 1) / (2 * J_lower + 1)
        
        return 1.0 / (2 * J_upper + 1)
    
    def _create_d1_transitions(self):
        transitions = []
        for ground in self.ground_states:
            for excited in self.excited_states_5p12:
                dF = abs(excited.F - ground.F)
                if dF <= 1 and not (excited.F == 0 and ground.F == 0):
                    cg_squared = self._calculate_clebsch_gordan_squared(
                        ground.F, excited.F, ground.J, excited.J
                    )
                    dipole_moment = RB_D1_REDUCED_DIPOLE * np.sqrt(cg_squared)
                    
                    trans = Transition(
                        lower=ground,
                        upper=excited,
                        dipole_moment=dipole_moment
                    )
                    transitions.append(trans)
        
        return transitions
    
    def _create_d2_transitions(self):
        transitions = []
        for ground in self.ground_states:
            for excited in self.excited_states_5p32:
                dF = abs(excited.F - ground.F)
                if dF <= 1 and not (excited.F == 0 and ground.F == 0):
                    cg_squared = self._calculate_clebsch_gordan_squared(
                        ground.F, excited.F, ground.J, excited.J
                    )
                    dipole_moment = RB_D2_REDUCED_DIPOLE * np.sqrt(cg_squared)
                    
                    trans = Transition(
                        lower=ground,
                        upper=excited,
                        dipole_moment=dipole_moment
                    )
                    transitions.append(trans)
        
        return transitions
    
    def _create_decay_channels(self):
        channels = []
        
        for excited in self.all_excited_states:
            total_branching = 0.0
            excited_channels = []
            
            for ground in self.ground_states:
                dF = abs(excited.F - ground.F)
                if dF <= 1 and not (excited.F == 0 and ground.F == 0):
                    cg_squared = self._calculate_clebsch_gordan_squared(
                        ground.F, excited.F, ground.J, excited.J
                    )
                    excited_channels.append((ground, cg_squared))
                    total_branching += cg_squared
            
            for ground, cg_squared in excited_channels:
                branching_ratio = cg_squared / total_branching if total_branching > 0 else 0
                decay_rate = RB_D_LINE_DECAY_RATE * branching_ratio
                
                channel = DecayChannel(
                    upper=excited,
                    lower=ground,
                    decay_rate=decay_rate,
                    branching_ratio=branching_ratio
                )
                channels.append(channel)
        
        return channels
    
    def get_transition(self, lower_label: str, upper_label: str) -> Transition:
        for trans in self.all_transitions:
            if trans.lower.label == lower_label and trans.upper.label == upper_label:
                return trans
        raise ValueError(f"Transition {lower_label} → {upper_label} not found")
    
    def get_level(self, label: str) -> AtomicLevel:
        all_levels = self.ground_states + self.all_excited_states
        for level in all_levels:
            if level.label == label:
                return level
        raise ValueError(f"Level {label} not found")
    
    def total_decay_rate(self, level: AtomicLevel) -> float:
        total = 0.0
        for channel in self.decay_channels:
            if channel.upper == level:
                total += channel.decay_rate
        return total
    
    def __repr__(self):
        return (f"Rb87System(ground_states={len(self.ground_states)}, "
                f"excited_states={len(self.all_excited_states)}, "
                f"transitions={len(self.all_transitions)})")
