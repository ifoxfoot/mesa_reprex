#import mesa package
import mesa
import mesa_geo as mg

#import model and agent
from model import *
from agents import *

#set up sliders for model parames
model_params = {
    "N": mesa.visualization.Slider("Number of Oysters", 50, 100, 250, 500)
}

#define how agents will be shown
def agent_portrayal(agent):
    if isinstance(agent, mg.GeoAgent):
        if isinstance(agent, Reef):
            return {
                "Color": "Blue",
            }
        elif isinstance(agent, Oyster):
            return {
                "stroke": False,
                "color": "Green",
                "radius": 2,
                "fillOpacity": 0.3,
            }
        elif isinstance(agent, Shell):
            return {
                "stroke": False,
                "color": "Gray",
                "radius": 2,
                "fillOpacity": 0.3,
            }
    elif isinstance(agent, ReefCell):
        return (agent.elevation, agent.elevation, agent.elevation, 1)

#create map element
map_element = mg.visualization.MapModule(agent_portrayal)

#server
server = mesa.visualization.ModularServer(
    OysterModel, [map_element], "Oyster Model", model_params = model_params
)

#launch server to port
server.launch()