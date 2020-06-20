"""
This file contains everything regarding the visualization and the server which
runs the model.
"""
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from .model import Anthill
from .agent import Ant, Brood,Fence

# IMPORTANT: the WIDTH and HEIGHT parameters are also in model.py; make sure
# to change those as well if you want to adjust the grid size
WIDTH = 25
HEIGHT = 25

def agent_portrayal(agent):
    if type(agent) is Brood:
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "black",
                     "r": 0.2}

    ## use this portrayal for ant visuals
    if type(agent) is Ant:
        portrayal = {"Shape":"ant.jpg", "Layer":0}
    if type(agent) is Fence:
        portrayal = {"Shape":"Fence.jpg", "Layer":0}

    return portrayal

chart0 = ChartModule([{"Label": "Total number of Ants",
                      "Color": "green"}],
                    data_collector_name='datacollector')

chart1 = ChartModule([{"Label": "mean tau",
                      "Color": "green"}],
                    data_collector_name='datacollector')

chart2 = ChartModule([{"Label": "sigma",
                      "Color": "green"}],
                    data_collector_name='datacollector')

chart3 = ChartModule([{"Label": "sigma*",
                      "Color": "green"}],
                    data_collector_name='datacollector')

grid = CanvasGrid(agent_portrayal, WIDTH, HEIGHT)
server = ModularServer(Anthill,
                       [grid,chart0,chart1,chart2,chart3],
                       "Anthill")
server.port = 8521 # The default
