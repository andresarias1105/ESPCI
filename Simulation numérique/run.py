
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import EllipseCollection, LineCollection
from simul import Simul
from animate import Animate
from matplotlib.patches import Arc
import numpy as np




class BoroAnim(Animate):
    def __init__(self, simulation):
        self.simul = simulation
        self.fig, (self.ax,self.ax2) = plt.subplots(2,1,figsize=(5, 5))  # initialise  graphics
        #self.circles.remove()
        self.circles = EllipseCollection(widths=2*simulation.sigma, heights=2*simulation.sigma, angles=0, units='x',
                                         offsets=simulation.position, transOffset=self.ax.transData)  # circles at position
        self.ax.add_collection(self.circles)

        self.segment = [[[0, 0], [0, simulation.L]]]  # simulation cell
        self.line = LineCollection(self.segment, colors='#000000')  # one line
        self.ax.add_collection(self.line)
        self.segment = [[[simulation.L, 0], [simulation.L, simulation.L]]]  # simulation cell
        self.line = LineCollection(self.segment, colors='#000000')  # second line
        self.ax.add_collection(self.line)

        self.arc= Arc ( xy=(self.simul.L/2,self.simul.L) , width=self.simul.L,height=self.simul.L, angle=0, theta1=0, theta2=180 )
        self.ax.add_patch(self.arc)
        self.arc= Arc ( xy=(self.simul.L/2,0) , width=self.simul.L,height=self.simul.L, angle=0, theta1=180, theta2=360 )
        self.ax.add_patch(self.arc)

        
        self.ax.set_xlim(left=-self.simul.L/2, right=self.simul.L+0.5)  # plotting limits on screen
        self.ax.set_ylim(bottom=-self.simul.L/2, top=3*self.simul.L/2+0.5)
        self.ax.set_aspect('equal') 
        self._ani = 0
        self.historyX=np.array(self.simul.position[0][0])
        self.historyY=np.array(self.simul.position[0][1])
        self.distance=[]
        self.distance_vec=[]
        self.historyDistance=[]
        self.historyDistanceVec=[]
        self.N = self.simul.position.shape[0]
        self.traj_lines = []
        self.traj_X = []
        self.traj_Y = []
        for i in range(self.N):
            ln, = self.ax.plot([], [], lw=1.25, alpha=0.9)
            self.traj_lines.append(ln)
            self.traj_X.append([self.simul.position[i,0]])
            self.traj_Y.append([self.simul.position[i,1]])
            
        

def main():
        
        
        np.random.seed(1)  # set random numbers to be always the same
        simulation = Simul(simul_time=0.05, sigma=0.3, L=5 )  # sigma particle radius # L box size
        print(simulation.__doc__)  # print the documentation from the class

        animate = BoroAnim(simulation)
        
        animate.go(nframes=500)  # number of animation steps
        print(simulation)  # print last configuration to screen


if __name__ == '__main__':
    main()


def run_sim(simul_time=0.05, steps=500, **kwargs):
    sim = Simul(simul_time=simul_time, **kwargs)
    dist_hist = []
    dist_vec_hist=[]
    for _ in range(steps):
        sim.md_step()
        # asumo que sim.distance se actualiza en md_step
        dist_hist.append(sim.distance)
        dist_vec_hist.append(sim.distance_vec[0])
    return np.array(dist_hist),sim.vo[0],sim.po[0],dist_vec_hist


N = 100
all_dists = []
all_len=[]
all_Vx=[]
all_disX=[]
for i in range(N):
    np.random.seed(i+1)
    d,v,x ,dv= run_sim(simul_time=0.05, steps=600, sigma=0.3, L=5)
    all_dists.append(d)
    all_len.append(np.sum(d))
    all_Vx.append(v)
    all_disX.append(dv)



fig, (ax,ax2) = plt.subplots(2,1,figsize=(10, 10))
for i, d in enumerate(all_dists, start=1):
    ax.plot(d, label=f"Sim {i}",c="b")
    ax2.plot(all_disX[i-1],c="r")  
ax.set_xlabel("Temps")
ax.set_ylabel("Distance")


ax2.set_xlabel("Temps")
ax2.set_ylabel("Distance")

ax.grid()
ax2.grid()


fig.suptitle("Métriques d'écart pour N={} positions aléatoires".format(N))

ax.set_title("a) Module carré de la distance entre particules")
ax2.set_title("b) Abcisse du vecteur distance entre particules")

#plt.legend()



plt.tight_layout()
plt.savefig("L4d0,2.pdf", format="pdf", bbox_inches="tight")
plt.show()

