import numpy as np
import matplotlib.pyplot as plt

# Parameters
b, tau = 0.5, 0.5

# Delay exponential function
def delay_exponential(t, b, tau):
    """
    Computes the delay exponential function

    u(t) = sum_{n=0}^∞ b^n (t - n tau)^n / n! * Theta(t - n tau)

    assuming history u(0) = 1 and u(t) = 0 for -tau <= t < 0.
    """
    t = np.asarray(t, dtype=float)
    u = np.zeros_like(t, dtype=float)

    max_n = int(np.floor(np.max(t) / tau)) 

    coeff = 1.0  # b^0 / 0!

    for n in range(max_n + 1):
        shifted_t = t - n * tau
        mask = shifted_t >= 0

        u[mask] += coeff * shifted_t[mask]**n

        # update coefficient for next term: b^(n+1)/(n+1)!
        coeff *= b / (n + 1)
    return u

# Time grid
t = np.linspace(0, 8, 1000)

# Solutions
u_DDE = delay_exponential(t, b, tau)
u_ODE = np.exp(b * t)

plt.rcParams.update({
    "xtick.labelsize": 22,
    "ytick.labelsize": 22,
    "axes.labelsize": 24,
    "axes.titlesize": 26,
    "legend.fontsize": 22})

# Main plot
fig, ax = plt.subplots(figsize=(16, 10))

ax.plot(t, u_ODE, label=r"ODE solution")
ax.plot(t, u_DDE, label=r"DDE solution")

ax.set_xlabel("Time (days)")
ax.set_ylabel(r"$u(t)$")
ax.set_title("ODE Solution vs DDE Solution")
ax.legend()

plt.show()
