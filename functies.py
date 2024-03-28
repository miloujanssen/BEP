import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.integrate import quad

class Functies:
    """De waterbouwkundige functies om de energie te bepalen"""

    def lambda_berekenen(self, A_t, A_b, g, xi_v, xi_t, n_trbn):
        mu = A_t * math.sqrt((2 * g) / (xi_v + xi_t))
        lmbda = n_trbn * mu / A_b
        return lmbda

    def bereken_mu_M2(self, omega_M2, a_M2, lmbda, F):
        mu_M2 = (-lmbda**2 * F**2 + math.sqrt(lmbda**4 * F**4 + 4 * omega_M2**4 * a_M2**2)) / (2 * a_M2 * omega_M2**2)
        return mu_M2

    def bereken_theta_M2(self, mu_M2, omega_M2, a_M2, lmbda, F):
        x = (lmbda * F * np.sqrt(mu_M2)) / (-omega_M2 * np.sqrt(a_M2))
        y = mu_M2
        return np.arctan2(y, x) 

    def bereken_mu_S2(self, omega_S2, lmbda, F, a_M2):
        mu_S2 = (-lmbda**2 * F**2 + math.sqrt(lmbda**4 * F**4 + 4 * omega_S2**4 * a_M2**2)) / (2 * omega_S2**2 * a_M2)
        return mu_S2

    def bereken_theta_S2(self, mu_S2, lmbda, F, omega_S2, a_M2):
        x = (lmbda * F * np.sqrt(mu_S2)) / (- omega_S2 * np.sqrt(a_M2))
        y = mu_S2
        return np.arctan2(y, x)

    def bereken_F(self, a_rel):
        if a_rel < 1:
            F = (-0.2169 * a_rel**3 + 0.4699 * a_rel**2 - 0.0103 * a_rel + 0.8990)**(-1)
        else:
            F = (0.0003 * a_rel**3 - 0.0118 * a_rel**2 + 0.2872 * a_rel + 0.8643)**(-1)
        return F

    def bereken_zeta_z(self, t, A0, a_M2, omega_M2, phi_M2, a_S2, omega_S2, phi_S2):
        return A0 + a_M2 * np.sin(omega_M2 * t - phi_M2) + a_S2 * np.sin(omega_S2 * t - phi_S2)

    def bereken_delta_h(self, t, mu_M2, mu_S2, a_M2, a_S2, omega_M2, phi_M2, theta_M2, omega_S2, phi_S2, theta_S2):
        term_M2 = mu_M2 * a_M2 * np.sin(omega_M2 * t - phi_M2 - theta_M2)
        term_S2 = mu_S2 * a_S2 * np.sin(omega_S2 * t - phi_S2 - theta_S2)
        return term_M2 + term_S2

    def delta_h_over_sqrt_delta_h(self, t, F, a_M2, mu_M2, a_S2, mu_S2, omega_M2, phi_M2, theta_M2, omega_S2, phi_S2, theta_S2):
        term_M2 = np.sqrt(mu_M2) * a_M2 * np.sin(omega_M2 * t - phi_M2 - theta_M2)
        term_S2 = np.sqrt(mu_S2) * a_S2 * np.sin(omega_S2 * t - phi_S2 - theta_S2)
        return (F * (1/a_M2)) * (term_M2 + term_S2)

    def bereken_debiet(self, A_t, g, xi_v, xi_t, n_trbn, term):
        return A_t * np.sqrt(2 * g / (xi_v + xi_t)) * term * n_trbn

    def bereken_vermogen(self, rho, g, A_t, xi_v, xi_t, delta_h, n_trbn):
        return rho * g * np.sqrt(2 * g) * A_t * (xi_t / (xi_v + xi_t)**(3/2)) * np.abs(delta_h)**(3/2) * n_trbn
    
    def energie_berekenen(self, delta_h_waarden, rho, g, A_t, xi_v, xi_t, n_trbn):
        def integraal(t):
            index = int(t * len(delta_h_waarden))
            if index < 0:
                index = 0
            elif index >= len(delta_h_waarden):
                index = len(delta_h_waarden) - 1
            return np.abs(delta_h_waarden[index]) ** 1.5

        resultaat_integraal, _ = quad(integraal, 0, 29.25 * 24 * 3600)
        
        E = rho * g * math.sqrt(2 * g) * A_t * (xi_t / (xi_v + xi_t)** (3/2)) * n_trbn * resultaat_integraal
        return E