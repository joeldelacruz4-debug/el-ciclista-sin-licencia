import pygame
import random

class Auto:

    def __init__(self):

        self.x = random.randint(220, 530)
        self.y = -100

        self.ancho = 50
        self.alto = 80

        self.velocidad = 7

        self.color = (255, 0, 0)

    def mover(self):

        self.y += self.velocidad

        if self.y > 600:

            self.y = -100
            self.x = random.randint(220, 530)

    def dibujar(self, pantalla):

        pygame.draw.rect(
            pantalla,
            self.color,
            (self.x, self.y, self.ancho, self.alto)
        )

    def obtener_rectangulo(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.ancho,
            self.alto
        )