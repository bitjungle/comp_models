# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

from typing import Callable, Tuple

class SIR_model:
    '''
    SIR compartmental model for mathematical modelling of infectious disease.

    Source: https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model
    The model consists of three compartments: S for the number of susceptible, 
    I for the number of infectious, and R for the number recovered (or immune) 
    individuals. This model is reasonably predictive for infectious diseases 
    which are transmitted from human to human, and where recovery confers 
    lasting resistance, such as measles, mumps and rubella. 
    '''
    def __init__(self, S_start: float, I_start: float, R_start: float, beta: float, gamma: float, I_threshold: float = 0.0):
        self._S = S_start
        self._I = I_start
        self._R = R_start
        self._beta = beta
        self._gamma = gamma
        self._I_threshold = I_threshold 
        self._N = S_start + I_start + R_start
        self._time = 0

    def _dSdt(self) -> float:
        return -self._beta * self._I * self._S / self._N

    def _dIdt(self) -> float:
        return self._beta * self._I * self._S / self._N - self._gamma * self._I

    def _dRdt(self) -> float:
        return self._gamma * self._I

    def _euler(self, prior: float, deriv: Callable[[], float], dt: float) -> float:
        return prior + deriv() * dt

    def update(self, dt: float) -> None:
        self._S = self._euler(self._S, self._dSdt, dt)
        self._I = self._euler(self._I, self._dIdt, dt)
        self._R = self._euler(self._R, self._dRdt, dt)
        self._time += dt
        if self._I < self._I_threshold:
            adjustment = (self._I_threshold - self._I) / 2
            self._S += adjustment
            self._R += adjustment
            self._I = self._I_threshold

    @property
    def S(self) -> float:
        return self._S

    @property
    def I(self) -> float:
        return self._I

    @property
    def R(self) -> float:
        return self._R

    @property
    def SIR(self) -> Tuple[float, float, float]:
        return self._S, self._I, self._R

    @property
    def N(self) -> float:
        return self._N

    @property
    def R0(self) -> float:
        return self._beta / self._gamma

    @property
    def beta(self) -> float:
        return self._beta

    @beta.setter
    def beta(self, beta: float) -> None:
        self._beta = beta
    
    @property
    def gamma(self) -> float:
        return self._gamma

    @gamma.setter
    def gamma(self, gamma: float) -> None:
        self._gamma = gamma

    @property
    def time(self) -> float:
        return self._time

if __name__ == "__main__":
    pass
