#import packages
import mesa
import mesa_geo as mg
from shapely.geometry import Point
import random

#import agents
from agents import *
from space import *
    
#set up class for model
class OysterModel(mesa.Model):
    
    """A model class for oysters"""

    #path to reef file and unique reef ID
    reefs = "data/oyster_reef.gpkg"
    unique_id = "OBJECTID"

    #define init parameters
    def __init__(self, N):
        self.num_oysters = N #number of oysters (int)
        self.space = SeaBed(crs = "epsg:3512")
        self.schedule = mesa.time.RandomActivation(self)
        self.step_count = 0
        self.current_id = N

        self.space.set_elevation_layer(crs = "epsg:3512")

        #create reef agents
        ac = mg.AgentCreator(
            Reef, 
            model = self
            )
        self.reef_agents = ac.from_file(
            self.reefs, unique_id = self.unique_id
            )
        
        #add reef agents to space
        self.space.add_agents(self.reef_agents)

        #create oysters
        for i in range(self.num_oysters):
            #get random reef to locate oyster
            random_reef =  self.random.randint(
                0, len(self.reef_agents) - 1
            )
        
            #create agent
            this_oyster = Oyster(
                unique_id = "oyster_" + str(i),
                model = self,
                geometry = self.point_in_reef(random_reef),
                crs =  self.space.crs
            )
            
            #add oyster agents to grid and scheduler
            self.space.add_oyster(this_oyster)
            self.space.add_agents(this_oyster)
            self.schedule.add(this_oyster)

        #add reef agents to schedule after oysters
        for agent in self.reef_agents:
            self.schedule.add(agent)

        #init data collector
        self.running = True
        
        #tell data collector what to collect
        self.datacollector = mesa.DataCollector(
            agent_reporters = {#reef metrics
                                "oyster_count": lambda a: a.oyster_count if a.type == "Reef" else None
                                },
            #get oyster lifespan                    
            tables = {"Lifespan": [lambda a: a.unique_id if a.type == "Oyster" else None, 
            lambda a: a.age if a.type == "Oyster" else None]}
            )
        
    #create function to create coordinates for new oyster
    def point_in_reef (self, random_reef):
        minx, miny, maxx, maxy = self.reef_agents[random_reef].geometry.bounds
        pnt = Point(0,0)
        while not self.reef_agents[random_reef].geometry.contains(pnt):
            pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        return pnt

    #define step
    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        self.step_count += 1
        self.space._recreate_rtree()  # Recalculate spatial tree, because agents are moving??
        self.datacollector.collect(self)
    
    #define run model function
    def run_model(self, step_count=200):
         for i in range(step_count):
            self.step()
