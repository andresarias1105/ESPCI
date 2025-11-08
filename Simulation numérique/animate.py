import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import EllipseCollection, LineCollection
import numpy as np

from simul import Simul


class Animate:
    def __init__(self, simul):
        self.simul = simul
        self.fig, (self.ax,self.ax2) = plt.subplots(1,2,figsize=(10, 8))  # initialise  graphics
        self.circles = EllipseCollection(widths=2*simul.sigma, heights=2*simul.sigma, angles=0, units='x',
                                         offsets=simul.position, transOffset=self.ax.transData)  # circles at position
        self.ax.add_collection(self.circles)

        self.segment = [[[0, 0], [0, simul.L], [simul.L, simul.L], [simul.L, 0], [0, 0]]]  # simulation cell
        self.line = LineCollection(self.segment, colors='#000000')  # draw square
        self.ax.add_collection(self.line)

        self.ax.set_xlim(left=-0.5, right=self.simul.L+0.5)  # plotting limits on screen
        self.ax.set_ylim(bottom=-0.5, top=self.simul.L+0.5)
        self.N = self.simul.position.shape[0]
        self.traj_lines = []
        self.traj_X = []
        self.traj_Y = []
        for i in range(self.N):
            ln, = self.ax.plot([], [], lw=1.25, alpha=0.9)   # color auto
            self.traj_lines.append(ln)
            self.traj_X.append([self.simul.position[i,0]])
            self.traj_Y.append([self.simul.position[i,1]])

        self._ani = 0
        self.historyX = np.array([self.simul.position[0,0]])
        self.historyY = np.array([self.simul.position[0,1]])
        self.historyDistance = np.array(getattr(self.simul, "distance", 0.0))
        self.historyDistanceVec=np.array(getattr(self.simul,"distance_vec",0.0))

    def init(self):  # this is the first thing drawn to the screen
        self.circles.set_offsets(np.array([self.simul.position[0],self.simul.position[3]]))
        self.circles.set_widths(np.array([2*self.simul.sigma[0],2*self.simul.sigma[3]]))
        self.circles.set_heights(np.array([2*self.simul.sigma[0],2*self.simul.sigma[3]]))
        
        return self.traj_lines + [self.circles]
        

    def anim_step(self, m):
        # ¡No limpies self.ax! (si lo limpias, borrarás la trayectoria)
        self.ax2.clear()  # este sí lo puedes limpiar si quieres el gráfico de abajo

        if m == 0:
            time.sleep(1)

        self.simul.md_step()  # integra un paso

        # Actualiza posiciones de partículas
        self.circles.set_offsets(np.array([self.simul.position[0],self.simul.position[3]]))

        # === Actualiza trayectorias ===
        for i in (0,3):
            self.traj_X[i].append(self.simul.position[i,0])
            self.traj_Y[i].append(self.simul.position[i,1])
            # Si quieres limitar el largo de la estela:
            MAXPTS = 250
            if len(self.traj_X[i]) > MAXPTS:
                self.traj_X[i] = self.traj_X[i][-MAXPTS:]
                self.traj_Y[i] = self.traj_Y[i][-MAXPTS:]
            self.traj_lines[i].set_data(self.traj_X[i], self.traj_Y[i])

        # (tu gráfico secundario)
        if hasattr(self.simul, "distance"):
            self.historyDistance = np.append(self.historyDistance, self.simul.distance)
            self.ax2.plot(self.historyDistance, c="b")
            self.ax2.set_xlabel("Temps")
            self.ax2.set_ylabel("Distance")
            self.ax2.grid()
            self.ax2.set_title("Module carré de la distance entre particules")
            plt.tight_layout()

            

        return self.traj_lines + [self.circles]
        


         # update positions on screen

    def go(self, nframes):
        self._ani = animation.FuncAnimation(self.fig, func=self.anim_step, frames=nframes,
                                            repeat=False, interval=10, init_func=self.init)  # run animation
        
       
        writer = animation.PillowWriter(fps=15,
                                         metadata=dict(artist='Me'),
                                         bitrate=1800)
        self._ani.save('stade.gif', writer=writer)
        plt.show()
        


    






