import sys
from typing import List

from shapely.geometry import Polygon
from classes.ball import Ball


# Suponiendo que Player está definido en otro lugar
# from player import Player 

class Sites():
    def __init__(self,fieldWidht,fieldHeight,center_x,center_y):
        altura_areagrande = 40.32
        largo_areagrande = 16.5
        altura_areapequenia = 9.16
        largo_areapequenia = 5.5
        self.field_site = Polygon([(0,0),(fieldWidht,0),(fieldWidht,fieldHeight),(0,fieldHeight)])
        self.area_grande_izquierda = Polygon([(0,center_y-(altura_areagrande/2)),(largo_areagrande,center_y-(altura_areagrande/2)),(largo_areagrande,center_y+(altura_areagrande/2)),(0,center_y+(altura_areagrande/2))])
        self.area_pequenia_izquierda = Polygon([(0,center_y-(altura_areapequenia)),(largo_areapequenia,center_y-(altura_areapequenia)),(largo_areapequenia,center_y+(altura_areapequenia)),(0,center_y+(altura_areapequenia))])
        
        self.area_grande_derecha = Polygon([(fieldWidht,center_y-(altura_areagrande/2)),(fieldWidht - largo_areagrande,center_y-(altura_areagrande/2)),(fieldWidht - largo_areagrande,center_y+(altura_areagrande/2)),(fieldWidht,center_y+(altura_areagrande/2))])
        self.area_pequenia_derecha = Polygon([(fieldWidht,center_y-(altura_areapequenia)),(fieldWidht - largo_areapequenia,center_y-(altura_areapequenia)),(fieldWidht - largo_areapequenia,center_y+(altura_areapequenia)),(fieldWidht,center_y+(altura_areapequenia))])

        self.mediocampo_izquierda = Polygon([(0,0),(fieldWidht/2,0),(fieldWidht/2,fieldHeight),(0,fieldHeight)])
        self.mediocampo_derecha = Polygon([(fieldWidht,0),(fieldWidht/2,0),(fieldWidht/2,fieldHeight),(fieldWidht,fieldHeight)])

class Field():
    """ Class responsible for the simulation of the football match"""

    def __init__(self):
        self.height = 70  # Altura promedio de un campo de fútbol en metros
        self.width = 105  # Ancho promedio de un campo de fútbol en metros
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.sites = Sites(self.width,self.height,self.center_x,self.center_y)
        self.ball: Ball = None

        self.equipo_con_balon = -1

        
        
    
    def plot_center_line(self):
        pass

    def plot_out_lines(self):
        pass

    def plot_goallines_touchlines(self):
        pass

    def plot(self):
       pass
       
   



