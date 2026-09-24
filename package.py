import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Utility functions
# - root findings
# - orderd alphabethic labeling
# - coordinate transform u->q
# - integration method (simpson)

def Newton_root(f, q_0, tol, max_iter):
    q = q_0
    for i in range(max_iter):
        f_q = f(q)
        f_prime_q = (f(q + tol) - f(q - tol)) / (2*tol)  # Numerical derivative
        if abs(f_prime_q) < tol:
            # if the derivative is small, we are close to a stationary point
            # Let's find the max/min and see if it is a root (or close enought to it)
            f_prime = lambda q: (f(q + tol) - f(q - tol)) / (2*tol)
            q_new = Newton_root(f_prime, q, tol=tol, max_iter=max_iter)
            if abs(q_new - q) < tol:
                if abs(f(q_new)) < tol:
                    return q_new
                else:
                    return None
        q_new = q - f_q / f_prime_q
        if abs(q_new - q) < tol:
            return q_new
        q = q_new
    raise ValueError("Newton's method did not converge within the maximum number of iterations.")

def root_guess(f, qmin, qmax, Nq):
    # sample [qmin, qmax] in many points
    # if |f(xi)|<|f(x{i-1})|, |f(x{i+1})|, xi is a good guess
    # Return: np.array of dim n (number of roots)
    qj = np.linspace(qmin, qmax, Nq)
    fj = f(qj)
    root=[]
    i=0
    for i in range(1, Nq-1):
        if np.abs(fj[i])<np.abs(fj[i-1]) and np.abs(fj[i])<np.abs(fj[i+1]):
            root.append(qj[i])
    return np.array(root)

def alphabeth(j):
    word = ''
    letters = np.array(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], dtype='<U1')
    while j > 0:
        u = np.mod(j-1, 26) 
        word =  letters[u] + word
        j = int((j-u)/26)
    return word

def q_u(u, q0, q1):
    return q0/2*(1+np.cos(u)) + q1/2*(1-np.cos(u))

def u_q(q, q0, q1):
    return np.arccos((q0+q1-2*q)/(q1-q0))

def simpson(y, dx):
    integral = dx/3*(y[0] + y[len(y)-1])
    for i in range(1, int((len(y)-1)/2)):
        integral = integral + 4*dx/3* y[2*i - 1]
    for i in range(1, int((len(y)-1)/2-1)):
        integral = integral + 2*dx/3*y[2*i]
    return integral

# Class Ham(iltonian system)

class Ham:
  def __init__(self, V, E, x):
    ''' V: the potential function \\
     E: energy levels \\
     x: position grid \\
     trajec: list of trajectories \\
     reg: list of regions to solve the energy degeneracy \\'''

    self.V = V
    self.E = E
    self.x = x
    self.xmin = np.min(x)
    self.xmax = np.max(x)
    self.equi_point = {'x': [], 'V': [], 'kind': []}

    # first guess roots parameters
    self.Nq_root=len(x)

    # root finding parameters
    self.tol=1e-6
    self.max_iter=100

    # integral in phase space
    self.Nu = 1001

    # add a pusher class (allowes different methods of integration for Hamiltonian system)
    self.pusher = Push()

  def p(self,qi,Ei):
    return np.real(np.sqrt(2*Ei - 2*self.V(qi), dtype=complex))

  def add_pdot(self, pdot):
    self.pdot = pdot

  def turns(self):
    self.root = []
    for i in range(0, len(self.E)):
      f = lambda q: 2*self.E[i] - 2*self.V(q)
      self.root.append(root_guess(f, self.xmin, self.xmax, self.Nq_root))
      # find the root with newton
      for j in range(0, len(self.root[i])):
        self.root[i][j]  = Newton_root(f, self.root[i][j], self.tol, self.max_iter)
      # Remove the root if it is not valid
      self.root[i] =  self.root[i][~np.isnan(self.root[i])] 

  def equilibrium(self):
    # find the roots for each energy values
    f = lambda q: (self.V(q+self.tol) - self.V(q-self.tol))/(2*self.tol)
    self.equi_point['x'] = np.array(root_guess(f, self.xmin, self.xmax, self.Nq_root))
    # find the root with newton
    for j in range(len(self.equi_point['x'])):
      self.equi_point['x'][j]  = Newton_root(f, self.equi_point['x'][j], self.tol, self.max_iter)
    self.equi_point['x'] =  self.equi_point['x'][~np.isnan(self.equi_point['x'])]  # Remove the root if it is not valid

    self.equi_point['V'] = np.array([self.V(xi) for xi in self.equi_point['x']])
  
    self.equi_point['kind'] = []
    for xi in self.equi_point['x']:
      if self.V(xi) > self.V(xi-2*self.tol):
        self.equi_point['kind'].append('max')
      elif self.V(xi) < self.V(xi-2*self.tol):
        self.equi_point['kind'].append('min')
      else:
        raise ValueError("The point is neither a maximum nor a minimum.")
    self.equi_point['kind'] = np.array(self.equi_point['kind'])
    
  def get_regions(self):
    self.reg = Regions(self)
    self.reg.add_boundaries(self)
    while self.reg.points['x'].size > 2:
      self.reg.find_region()
    self.reg.deletepoint(1)
    self.reg.deletepoint(0)

  def get_trajectories(self):
    self.trajec = Trajectories()
    self.trajec.fill(self)
    self.trajec.getlabel(self.reg)

  def get_actionfreq(self):
    self.trajec.computeJ(self)
    self.trajec.computeomega(self)
  
  def evol_traj(self, i, method):
    if method == 'LF':
      return self.pusher.LF(self,i)
    elif method == 'SQ':
      return self.pusher.SQ(self,i)
    elif method == 'PI':
      return self.pusher.PI(self,i)
    else:
      print('the method selected is not available. Chose between:\n - \'LF\' : Leap Frog $t,u,v$ \n - \'SQ\' : Simpson Quadrature (trapezoidal now) $t,u$ \n - \'PI\' : Polynomial integration $t,u$')

# Class (separatrix) Regions

class Regions:
  def __init__(self, ham):
    self.label = []
    self.Emin = []
    self.Emax = []
    self.xmin = []
    self.xmax = []
    self.points = {'x': [], 'V': [], 'kind': []}
    self.points['x'] = ham.equi_point['x']
    self.points['V'] = ham.equi_point['V']
    self.points['kind'] = ham.equi_point['kind']
    #self.points = self.add_boundaries(ham)
    # del self.points

  def add_boundaries(self, ham):
    self.points['x'] = np.concatenate([[ham.xmin], self.points['x'], [ham.xmax]])
    self.points['V'] = np.concatenate([[ham.V(ham.xmin)], self.points['V'], [ham.V(ham.xmax)]])
    self.points['kind'] = np.concatenate([['boundary'], self.points['kind'], ['boundary']])

  def find_region(self):
    # build the regions in phase-space starting from the lowest energy. If neighborh points have the same energy, they lie on the same separatrix, thus we have only one region. 
    # The method discard the first point and work with the other. After the region has been built, then the point is discarded
    j = len(self.label) + 1
    i = np.argmin(self.points['V'])
    if self.points['V'][i] == self.points['V'][i+1] or self.points['V'][i] == self.points['V'][i-1]:
      self.deletepoint(i)
    else:
      self.label.append(alphabeth(j))
      Emax, Emin = self.energy_range(i)
      self.Emax.append(Emax)
      self.Emin.append(Emin)
      xmax, xmin = self.position_range(i)
      self.xmax.append(xmax)
      self.xmin.append(xmin)
      self.deletepoint(i)

  def position_range(self, i):
    # at the lowest energy unexplored the position range is limited by the neighbors!
    xmin = self.points['x'][i-1]
    xmax = self.points['x'][i+1]
    return xmax, xmin
        
  def energy_range(self, i):
    # at the lowest energy explored, the energy is bounded by the lowest energy (the one of the point) and the lowest energy between the neigbohrs.
    Emin = self.points['V'][i]
    Emax = min(self.points['V'][i+1], self.points['V'][i-1])
    return Emax, Emin

  def deletepoint(self, i):
    for key, value in self.points.items():
      self.points[key] = np.delete(value, i)

  def df(self):
    return  pd.DataFrame( {key: self.__dict__[key] for key in ['xmin','xmax','Emin','Emax']} , index=self.label )

# Class Trajectories (with energy degeneracy)
#   this is the juice

class Trajectories:
  def __init__(self):
    self.index = np.array([], dtype=int)
    self.E = np.array([])
    self.x1 = np.array([])
    self.x2 = np.array([])
    self.label = np.array([])

  def fill(self, ham):
    k = 0 # index of the trajectory
    for i, qs in enumerate(ham.root):
      # i is the index of energy level
      for j, qi in enumerate(qs[:-1]):
        # j is the index of root at energy level Ei
        if ham.V(qi+ham.tol) < ham.E[i]:
            self.index = np.concatenate([self.index, [int(k)]], dtype=int)
            self.E = np.concatenate([self.E, [ham.E[i]] ])
            self.x1 = np.concatenate([self.x1, [qs[j]] ])
            self.x2 = np.concatenate([self.x2, [qs[j+1]] ])
            k += 1

  def getlabel(self, regions):
    for i in self.index:
      maskx1 = regions.xmin < self.x1[i]
      maskx2 = regions.xmax > self.x2[i]
      maskEmin = regions.Emin < self.E[i]
      maskEmax  = regions.Emax > self.E[i]
      mask = maskx1 & maskx2 & maskEmin & maskEmax
      self.label = np.concatenate([ self.label, np.array(regions.label)[mask] ])

  def computeJ(self, ham):
    self.J = np.array([])
    for i in self.index:
      self.J = np.concatenate([self.J, [self.Ji(ham,i) ]])

  def Ji(self, ham, i):
    uj = np.linspace(0, np.pi, ham.Nu)
    du = uj[1]-uj[0]
    qj = q_u(uj,self.x1[i],self.x2[i])
    pj = ham.p(qj, self.E[i])
    integrand_J = np.sin(uj)*pj
    return 1/np.pi*(self.x2[i]-self.x1[i])/2*simpson(integrand_J,du)

  def computeomega(self, ham):
    self.omega = np.zeros_like(self.J)
    for letter in ham.reg.label:
      mask = self.label == letter
      ind = self.index[mask]
      if len(ind) < 2: break

      self.omega[ind] = self.omega_letter(mask)

  def omega_letter(self,mask):
    om = []
    E = self.E[mask]
    J = self.J[mask]
    for i in range(len(E)):
      if i == 0:
        om.append( (E[1]-E[0])/(J[1]-J[0]) )
      elif i == len(E)-1:
        om.append( (E[-1]-E[-2])/(J[-1]-J[-2]) )
      else:
        om.append( (E[i+1]-E[i-1])/(J[i+1]-J[i-1]) )
    return np.array(om)

  def df(self):
      return  pd.DataFrame( {key: self.__dict__[key] for key in ['x1','x2','E','label', 'J', 'omega']} , index=self.index )

# Class Pushers :: method to evolve the trajectory in time

class Push:
    def __init__(self):
        self.Nu = 100
        self.dt = 0.01
        self.step = 1000
        self.degree = 10

    def LF(self, system, i):
        x = [system.trajec.x1[i]]
        v = [system.p(system.trajec.x1[i], system.trajec.E[i])]
        if hasattr(system, 'pdot'):
            pdot = system.pdot
        else:
            pdot = lambda q: (system.V(q-system.tol) - system.V(q+system.tol))/(2*system.tol)
        for j in range(self.step):
            v_half = v[-1] + pdot(x[-1])*self.dt*0.5
            x_new = x[-1] + v_half*self.dt
            v_new = v_half + pdot(x_new)*self.dt*0.5
            x.append(x_new)
            v.append(v_new)        
        t = np.arange(0,self.step+1)*self.dt
        return t, x, v

    def SQ(self, system, i):
        ui = np.linspace(1, 2*np.pi, self.Nu)
        qi = q_u(ui, system.trajec.x1[i], system.trajec.x2[i])
        abspi = system.p(qi, system.trajec.E[i])
        dt = (system.trajec.x2[i] - system.trajec.x1[i])/2*np.abs(np.sin(ui))/abspi
        dt[0] = dt[1]
        dt[-1] = dt[-2]
        trapez =  0.5*(dt[1]+dt[0])*(ui[1]-ui[0])
        ti = [ trapez ]
        for i in range(1,len(ui)-1):
            trapez = 0.5*(dt[i+1] + dt[i])*(ui[i+1]-ui[i])
            ti.append(ti[-1] + trapez)    
        ti = np.array(ti)
        ui = 0.5*(ui[1:] + ui[:-1])
        return ti, ui

    def PI(self, system, i):
        ui = np.linspace(1, 2*np.pi, self.Nu)
        qi = q_u(ui, system.trajec.x1[i], system.trajec.x2[i])
        abspi = system.p(qi, system.trajec.E[i])
        dt = (system.trajec.x2[i] - system.trajec.x1[i])/2*np.abs(np.sin(ui))/abspi
        dt[0] = dt[1]
        dt[-1] = dt[-2]
        poly = np.polynomial.polynomial.Polynomial.fit(ui, dt, self.degree)
        t = poly.integ(k=0)
        ti = t(ui) - t(0)
        return ti, ui