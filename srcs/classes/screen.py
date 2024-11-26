import pygame
import numpy as np
from classes.player import Player
from classes.ball import Ball
from classes.field import Field
from typing import List
import random

class Screen:
    """
    Clase para crear y mostrar una ventana interactiva con un polígono y una línea en Pygame.
    """

    def __init__(self,playerList: List[Player],ball: Ball,field: Field,viewWidht,viewHeight,time):
        # Inicializar Pygame
        self.player_list = playerList
        pygame.init()

        self.view_width = viewWidht
        self.view_height = viewHeight

        self.time = time
        # Configurar la ventana
        self.field: Field = field

        self.field_width, self.field_height = field.width, field.height

        self.ball: Ball = ball
        self.screen = pygame.display.set_mode((self.view_width, self.view_height))
        pygame.display.set_caption('Partido de Futbol')

        # Colores
        self.bg_color = (0, 128, 0)  # Gris claro
        self.line_color = (255, 0, 0)    # Rojo
        self.polygon_color = (0, 0, 255) # Azul

       

    def transform_point(self,v):
        return [(v[0] / self.field_width)*self.view_width,(v[1] / self.field_height)*self.view_height]
        

    def transform_polygon(self,vertices):
        vertices_transformados = []
        for i in range(len(vertices)):
            verticescopia = list(vertices[i])
            verticescopia[0] = (verticescopia[0] / self.field_width)*self.view_width
            verticescopia[1] = (verticescopia[1] / self.field_height)*self.view_height
            vertices_transformados.append(verticescopia)
        return vertices_transformados

    def plot_players(self):
        for id in range(len(self.player_list)):
            vertices_transformados = self.transform_polygon(self.player_list[id].action_area.exterior.coords)
            # if self.player_list[id].regiondelcampoasignada != None:
            #     vertices_voronoi_transformados = self.transform_polygon(self.player_list[id].regiondelcampoasignada.exterior.coords)
            #     pygame.draw.polygon(self.screen, self.player_list[id].color, vertices_voronoi_transformados,width=2)
            if self.player_list[id].soycandidato == True: 
                    self.player_list[id].fuicandidato = self.time
                    self.player_list[id].soycandidato = False
                    pygame.draw.polygon(self.screen, (180,180,0), vertices_transformados)  
                    
                        
            else:   
                #print("Tiempo:" , self.player_list[id].fuicandidato )                
                if self.player_list[id].fuicandidato > 0 and (self.time - self.player_list[id].fuicandidato) < 0.15: 
                    pygame.draw.polygon(self.screen, (180,180,0), vertices_transformados)   
                else: 
                    #print("me meteo")
                    pygame.draw.polygon(self.screen, self.player_list[id].color, vertices_transformados)
                    self.player_list[id].fuicandidato = -1

                
            pygame.draw.circle(self.screen,(0,0,255),self.transform_point(self.player_list[id].movement.move_destination_coordinates),radius=2)
        


    def plot(self):
        # Método para actualizar la visualización
        self.screen.fill(self.bg_color)
        self.plot_field()  # Rellenar el fondo con el color gris clar
        self.plot_players()
        self.plot_ball()
        # Dibujar la línea
       
    def plot_field(self):
        vertices_transformados = self.transform_polygon(self.field.sites.area_grande_izquierda.exterior.coords)
        pygame.draw.polygon(self.screen, (255,255,255), vertices_transformados,width=2)
        vertices_transformados = self.transform_polygon(self.field.sites.area_pequenia_izquierda.exterior.coords)
        pygame.draw.polygon(self.screen, (255,255,255), vertices_transformados,width=2)
        vertices_transformados = self.transform_polygon(self.field.sites.area_grande_derecha.exterior.coords)
        pygame.draw.polygon(self.screen, (255,255,255), vertices_transformados,width=2)
        vertices_transformados = self.transform_polygon(self.field.sites.area_pequenia_derecha.exterior.coords)
        pygame.draw.polygon(self.screen, (255,255,255), vertices_transformados,width=2)
        vertices_transformados = self.transform_polygon(self.field.sites.mediocampo_izquierda.exterior.coords)
        pygame.draw.polygon(self.screen, (255,255,255), vertices_transformados,width=2)
        vertices_transformados = self.transform_polygon(self.field.sites.mediocampo_derecha.exterior.coords)
        pygame.draw.polygon(self.screen, (255,255,255), vertices_transformados,width=2)
        pygame.draw.circle(self.screen,(255,255,255),self.transform_point([self.field.center_x,self.field.center_y]),radius=self.transform_polygon([[0,9.15]])[0][1],width=2)



    def plot_ball(self):
        vertices_transformados = self.transform_polygon(self.ball.action_area.exterior.coords)
        pygame.draw.polygon(self.screen, (255,255,255), vertices_transformados)


    def visualice(self):
        # Bucle principal de la aplicación
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
            

            # Actualizar la pantalla
        self.plot()
        pygame.display.flip()

        
