<header>

# Simulatie single particle motion in a given magnetic field configuration
The code is created from scratch and aims to test a new method for solving close orbits trajectory. It solves one dimensional dynamics, 2D differential equation in the phase space, using the energy and z-momentum constants of motion to reduce the dimensionality from 3D3V to 1D1V. Furthermore, it exploits the symmetry (v,t) -> (-v,-t) of the trajectory by solving the motion in the negativ v-semiplane from the given motion in the upper plane.
The energy -- in the hypothesis of a fixed z-momentum $p_z$ -- labels the trajectory (x,v)(t) in the phase space, and then the time dependence is solve via numerical method for differential equation. Note that the relation between the energy are not bijective -- a trajectory has an unique value of energy but not vice-versa. This means that there can be some degeneracy in the energy. In this case, the cause of the degeneracy is due to the presence of a separatrix. 
</header>

## Symmetries of the problem

The magnetic field has no dependence on the variable $z, \theta$, thus it's derivative against them is equal to 0. At the same time also the Magnetic Vector is indipendet on this variables. These variable do not appear neither in the Hamiltonian $H=H(\vec{p},r)$. In cartesian coordinates the Hamiltonian is:
$$
H =0.5(\vec{p}-\vec{A})^2 = 0.5p_r^2 + 0.5(p_\theta-0.5B_0r)^2+0.5(p_z-A_z(r))^2
$$

thus for the equation of motion, we find that the respective momentum of the cyclic coordinates are constant of motion:

$$
\begin{align}
\dot{p}_\theta = - \frac{\partial H}{\partial \theta} = 0 \\
\dot{p}_z = - \frac{\partial H}{\partial z} = 0
\end{align}
$$

This means that the coordinates $p_\theta$ and $p_z$ can be seen as 'parameters' of the particle, i.e. proprietries that do not vary throught the dynamic. The evolution of the coordinate is less simple:

$$
\dot{\theta} = \frac{\partial H}{\partial p_\theta} = \frac{p_\theta}{r^2(t)}-0.5B_0
\dot{z} = \frac{\partial H}{\partial p_z} = p_z-A_z(r(t))
$$

The two coordinates are not straightfoward to integrate: it requires in general numerical integration. But it also requires the knowledge of $r(t)$.

## The reduced to 1D hamiltonian system

The equation of motion for $r$ is decoupled from the others, and in particular, it is fundamental for the integration of the other coordinates. It can derived from the previous Hamiltonian. In particular, since $r$ is decoupled, we can think the system as a 1D-Hamiltonian systen. This allows to study qualitativly the phase space, and to procede in a more straigthforward way. The Hamiltonian is the same, but the part with the angular and azial momentums becomes the effective potential:

$$ H(r, p_r) = 0.5p_r^2 + V_{eff}(r)\\
V_{eff}(r) =  0.5(p_\theta-0.5B_0r)^2+0.5(p_z-A_z(r))^2
$$
this will be the system of interest.

## Qualitative study on the 1D hamiltonian system

## Computation of the action variable and frequency
The action variable is related to the fundamental frequency of a trajectory. This method is taken from the work of Berk et Warnock. They provided a method to compute the action integral with a specific change of variable that make the convergence faster. They also point out that it is possible to compute the phase $\Phi(t)$ using an integration techniques, but it seems that it cannot reach the convergence as expected.

The method associate for each trajectory the action and the frequency. The trajctories are labeled by the energy and other indces to solve the finite degeneracy.

### Numerical method
The main numerical methods are:

- Newton root finding algorithm 
- Simpson integration method

<u>Note</u>: the root finding algorithm has been modify to handle points that are both roots and min/max points. Such points would break the standard Newton algorithm because around stationary points, the first derivative is so small than would not 'push' the point along the $x$ axis. This issue is relevant when the trajectory is at the stationary point (minimum) or close to separatrix (maximum/unstable).

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

The method to compute $J(E)$ simply rely on the assumption that there is no degeneracy in energy for the system. This can be extended to the degenerate one by considering separatly each degenerate regions.

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

The computation of $J(E_\alpha)$, which stands for the action for the trajectory with energy $E$ in the degeneracy $\alpha$, is done using a change of variable suggested in the paper of  Berk et Warnock. This is implemented in the following way. The final computation uses a standard trapezoidal method.

    # Change of Variable
    Ham.ugrid = linspace(0,2*pi, Nu)
    def x(u, x1,x2): 
        return x1/2*(1+np.cos(u)) + x2/2*(1-np.cos(u))
    
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

The computation of $\omega$ instead relies on a simple finite difference method. For the extreme points of $\[E_{min},E_{max}\], a right/left derivative is used, while for intermediate points a avarged derivative is used.

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



## The evolution $x(t),p(t)$ for a trajectory

The idea is to employ a polynomial fit to integrate using analytical equation. The polynomial fit is done with a Gaussian fit. The power of the polynomial has been left at small values, to guaratee computational speed, but not too small to do not underestimate.

The second approach would employ standard numerical techniques (finite difference).

The third approach would fit the potential to a polynomial, and then integrate using Elliptic functions.

The fourth approach is the leap frog method (the with half step or full step)

### The result of the evolution

1. the numerical quadrature employ the change of variable $q(u)$ to compute the evolution.
The evolution is then $ui, ti$. The values of the dynamic variables are then $qi=q(ui)$ and $pi=np.sign(np.sin(ui))*p(ui)$
2. the numerical method (leapforg) do not change the variable, and the result of the integration is the triple $ti,qi,pi$.

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

Which is added as method in the Class Ham

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
        Raise 'chose method between LF-SQ-PI \n - LF : Leap Frog method (ti,qi,pi), parameter: dt \n - SQ : Simpson Quadrature (ti, ui), parameter Nu \n PI : Polynomial Interpolate _and integration_ (ti, ui), parameter Nu' 
        
        return list

The method for evolution belongs to another class

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
The magnetic configuration is a twisted mangetic field, with axial and azimuthal components. These configuration is related to a selfconsitent current $j_z$ variable along-z. The derivation of this self-consistent configuration is addressed in detail in the work of X. Leoncini et al. Here, the interest is revolved towards the study of single particle motion in this special configuration.


## q-profile
The peculiarity of this magnetic configuration can be seen already from q-profile. It display two radial values at which there is no azimuthal component: there the rotation of the magnetic field is inverted!


## Vector Potential
The potential is taken from a previous work by X.Leoncini ...
The cylindrical symmetry impose a null potential along the radial direction $A_r=0$. The azimuthal componet is resposible for the generation of the magnetic field along the cylindrical z-axis, while the z-component is responsible for the generation of the azimuthal magnetic field.


# The 3D-trajectory

## The numerical method to find $\theta(t), z(t)$ from $r(t)$

The numerical method emploies a quadrature method:
$$
\begin{align}
\theta(t) = \omega t - \int_0^t \frac{p_\theta}{r^2(t')}\,dt' \\
z(t) = p_z(t) - \int_0^t A_z(r(t'))\, dt'
\end{align}
$$


## Analysis of transport and conservation


### Prompt losses in a cylinder
In this case, we investigate the section of phase space given by: E, radial position, and angle between v_perp and v. This will be done by slicing at differnt values of E. The results, then will be interpreted under the light of the analysis from the occurrence of a separatrix.

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

### Magnetic moment
the conservation of magnetic moment will be investigated. The results from cyclotron case and in presence of separatrix will be explored. We expect that closer to the separatrix the magnetic moments fluctuates heavly.
A proper way to compute the magnetic moment has to be emploied.

The relation with the frequency $\omega= \partial_E J$ is explored


