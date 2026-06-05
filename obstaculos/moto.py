import pygame
import random

CARRILES = [260, 360, 460]

class Moto:

    def __init__(self):
        self.carriles = CARRILES
        self.x = random.choice(self.carriles)
        self.y = random.randint(-1200, -500)

        self.carril_actual = self.x

        self.imagen = pygame.image.load("assets/imagenes/moto.png")
        self.imagen = pygame.transform.scale(self.imagen, (60, 90))

    def mover(self, velocidad):
        self.y += velocidad

        if self.y > 600:
            self.y = random.randint(-1300, -600)
            self.x = random.choice(self.carriles)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def obtener_rectangulo(self):
        return pygame.Rect(self.x + 10, self.y + 10, 40, 70)