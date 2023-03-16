#import packages
import mesa_geo as mg
import random
from shapely.geometry import Point


#import model
from model import *

#set up class for shells
class Shell(mg.GeoAgent):

    """Shell Agent"""

    def __init__(self, unique_id, model, geometry, crs):
        super().__init__(unique_id, model, geometry, crs)
        self.type = "Shell"
        
    def step(self):
        pass

#set up class for oyster agent
class Oyster(mg.GeoAgent):
    
    """Oyster Agent"""
   
    #define init values
    def __init__(self, unique_id, model, geometry, crs):
         super().__init__(unique_id, model, geometry, crs)
         self.type = "Oyster"

    #define what happens at each step      
    def step(self):

        #set status to alive
        self.status = "alive"
        
        #if conditions met, kill off
        if (random.random() < 0.002):
            self.status = "dead"
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
            

            #convert dead oysters to shells
            new_shell = Shell(
                unique_id = "shell_" + str(self.unique_id).replace("oyster_", ""),
                model = self.model,
                geometry = self.geometry, 
                crs = self.model.space.crs,
                )

            #add shell agents to grid and scheduler
            self.model.space.add_agents(new_shell)
            self.model.schedule.add(new_shell)

        #establish reproductive days
        reproductive_days = list(range(203, 210)) + list(range(212, 215))
        
        #reproduction
        if (self.status == "alive") and any(self.model.step_count%i == 0 for i in reproductive_days):

            #create new oysters
            for i in range(3):
                #get random reef
                random_reef =  self.random.randint(
                0, len(self.model.reef_agents) - 1
                )
                
                #create oyster
                baby_oyster = Oyster(
                    unique_id = "oyster_" + str(self.model.next_id()),
                    model = self.model,
                    geometry = self.model.point_in_reef(random_reef), 
                    crs = self.model.space.crs
                )
            
                #add oyster agents to grid and scheduler
                self.model.space.add_oyster(baby_oyster)
                self.model.space.add_agents(baby_oyster)
                self.model.schedule.add(baby_oyster)


#set up class for ReefAgent
class Reef(mg.GeoAgent):

    """Reef Agent"""

    def __init__(
        self, unique_id, model, geometry, crs
    ):
        super().__init__(unique_id, model, geometry, crs)
        self.type = "Reef"

    def step(self):
        #get step count
        self.oyster_count = len(list(self.model.space.get_intersecting_agents(self)))

    #get reef identity
    def __repr__(self):
        return "Reef " + str(self.unique_id)

