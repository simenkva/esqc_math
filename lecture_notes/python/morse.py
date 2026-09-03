"""
HF Morse potential + analytical bound-state eigenvalues/eigenfunctions.

Model:
    V(r) = D_e (1 - exp[-a (r - r_e)])^2 - D_e
so that V(r_e) = -D_e and V(∞) = 0.

Bound-state energies (analytic):
    E_n = - (ħ^2 a^2 / (2 μ)) * (λ - n - 1/2)^2
with
    λ = sqrt(2 μ D_e) / (ħ a)
and n = 0, 1, ..., n_max where λ - n - 1/2 > 0.

Eigenfunctions (analytic, up to normalization):
Let x = r - r_e (in meters) and y = 2 λ exp(-a x).
Define s_n = λ - n - 1/2.
Then
    ψ_n(y) ∝ y^{s_n} exp(-y/2) L_n^{(2 s_n)}(y)
where L_n^{(α)} are associated Laguerre polynomials.

We compute ψ_n on an r-grid and normalize numerically.

Requirements:
    numpy, matplotlib, scipy (for associated Laguerre polynomials)
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from  plotsetup import *

from scipy.special import eval_genlaguerre

# -------------------------
# Physical constants (SI)
# -------------------------
u = 1.66053906660e-27          # kg
c = 299792458.0                # m/s
hbar = 1.054571817e-34         # J*s
eV = 1.602176634e-19           # J

# -------------------------
# HF parameters (typical)
# -------------------------
re_A_default = 0.9168          # Å
De_eV_default = 6.12           # eV (approx.; De > D0)
omega_e_cm_default = 4138.0    # cm^-1

mH_u = 1.00782503223
mF_u = 18.998403163
mu = (mH_u*mF_u/(mH_u+mF_u)) * u  # reduced mass in kg


def morse_params_from_De_omega(re_A, De_eV, omega_e_cm):
    """
    Given r_e (Å), D_e (eV), ω_e (cm^-1), compute Morse 'a' (1/Å) using
        k = μ (2π c ω_e)^2
        k = 2 D_e a^2
    """
    omega = 2*np.pi * c * (omega_e_cm * 100.0)  # rad/s
    k = mu * omega**2                            # N/m
    De_J = De_eV * eV
    a_inv_m = np.sqrt(k/(2*De_J))                # 1/m
    a_inv_A = a_inv_m * 1e-10                    # 1/Å
    return a_inv_A, k


def morse_potential(r_A, re_A, De_eV, a_inv_A):
    """Morse potential in eV; r_A, re_A in Å; a in Å^-1."""
    return De_eV * (1 - np.exp(-a_inv_A*(r_A - re_A)))**2 - De_eV


def bound_state_energies(De_eV, a_inv_A):
    """
    Analytical energies in eV for the shifted Morse potential (V(∞)=0).
    """
    De_J = De_eV * eV
    a_inv_m = a_inv_A * 1e10
    lam = np.sqrt(2*mu*De_J)/(hbar*a_inv_m)
    n_max = int(np.floor(lam - 0.5))
    ns = np.arange(0, n_max+1)
    En_J = - (hbar**2 * a_inv_m**2)/(2*mu) * (lam - ns - 0.5)**2
    En_eV = En_J / eV
    return lam, ns, En_eV


def morse_eigenfunction(r_A, n, re_A, De_eV, a_inv_A, lam):
    """
    Compute ψ_n(r) on grid r_A (Å). Returns normalized ψ_n (units: 1/sqrt(Å))
    via numerical normalization.
    """
    x_m = (r_A - re_A) * 1e-10
    a_inv_m = a_inv_A * 1e10
    y = 2*lam*np.exp(-a_inv_m*x_m)

    s = lam - n - 0.5
    if s <= 0:
        raise ValueError("Requested n exceeds bound-state limit (s_n <= 0).")

    # Associated Laguerre: L_n^{(α)}(y) with α = 2s
    L = eval_genlaguerre(n, 2*s, y)

    psi = (y**s) * np.exp(-y/2) * L

    # Numerical normalization: ∫ |ψ|^2 dr = 1 (dr in Å here)
    norm = np.sqrt(np.trapz(psi**2, r_A))
    return psi / norm


ap = argparse.ArgumentParser()
ap.add_argument("-m", type=int, default=0, help="number of lowest states to plot")
ap.add_argument("--re", type=float, default=re_A_default, help="r_e in Å")
ap.add_argument("--De", type=float, default=De_eV_default, help="D_e in eV")
ap.add_argument("--omegae", type=float, default=omega_e_cm_default, help="ω_e in cm^-1")
ap.add_argument("--rmin", type=float, default=0.45, help="r-min in Å for plotting")
ap.add_argument("--rmax", type=float, default=3.0, help="r-max in Å for plotting")
args = ap.parse_args()

re_A = args.re
De_eV = args.De
omega_e_cm = args.omegae

a_inv_A, k = morse_params_from_De_omega(re_A, De_eV, omega_e_cm)
lam, ns, En_eV = bound_state_energies(De_eV, a_inv_A)

n_bound = len(ns)
m = min(args.m, n_bound)

r = np.linspace(args.rmin, args.rmax, 1200)
V = morse_potential(r, re_A, De_eV, a_inv_A)



fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(r, V, label="Morse potential")

# scale for visualizing wavefunctions on an energy plot
dE = float(np.abs(En_eV[1] - En_eV[0])) if m >= 2 else 0.8
scale = 0.35 * dE

for i in range(m):
    n = int(ns[i])
    E = float(En_eV[i])

    psi = morse_eigenfunction(r, n, re_A, De_eV, a_inv_A, lam)

    ax.hlines(E, r[0], r[-1], linewidth=0.8)
    ax.plot(r, E + scale*psi, linewidth=1.2)

#ax.axhline(0, linewidth=1)
#ax.axvline(re_A, linestyle="--", linewidth=1)

ax.set_xlabel(r"Internuclear distance $r$ (Å)")
ax.set_ylabel(r"Energy / Potential (eV)")
ax.set_title(
    "Morse potential"
#    rf"$D_e$={De_eV:.2f} eV, $r_e$={re_A:.4f} Å, $a$={a_inv_A:.3f} Å$^{{-1}}$, "
#    rf"$N_{{\rm bound}}$={n_bound}"
)
ax.set_xlim(r.min(), r.max())
ax.set_ylim(min(V.min(), En_eV[0]) - 0.6, 1.8)
ax.grid(True, alpha=0.25)

E_1 = -5
ax.axhline(E_1, linestyle="--", color="C1", linewidth=1)
ax.text(r[-1], E_1, f"$E_1$={E_1:.2f} eV", color="black", fontsize=10, va="bottom", ha="right")

E_2 = 0.5
ax.axhline(E_2, linestyle="--", color="C1", linewidth=1)
ax.text(r[-1], E_2, f"$E_2$={E_2:.2f} eV", color="black", fontsize=10, va="bottom", ha="right")

# compute crossing points for E_1 and E_2
def find_crossings(r, V, E):
    """Find r-values where V(r) crosses E."""
    crossings = []
    for i in range(len(r) - 1):
        if (V[i] - E) * (V[i + 1] - E) < 0:
            # Linear interpolation to find crossing point
            r_cross = r[i] + (r[i + 1] - r[i]) * (E - V[i]) / (V[i + 1] - V[i])
            crossings.append(r_cross)
    return crossings

crossings_E1 = find_crossings(r, V, E_1)

crossings_E2 = find_crossings(r, V, E_2)

counter = 1

for i, r_cross in enumerate(crossings_E2):
    label = f"$r_{{{counter}}}$"
    ax.axvline(r_cross, linestyle="--", color="C1", linewidth=1)
    ax.text(r_cross+.025, ax.get_ylim()[0], f"{label}", color="black", fontsize=12, va="bottom", ha="left")
    counter += 1

for i, r_cross in enumerate(crossings_E1):
    label = f"$r_{{{counter}}}$"
    ax.axvline(r_cross, linestyle="--", color="C1", linewidth=1)
    ax.text(r_cross+.025, ax.get_ylim()[0], f"{label}", color="black", fontsize=12, va="bottom", ha="left")
    counter += 1
    

    

plt.tight_layout()
# set transparent background
plt.savefig("../figures/exercises/morse_potential_exercise.svg", transparent=True)
plt.show()

