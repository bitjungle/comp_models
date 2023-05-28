# Copyright (C) 2020 BITJUNGLE Rune Mathisen
# This code is licensed under a GPLv3 license 
# See http://www.gnu.org/licenses/gpl-3.0.html 

from typing import Callable, Tuple

class SEIR_model:
    '''
    SEIR compartmental model for mathematical modelling of infectious disease.

    Source: https://www.nature.com/articles/s41421-020-0148-0#Sec6
    Assumption: No new transmissions from animals, no differences in 
    individual immunity, the time-scale of the epidemic is much faster 
    than characteristic times for demographic processes (natural birth 
    and death), and no differences in natural births and deaths.
    '''
    def __init__(self, S_start: float, E_start: float, I_start: float, R_start: float, beta: float, gamma: float, sigma: float, I_threshold: float = 0.0):
        self._S = S_start
        self._E = E_start
        self._I = I_start
        self._R = R_start
        self._beta = beta
        self._gamma = gamma
        self._sigma = sigma
        self._I_threshold = I_threshold 
        self._N = S_start + E_start + I_start + R_start
        self._time = 0

    def _dSdt(self) -> float:
        return -self._beta * self._S * self._I / self._N 

    def _dEdt(self) -> float:
        return self._beta * self._S * self._I / self._N - self._sigma * self._E

    def _dIdt(self) -> float:
        return self._sigma * self._E - self._gamma * self._I

    def _dRdt(self) -> float:
        return self._gamma * self._I 

    def _euler(self, prior: float, deriv: Callable[[], float], dt: float) -> float:
        return prior + deriv() * dt
    
    def update(self, dt: float) -> None:
        self._S = self._euler(self._S, self._dSdt, dt)
        self._E = self._euler(self._E, self._dEdt, dt)
        self._I = self._euler(self._I, self._dIdt, dt)
        self._R = self._euler(self._R, self._dRdt, dt)
        self._time += dt
        if self._I < self._I_threshold:
            adjustment = (self._I_threshold - self._I) / 2
            self._E += adjustment
            self._R += adjustment
            self._I = self._I_threshold

    @property
    def S(self) -> float:
        return self._S

    @property
    def E(self) -> float:
        return self._E

    @property
    def I(self) -> float:
        return self._I

    @property
    def R(self) -> float:
        return self._R

    @property
    def SEIR(self) -> Tuple[float, float, float, float]:
        return self._S, self._E, self._I, self._R

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
    def sigma(self) -> float:
        return self._sigma

    @sigma.setter
    def sigma(self, sigma: float) -> None:
        self._sigma = sigma

    @property
    def time(self) -> float:
        return self._time

if __name__ == "__main__":
    pass
