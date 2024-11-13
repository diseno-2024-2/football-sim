import pygame
from classes.player import Player
from classes.field import Field
from typing import List


class Screen:
    """
    Clase para crear y mostrar una ventana interactiva con un polígono y una
    línea en Pygame.
    """

    def __init__(self, playerList: List[Player], field: Field, viewWidht, viewHeight):
        # Inicializar Pygame
        self.player_list = playerList
        pygame.init()

        self.view_width = viewWidht
        self.view_height = viewHeight

        # Configurar la ventana
        self.field_width, self.field_height = field.width, field.height

        self.screen = pygame.display.set_mode(
            (self.view_width, self.view_height))
        pygame.display.set_caption('Partido de Futbol')

        # Colores
        self.bg_color = (0, 128, 0)  # Gris claro
        self.line_color = (255, 0, 0)    # Rojo
        self.polygon_color = (0, 0, 255)  # Azul

    def transform_point(self, v):
        return [(v[0] / self.field_width)*self.view_width, (v[1] / self.field_height)*self.view_height]

    def transform_polygon(self, vertices):
        vertices_transformados = []
        for i in range(len(vertices)):
            verticescopia = list(vertices[i])
            verticescopia[0] = (verticescopia[0] /
                                self.field_width)*self.view_width
            verticescopia[1] = (verticescopia[1] /
                                self.field_height)*self.view_height
            vertices_transformados.append(verticescopia)
        return vertices_transformados

    def plot_players(self):
        for player in self.player_list:
            vertices_transformados = self.transform_polygon(
                player.action_area.exterior.coords)
            pygame.draw.polygon(self.screen, (255, 0, 0),
                                vertices_transformados)

            pygame.draw.circle(self.screen, (0, 0, 255), self.transform_point(
                player.movement.move_destination_coordinates), 10)

    def plot(self):
        # Método para actualizar la visualización
        # Rellenar el fondo con el color gris claro
        self.screen.fill(self.bg_color)

        self.plot_players()
        # Dibujar la línea

    def visualize(self):
        # Bucle principal de la aplicación

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

            # Actualizar la pantalla
        self.plot()
        pygame.display.flip()
