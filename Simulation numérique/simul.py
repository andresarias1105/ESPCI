import numpy as np
import math


class Simul:
    """ 
    This is the prototype of the simulation code
    It moves the particles with at _velocity, using a vector notation: numpy should be used.
    """
    def __init__(self, simul_time, sigma, L):
        np.seterr(all='ignore')  # remove errors in where statements
        self.L = L
        self.po,self.vo=np.array([[self.L/2,self.L/2],[3.,-4.]])
        self.dp,self.dv=np.random.uniform(0,self.L,(2,2))


        self.position = np.array([self.po,[self.L/2,self.L],[self.L/2,0],self.po+0.2*self.dp])  # starting positions
        self.velocity = np.array([self.vo ,[0.,0.],[0.,0.],self.vo+0.2*self.dv])# random velocities
        self.l, self.m = np.triu_indices(self.position.shape[0], k=1)  # all pairs of indices between particles
        self.sigma = np.array([sigma, self.L/2,self.L/2,sigma])  # particle radius
        self.simul_time = simul_time

        self.distance=np.sum((self.position[0]-self.position[3])*(self.position[0]-self.position[3]))
        self.distance_vec=(self.position[0]-self.position[3])
        

    def wall_time(self):
            particle,tmin=None,np.inf
            for i in (0,3):
                x = self.position[i, 0]
                vx = self.velocity[i, 0]

                if vx > 0:
                    t = (self.L - self.sigma[i] - x) / vx
                elif vx < 0:
                    t = (x - self.sigma[i]) / (-vx)
                
                if t<tmin:
                    tmin=t
                    particle=i
                
            return tmin, particle, 0  # particle 0, componente x


    
       
    def circle_inside_time(self):
    
        best_t, hit ,particle,= np.inf, None,None
        for i in (0,3): 
            r0 = self.position[i]
            v0 = self.velocity[i]
            A = np.dot(v0, v0)
            if A == 0.0:
                return np.inf, None

            for j in (1, 2):
                Cj = self.position[j]                  
                Reff = self.sigma[j] - self.sigma[i]   
                dX = r0 - Cj

                B = 2.0 * np.dot(v0, dX)
                C = np.dot(dX, dX) - Reff**2
                if not (C < 0 and B > 0):
                    continue

                disc = B*B - 4.0*A*C
                if disc < 0:
                    continue

                
                t = (-B + math.sqrt(disc)) / (2.0*A)
                if t < 0:
                    continue

                
                p = r0 + t * v0               
                cy = Cj[1]
                if j == 1 and p[1] < cy:      
                    continue
                if j == 2 and p[1] > cy:      
                    continue
                

                if t < best_t:
                    best_t, hit,particle = t, j,i

        return best_t, hit,particle

    def reflect_on_inner_circle(self, j,i):
        
        Cj = self.position[j]
        r0 = self.position[i]
        n = r0 - Cj
        n /= np.linalg.norm(n)              
        v0 = self.velocity[i]
        self.velocity[i] = v0 - 2.0 * np.dot(v0, n) * n


    def md_step(self):
        ke_start = (self.velocity**2).sum()/2.0
        t = 0.0
        eps = 1e-12

        while t < self.simul_time:
            wt, Wparticle, _ = self.wall_time()
           
            ct, cj,particle = self.circle_inside_time()

            next_t = min(wt, ct)
            remaining = self.simul_time - t
            dt = min(next_t, remaining)

            
            self.position += dt * self.velocity
            t += dt

            if next_t <= remaining + eps:
                if wt <= ct:   
                    
                    if self.velocity[Wparticle,0] > 0:
                        self.position[Wparticle,0] = self.L - self.sigma[Wparticle]
                    else:
                        self.position[Wparticle,0] = self.sigma[Wparticle]
                    
                    self.velocity[Wparticle,0] *= -1.0
                else:          
                    
                    self.reflect_on_inner_circle(cj,particle)
            else:
                break
        self.distance=np.sum((self.position[0]-self.position[3])*(self.position[0]-self.position[3]))
        self.distance_vec=(self.position[0]-self.position[3])
        return -1



            
          
        

        

        return pressure

    def __str__(self):   # this is used to print the position and velocity of the particles
        p = np.array2string(self.position)
        v = np.array2string(self.velocity)
        return 'pos= '+p+'\n'+'vel= '+v+'\n'
