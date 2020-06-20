"""
Here are all the different types of agents.
Ants: move randomly
Brood: don't do anything but exist
Fence:Boundarary
"""
from mesa import Agent
import numpy as np

# ---> This is a bit messy here, but needed to calculate bound_vals 
# for list of boundary coordinates, wasn't sure where else to put it
WIDTH = 25
HEIGHT = 25
bound_vals=[]
neigh_bound=[]


for i in range(WIDTH):
    for j in range(HEIGHT):
        if (i == 1 or i == WIDTH - 2) or (j == 1 or j == HEIGHT-2):
            neigh_bound.append((i,j))

class Ant(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)


    def force_calc(self):
        """ Calculate the force acting on the ant. """

        ##check the neighbor if it is Ant or fence

        # Calculate the force in x and y direction 

        Fx = 0

        if (type(self.model.grid[self.pos[0]-1][self.pos[1]]) is Ant or 
            type(self.model.grid[self.pos[0]-1][self.pos[1]]) is Fence):
            Fx += 1
        if (type(self.model.grid[self.pos[0]+1][self.pos[1]]) is Ant or 
            type(self.model.grid[self.pos[0]+1][self.pos[1]]) is Fence):
            Fx -= 1

        Fy = 0 
        if (type(self.model.grid[self.pos[0]][self.pos[1]-1]) is Ant or 
            type(self.model.grid[self.pos[0]][self.pos[1]-1]) is Fence):
            Fy += 1
        if (type(self.model.grid[self.pos[0]][self.pos[1]+1]) is Ant or 
            type(self.model.grid[self.pos[0]][self.pos[1]+1]) is Fence):
            Fy -= 1

        # Magnitude of the force
        F = np.sqrt(Fx**2+Fy**2)

        return Fx,Fy,F

    def stoch_move(self,c):
        """ Moves are selected stochastically """
        # First find possible trial configurations
        trials = []
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                # Skip the centre and the preferered direction c
                if (x!=0 or y !=0):
 
                    if self.model.grid.is_cell_empty((self.pos[0] + x,self.pos[1] + y)) == True:
                        trials.append((x,y))
        w = []
        beta = 5
        for i in trials:
            # The magnitude of vector difference c and c*
            d = np.sqrt((i[0] - c[0])**2 + (i[1] - c[1])**2)
            w.append(np.exp(-beta * d))
        sumw = np.sum(w)

        # Select one with probability w/sumw
        n = self.select(sumw,w)

        return trials[n]

    def select(self,sumw,w):
        """ Select one of the trial configurations,c*, with probability eq. 11. """

        ws = self.random.uniform(0,1) * sumw
        cumw = w[0]
        n = 0
        while(cumw < ws):
            n += 1
            cumw += w[n]

        return n

    def move(self):

        Fx, Fy, F = self.force_calc()

        if F != 0:
            # Calculate the new preferred direction, rounding to nearest integer
            c = (int(round(Fx / F)), int(round(Fy / F)))

            c = self.stoch_move(c) # For deterministic model comment this line out

            new_position = (self.pos[0] + c[0], self.pos[1] + c[1])

            # ant if it has moved onto the boundary and it will be removed
            if new_position in neigh_bound:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)

            ## if it is empty then move into this place
            elif self.model.grid.is_cell_empty(new_position):
                self.model.grid.move_agent(self, new_position)

            # Remove if new pos is already occupied but current pos is on boundary
            elif self.pos in neigh_bound:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)

        # Remove if F=0 and cur pos is on the boundary
        elif self.pos in neigh_bound:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


    def step(self):
        self.move()

class Brood(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)


class Fence(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)

