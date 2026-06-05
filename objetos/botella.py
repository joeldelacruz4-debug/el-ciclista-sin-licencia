import pygame
import random
import os
import sys


def ruta_base(rel_path):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, rel_path)


CARRILES = [260, 360, 460]


class Botella:

    def __init__(self):
        self.carriles = CARRILES
        self.x = random.choice(self.carriles)
        self.y = random.randint(-1000, -300)

        self.imagen = pygame.image.load(
            ruta_base("assets/imagenes/botella.png")
        )

        self.imagen = pygame.transform.scale(self.imagen, (40, 60))

    def mover(self, velocidad):
        self.y += velocidad

        if self.y > 600:
            self.y = random.randint(-1100, -400)
            self.x = random.choice(self.carriles)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def obtener_rectangulo(self):
        return pygame.Rect(self.x + 8, self.y + 8, 24, 44)