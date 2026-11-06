# Single Particle Motion in Magnetic Fields

This project implements a numerical framework to study single-particle trajectories in axisymmetric magnetic field configurations, with particular attention to closed orbits and separatrix dynamics.

The main idea is to exploit the conservation of energy and canonical momenta to reduce the original 3D particle dynamics to an equivalent 1D Hamiltonian system. This reduction makes it possible to study the phase space, identify different orbit families, and compute their fundamental frequencies.

## Numerical Methods

The code provides tools for:

- **Phase-space analysis:** construction of the effective potential and identification of stable and unstable equilibrium points.
- **Orbit classification:** identification of different phase-space regions, including libration and rotation regions separated by separatrices.
- **Action and frequency computation:** evaluation of the action integral and the corresponding fundamental frequency.
- **Orbit evolution:** numerical reconstruction of particle trajectories using different integration methods.

The available integration methods are:

- **LF:** Leapfrog integration of Hamilton's equations.
- **SQ:** Simpson quadrature for orbit reconstruction.
- **PI:** Polynomial interpolation followed by analytical integration.

Newton's method is also implemented for finding turning points and stationary points, with specific improvements for degenerate roots.

## Examples

### 1. Cyclotron Motion

The first example considers particle motion in a uniform magnetic field, corresponding to the classical cyclotron problem.

This configuration provides a reference case to validate the numerical methods. In particular, it allows comparison between the expected analytical motion and the trajectories obtained through numerical integration.

It is also useful for testing the computation of the action and fundamental frequency in a system without separatrix-induced energy degeneracy.

### 2. Twisted Magnetic Field Configuration

The second example investigates particle motion in a self-consistent twisted magnetic field, characterized by both axial and azimuthal magnetic field components.

Unlike the uniform field case, this configuration can exhibit multiple radial equilibria and separatrices. These features produce different families of particle trajectories, including libration and rotation orbits.

The analysis focuses on:

- The magnetic field and its q-profile.
- The structure of the effective potential and phase space.
- The classification and evolution of particle trajectories.
- The computation of the action and fundamental frequency near separatrices.
- The conservation of the magnetic moment.
- Particle transport and prompt losses in a cylindrical domain.

A particular goal is to investigate how the presence of separatrices affects particle dynamics and the validity of adiabatic invariants.

### 3. Analysis of First-Orbit Losses

The framework is used to study particle losses during the first orbit in a cylindrical confinement domain. The **loss function** distinguishes between confined and lost trajectories. For a particle starting at an initial position $r_0$, the loss function is defined as

$$
\mathcal{L}(\mathbf{r}_0) =
\begin{cases}
1 & \text{if} \; r_\text{max}(r_0) < a
\\
0 & \text{otherwise},
\end{cases}
$$

where $a$ is the cylinder radius and $\mathbf{r}_0$ denotes the initial conditions. 

By exploiting the constants of motion, the trajectory classification can be performed using only the initial radial position, energy and canonical momenta. This avoids the need to scan over all possible initial angular and axial coordinates.

The loss function can then be evaluated in terms of physically relevant quantities, such as energy, parallel velocity and pitch angle, providing a direct representation of the regions of velocity space associated with particle losses. Finally, by combining the loss function with a Maxwellian distribution $f_M(\vec{v})$, different momentum can be estimated through a velocity-space integral:

$$
\vec{u}(r_0) =
\int v\,\mathcal{L}(\mathbf{\vec{v};r_0})\,
f_M(\mathbf{\vec{v}})\,d\vec{v}, \\
T_r(r_0) =
\int \frac{v_r^2}{2}\,\mathcal{L}(\mathbf{\vec{v};r_0})\,
f_M(\mathbf{\vec{v}})\,d\vec{v},\\
T_\theta(r_0) =
\int \frac{v_r^2}{2}\,\mathcal{L}(\mathbf{\vec{v};r_0})\,
f_M(\mathbf{\vec{v}})\,d\vec{v},
$$

This approach makes it possible to investigate how first orbit losses can affect the standard Maxwellian distribution, in absence of frequent collissions (for time of the order of the cylotron period), and how they can result in anisotropy and flows.
## References

The numerical approach employed for the computation of the action and frequency follows the method described by Berg and Warnock [1]. The twisted magnetic-field configuration is inspired by the reversed-shear magnetic equilibria studied by Ogawa et al. [2] and the self-consistent Vlasov–Maxwell equilibrium developed by Cordonnier et al. [3].

References

[1] J. S. Berg and R. L. Warnock, "A Code to Compute the Action-Angle Transformation for a Particle in an Arbitrary Potential Well," Proceedings of the 1995 Particle Accelerator Conference (PAC 1995).

[2] S. Ogawa, B. Cambon, X. Leoncini, M. Vittot, D. del Castillo-Negrete, G. Dif-Pradalier, and X. Garbet, "Full Particle Orbit Effects in Regular and Stochastic Magnetic Fields," Physics of Plasmas, 23, 072506 (2016). doi.org/10.1063/1.4958653

[3] A. Cordonnier, X. Leoncini, G. Dif-Pradalier, and X. Garbet, "Full self-consistent Vlasov-Maxwell solution," Physical Review E, 106, 064209 (2022). doi.org/10.1103/PhysRevE.106.064209

