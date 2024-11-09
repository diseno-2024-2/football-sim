import sys
from typing import List

from shapely.geometry import Polygon

# Suponiendo que Player está definido en otro lugar
# from player import Player 

class Sites():
    def __init__(self,fieldWidht,fieldHeight):
        self.field_site = Polygon([(0,0),(fieldWidht,0),(fieldWidht,fieldHeight),(0,fieldHeight)])

class Field():
    """ Class responsible for the simulation of the football match"""

    def __init__(self):
        self.height = 70  # Altura promedio de un campo de fútbol en metros
        self.width = 105  # Ancho promedio de un campo de fútbol en metros
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.sites = Sites(self.width,self.height)

        
        
    
    def plot_center_line(self):
        pass

    def plot_out_lines(self):
        pass

    def plot_goallines_touchlines(self):
        pass

    def plot(self):
       pass
       
   



