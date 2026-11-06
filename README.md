<header>

# Simulatie single particle motion in a given magnetic field configuration
The code is created from scratch and aims to test a new method for solving close orbits trajectory. It solves one dimensional dynamics, 2D differential equation in the phase space, using the energy and z-momentum constants of motion to reduce the dimensionality from 3D3V to 1D1V. Furthermore, it exploits the symmetry (v,t) -> (-v,-t) of the trajectory by solving the motion in the lower v-semiplane from the resolved motion in the upper semiplane.
The energy, given the $\theta$ and $z$ momentums $p_\theta, p_z$, labels the trajectory (x,v)(t) in the phase space. While the orbit in the phase-space is obtained analytically, the time dependence is solved via numerical integrations, or with numerical methods for differential equation. Note that the relation between the energy and trajectories is not bijective -- a trajectory has an unique value of energy but not vice-versa. This means that there can be some degeneracy in the energy. Here, the we will consider the case when the degeneracy is due to the presence of a separatrix, or more. 
</header>

## Symmetries of the problem

The magnetic field has no dependence on the variable $z, \theta$, thus it's derivative against them is equal to 0. At the same time also the Magnetic Vector is indipendet on these variables. Therefore, these variables do not appear neither in the Hamiltonian $H=H(\vec{p},r)$. Here, we focused in a megnetic geometry with an O-point. In particular, the O-point can have a magnetic field on its axis, which naturally lead to the choice of cartesian coordinates. In cartesian coordinates the Hamiltonian is:
$$
H =\frac{(\vec{p}-\vec{A})^2}{2} = \frac{p_r^2}{2} + \frac{(p_\theta-0.5B_0r)^2}{2r^2}+\frac{(p_z-A_z(r))^2}{2}
$$

With the symmetries assumptions for $\theta$ and $z$, we find that the momentums of the cyclic coordinates are constant of motion:

$$
\begin{align}
 \dot{p}_\theta = - \frac{\partial H}{\partial \theta} = 0 \\

 \dot{p}_z = - \frac{\partial H}{\partial z} = 0
\end{align}
$$

This means that the $p_\theta$, $p_z$, and $E$ are constants of motions of the system. They can be seen as 'parameters' of the trajectory, since they are dynamical quantities that do not vary with the time. The evolution in time of the coordinate is less simple:

$$
\dot{\theta} = \frac{\partial H}{\partial p_\theta} = \frac{p_\theta}{r^2(t)}-\frac{B_0}{2} \\
\dot{z} = \frac{\partial H}{\partial p_z} = p_z-A_z(r(t))
$$

The two coordinates are not straightfoward to integrate: it also requires the knowledge of $r(t)$, which has to be integrated numerically.

## The reduced to 1D hamiltonian system

The dynamics can be solve starting from the equation of motion for $r(t)$. Since it is decoupled from the other coordinates, we can reduce the system to a 1D-Hamiltonian system. This allows to study qualitativly the phase space, and to procede in a more straigthforward way with the integration
$$ 
H(r, p_r) = \frac{p_r^2}{2} + V_{eff}(r)$$
where the effective potential is defined as
$$
V_{eff}(r) = \frac{(p_\theta-0.5B_0r)^2}{2r^2}+\frac{(p_z-A_z(r))^2}{2}
$$
## Qualitative study of closed orbits

The qualitative study in this context simply reduce in a study of the function $V_\text{eff}$ and in the identification of 'closed' regions. Note that in the context of this study the orbits are always closed.
1. The stationary points (*max/min*): they can be stable (O-point) or unstable (X-point);
2. The basin of attraction: the regions where the orbits do not leave, and defined by stationary points.

## Computation of fundamental frequency

This method is taken from the work of Berk et Warnock. Their approach relies on the fundamental relations between the action function $J(E)$ and the fundamental frequency $\omega=\partial_EJ$, and the relation between the action variable and the phase-space area encopassed by an orbit $J(E) =\oint_\gamma p \,dq$. Their method computes the action integral, using a specific change of variable that make the convergence faster. They also point out that it is possible to compute the phase $\Phi(t)$ using an integration techniques, but it seems that it cannot reach the convergence as expected.

In this work, the method is implemented and adapted to deal with the presence of energy degeneracy by introducing regions where the function $J(E)$ is monotonic. In particular, the regions stratify the phase space.

### Numerical method
The main numerical methods are:

- Newton root finding algorithm 
- Simpson integration method

<u>Note</u>: the root finding algorithm has been modify to handle points that are both roots and stationary points. Indeed, such points would not converge in the standard Newton algorithm because the first derivative becomes negligible so that the algorithm would not 'move' the point along to the correct result with enought speed. In the context of solving the dynamics in 1D-Hamiltonian system, it is relevant when considering a trajectory near to the stationary point (minimum) or a separatrix (maximum).

#### Dealing with energy degeneracy

In the noteboook 'Berg et Warnock' a numerical technique has been developed to resolve the degeneracy in the presence of a separatrix. The regions due to a single X point  has been labeled (a,b,c). In particular, they identify the left and right lobes in the separatrix, which correspond to libration motion, and the region out of the separatrix, which is the rotation motion. The pseudo-code is the following

    # pseudo-code for energy degeneracy
    
    # find the 2D-intervals (regions) from O-points and X-points (max/min of V)
    
    # compute the equilibriums

    equilibrium = find_stationary(V)
    equilibrium = add_boundary(grid, V)
    while len(equilibrium) > 2:
        try regions.find_a_region()
    equilibrim.remove('all')

    def find_region():
        # build the regions in phase-space starting from the lowest energy. If neighborh points have the same energy, they lie on the same separatrix, thus we have only one region. 
        # The method discard the first point and work with the other. After the region has been built, then the point is discarded

        i = argmin(equilibrium['Energy'])
        if equilibrium['Energy'][i] == equilibrium['Energy'][i+1] .or. equilibrium['Energy'][i] == equilibrium['Energy'][i-1]:
            equilibrium.remove(i)
        else:
            regions.append(alphabeth(j))
            Emax, Emin = energy_range(i)
            regions.append(Emax)
            regions.append(Emin)
            xmax, xmin = position_range(i)
            regions.append(xmax)
            regions.append(xmin)
            equilibrium.remove(i)
    
    def position_range(i):
        # at the lowest energy unexplored the position range is limited by the neighbors!

        xmin = equilibrium[i-1]
        xmax = equilibrium[i+1]
        return xmax, xmin
        
    def Energy_range(i):
        # at the lowest energy explored, the energy is bounded by the lowest energy (the one of the point) and the lowest energy between the neigbohrs.

        Emin = equilibrium[i]
        Emax = min(equilibrium[i+1], equilibrium[i-1])
        return Emax, Emin

    def remove(i)
        for key, value in equilibrium:
            equilibrium[key] = np.argremove(i, value)
    
    def alphabeth(j):
        word = ''
        letters = np.array(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])
        while j < 0
            u = mod(j, 26) 
            word.append(letters[u-1])
            j = (j-u)/26
        return word

    # associate to each trajectory a label to resolve the degeneracy
    for trajectory in df:
        trajectory.getlabel()

    def getlabel():
        regions = regions.label
        maskx = regions.xmax >= trajectory.xmax .and. regions.xmin <= trajectory.xmin
        if sum(maskx) == 1:
            mask = maskx
        else
            mask2 = regions.Emax >= trajectory.E .and. regions.Emin <= trajectory.E
            mask = maskx*maskE
        trajectory.label = region.label[mask]

#### The Numerical method for $J(E_{\alpha})$ and $\omega(E_{\alpha})$

The method to compute $J(E)$ simply rely on the assumption that there is no degeneracy in energy of the system. This can be extended to the degenerate one by considering separatly each degenerate regions.

    # Class initializing arguments
    Ham.V(x)
    Ham.Egrid
    Ham.xgrid

    # Class methods
    Ham.p(x, E)
    Ham.turn_points()
    Ham.turn_points.findturningpoints(E)
    Ham.regions.findregion()
    Ham.trajectories.findtrajectory()
    Ham.trajectories.getlabel()
    Ham.trajectories.computeJ()
    Ham.trajectories.computeomega()

    # Class attributes
    Ham.trajectories() # dataframe ['dummyindex', 'xmin', 'xmax',
                                     'E', 'label', 'J','omega']
    Ham.regions()      # dataframe ['label', 'xmin', 'xmax', 'Emin', 'Emax']

The computation of $J(E_\alpha)$, which stands for the action for the trajectory with energy $E$ in the degeneracy $\alpha$, is done using a change of variable suggested in the paper of  Berk et Warnock.
$$
q(x; E) =  \frac{x_1+x_2}{2} + \frac{x_1-x_2}{2}\cos{(x)}

$$
where $x_1(E)$, $x_2(E)$ are function of the orbit's energy $E$, and represent the inversion points of the obrit. This is implemented in the following way.

    # Change of Variable
    Ham.ugrid = linspace(0,2*pi, Nu)
    def x(u, x1,x2): 
        return x1/2*(1+np.cos(u)) + x2/2*(1-np.cos(u))
The computation of the action emploies a standard trapezoidal method.

    # Integration method
    def simpson(y, dx):
        integral = dx/3*(y[0] + y[len(y)-1])
        for i in range(1, int((len(y)-1)/2)):
            integral = integral + 4*dx/3* y[2*i - 1]
        for i in range(1, int((len(y)-1)/2-1)):
            integral = integral + 2*dx/3*y[2*i]
        return integral
    
    # Method to compute J
    def computeJ():
        trajectories.J = []
        for index in trajectory['dummyindex']: 
            x1,x2 = trajectory['xmin'][index], trajectory['xmax'][index]
            x_q = x(Ham.ugrid, x1,x2)
            pj = p(qj, H[i])
            du = uj[1]-uj[0]
            integrand_J = np.sin(uj)*pj
            J = (1/np.pi*(root[i][1]-root[i][0])/2*simpson(integrand_J,du))
            trajectories.J.append(J)

The computation of $\omega$ instead relies on a simpler finite difference method. For the extreme points of $\[E_{min},E_{max}\], a forward/backward derivative is used, while for the other points a central derivative is used.

    def computeomega():
        trajectory.omega = trajectory.J
        for label in regions.label:
            mask = trajectories.label == label
            E_tmp = trajectories.E[mask]
            arg = argsort(E_tmp)
            E_tmp = E_tmp[arg]
            index = trajectories.dummyindex[mask][arg]
            J_tmp = trajctories.J[mask][arg]
            trajectory.omega[index[1]] = [(J_tmp[1]-J_tmp[0])/(E_tmp[1]-E_tmp[0])]
            for i in range(1,len(E_tmp)-1):
                trajectory.omega[index[i]] = ((J_tmp[i+1]-J_tmp[i-1])/(E_tmp[i+1]-E_tmp[i-1]))
            trajectory.omega[index[-1]] = ((J_tmp[-1]-J_tmp[-2])/(E_tmp[-1]-E_tmp[-2]))


## The solutions $x(t),p(t)$ 

The solution of the 1D-Hamiltonian system can be expressed in two ways. The first employes the constant of motion to reduce the system of differential equation to a single equation:
$$
 \dot{x}(x) =\frac{ \partial H}{\partial p} = p = \sqrt{2E - 2V_\text{eff}(x)}
$$
from this solution a quadrature procedure is possible:
$$
t(x) = \int_{x_1}^x \frac{dx}{\dot{x}(x)}
$$
in this case, the solution is given by an integration of a term that diverges at the inversion points $x_1$, $x_2$. The second case do not reduce the system of differential equation but solves it directily. The integration for this second case has to be chosen carefully to conserve the energy of the orbit.
$$
\dot{x} = p \\
\dot{p} = - \frac{V_\text{eff}(x)}{\partial x}
$$

### Numerical methods  

Different numerical methods are tested and available in this code:
1. A polynomial fit to ${\dot{x}}^{-1}$, and a subsequent analytical integration to find $t(x)$. The polynomial fit is done with a Gaussian fit. Euristicly, the power of the polynomial should be kept at rather high valutes, $p\sim 10$, to ensure that the 

2. A direct trapezoidal integration of ${\dot{x}}^{-1}$ to find $t(x)$.
3. A the leap frog method to the Hamilton equations of motion.

*The fourth approach would fit the potential to a polynomial, and then integrate using Elliptic functions.*

### The result of the evolution

1. the numerical quadrature employ the change of variable $q(u)$ to improve the integrand divergence. The integrand thus become $\frac{sin(u)}{\dot{x}(u)}$.
The discretized orbit is then $(t_i, u_i)$. The values of the dynamic variables are computed as $q_i=q(ui)$ and $p_i=\text{sign}(\sin({u_i)})\dot{x}(u_i)$
2. the leapfrog method do not change the variable to $u$, and the result of the integration is the triple $(ti,qi,pi)$.

The pseudocode is:

    #Change of Variable
    ui = linspace(1, 2pi, Nu)
    qi = q(ui, traj[x1], traj[x2])
    abspi = p(ui, traj[E])
    dt = (x1-x2)/2*sin(ui)/abspi
    % Simpson quadrature (tuning parameter Nu)
        ti = integrate(dt, ui) 
    % Polynomial interpolation (tuning paramter d)
        poly = interpolation(ui,dt, d=10)
        t = poly.integ()
        ti = t(ui) - t(0)
    step = 100
    dt = 0.001
    intial = [x1, p(x1, E)]
    % LF method
        qi, pi = evolveLF(initial, dt, step)

In the Class Ham, the numerical methods are implemented as a method of the class, which act as a interface between the system and the numerical methods

    def evolve(self, index, method):
        index = np.array(index)
        list = []
        if method == 'LF':
            for i in index:
                ti, qi, pi = evolve.LF(self, i)
                list.append([ti, qi, pi])
        elif method == 'SQ':
            for i in index:
                ti, ui = evolve.SQ(self, i)
                list.append([ti, ui])
        elif methof == 'PI':
            for i in index:
                ti, ui = evolve.PI(self, i)
                list.append([ti, ui])
        else:
            print('chose method between LF-SQ-PI \n - LF : Leap Frog method (ti,qi,pi), parameter: dt \n - SQ : Simpson Quadrature (ti, ui), parameter Nu \n PI : Polynomial Interpolate _and integration_ (ti, ui), parameter Nu') 
            break
        
        return list

A new class is introduce where the specific implementation of each method is defined, with their own parameters

    Class Push
    def __init__(self)
        self.Nu = 100
        self.dt = 0.1
        self.step = 100

    def LF(self, system, i)
        intial = [system.traj.x1[i], p(system.traj.x1[i], system.traj.E[i])]
        qi, pi = evolveLF(initial, self.dt, self.step)
        ti = np.arange(0,self.step)*self.dt
        return ti, qi, pi

    def SQ(self, system, i)
        ui = linspace(1, 2pi, self.Nu)
        qi = q(ui, system.traj.x1[i], system.traj.x2[i])
        abspi = system.p(ui, system.traj.E[i])
        dt = (system.traj.x1[i] - system.traj.x2[i])/2*sin(ui)/abspi
        ti = simpson(dt, ui) 
        return ti, ui

    def PI(self, system, i)
        ui = linspace(1, 2pi, self.Nu)
        qi = q(ui, system.traj.x1[i], system.traj.x2[i])
        abspi = system.p(ui, system.traj.E[i])
        dt = (system.traj.x1[i] - system.traj.x2[i])/2*sin(ui)/abspi
        poly = interpolation(ui,dt, d=10)
        t = poly.integ()
        ti = t(ui) - t(0)
        return ti, ui


## Validation against cyclotron motion

## implementation of pyHamSys package

# Magnetic configuration for fusion
The magnetic configuration is a twisted mangetic field, with axial and azimuthal components. This configuration is related to a selfconsitent current $j_z$ variable along-z. The derivation of this self-consistent configuration is addressed in detail in the work of X. Leoncini et al. Here, the interest is towards the study of single particle motion in this special configuration.

## q-profile
The peculiarity of this magnetic configuration can be seen already from q-profile. It display two radial values at which there is no azimuthal component: there the rotation of the magnetic field is inverted.


## Vector Potential
The cylindrical symmetry impose a null potential along the radial direction $A_r=0$. The azimuthal componet is resposible for the generation of the magnetic field along the cylindrical z-axis, while the z-component is responsible for the generation of the azimuthal magnetic field. 


# The 3D-trajectory

## The numerical method to find $\theta(t), z(t)$ from $r(t)$

The numerical method solves the following equations:
$$
\begin{align}
\theta(t) = \omega t - \int_0^t \frac{p_\theta}{r^2(t')}\,dt' \\
z(t) = p_z(t) - \int_0^t A_z(r(t'))\, dt'
\end{align}
$$
The solution is obtained with a numerical quadrature approach

### Magnetic moment
the conservation of magnetic moment will be investigated. The results from cyclotron case and in presence of separatrix will be explored. We expect that closer to the separatrix the magnetic moments fluctuates heavly.
A proper way to compute the magnetic moment has to be emploied.

The relation with the frequency $\omega= \partial_E J$ is explored


## Analysis of transport and moments of the distribution


### Prompt losses in a cylinder
In this case, we investigate the phase space given by (E, radial position, and pitch angle). This will be done by slicing at differnt values of E. The results, then will be interpreted under the light of the analysis from the occurrence of a separatrix.

The prompt losses in cyclotron motion and in the presence of a separatrix will be investigated.

#### the approach
1. measure the $r_{max}$ of a trajectory in 3D
2. given the COM $p_z, p_\theta, E$, build the function
$$

F(\text{COM})= 
\begin{cases}
0 & \text{ if } \; r_{max}>1 \\
1 &\text{ if } \; r_{max}\leq 1
\end{cases}
$$
3. change the variables to pitch angle, parallel velocity and energy.
4. test in maxweillan: integrate the losses on the energy with maxwellian distribution, in order to find the energy losses:
$$
E_{loss} = \int E\; F(COM) \, f_M(E,T)\,dE
$$
First with constant temperature, then with spatially varying temperature.
Other solution with respect of the distribution in energy (how populated are the trajectories) can be tested, with some reference, that differs from the simplistic approach of $f_M(E,T)$

### why this works?
The Problem is again here. How can the information about the orbit of the kind $(r_0, \theta_0=0,z=0, E, p_\theta, p_z)$ be enought for all the orbits $(r_0, \theta_0, z_0, E, p_\theta, p_z)$ ?

There should be a map 'very simple' for $r, \theta, z,  t$ that connects these function with initial condition $(\theta_0,z_0)$ to those that have initial condition $(\theta_0=0,z_0=0)$. 

$$
\Phi_{t}(\theta_0, z_0) = f(\Phi_{t}(\theta_0=0, z_0=0))
$$
How to compute this? it is better to check how the solution $r(t)$ changes. The differential equation is

$$
\dot{r} = \sqrt{2E-V_\text{eff}(r, p_\theta, p_z)} 
$$
with initial condition $(t_0=0, r_0)$. Thus the function $f$ behave like an identity in the radial component. The solution of $\theta(t)$?

$$
\dot{\theta} = \frac{p_\theta}{r^2} - \frac{B_0}{2}
$$

with initial condition $\theta_0=\theta^*$. Here the function $f$ has simply to add the initial condition.
$$
\theta(t; \theta_0=\theta^*) = \theta(t;\theta_0=0) + \theta^*
$$
*(the dimostration is straightforward: the two function have the same derivative, so they can differ only for a constant. By looking at t=0, the constant is found)*

Finally, the solution for $z(t)$ again differs only for a constant
$$
z(t; z_0=z^*) = z(t; z_0=0) + z^*
$$

### how does the loss function is not dependent on the initial value of $\theta_0, z_0$?

The loss function is defined as $1$ if $r_\text{max}$ is outside the minor radius. Thus, it depends on $r_\text{max} = \max{r(t)}$, which again depends on the constant of motions $p_\theta, p_z, E$ and on the initial radial condition $r_0$.

Now, even if we look in the initial-velocty space $v_{r,0}, v_{\theta,0}, v_{z,0}$, there is no dependeces on the variable $\theta_0, z_0$.
$$
v_{r,0} = \frac{p_{r,0}}{m} = \frac{\sqrt{2E-V_\text{eff}(r_0, p_\theta, p_z)}}{m}\\
v_{\theta, 0} = \frac{p_\theta r_0}{m} - \frac{qB_0}{m}r_0\\
v_{z,0} =  \frac{p_z}{m} -\frac{qB_0}{m}J(r_0)
$$

Therefore, at a given position, $(r_0, \theta_0, z_0)$, the loss function in the velocity 


