import pygame
import random

class Auto:

    def __init__(self):

        self.x = random.randint(220, 530)
        self.y = -100

        self.ancho = 60
        self.alto = 100

        self.imagen = pygame.image.load(
            "assets/imagenes/auto.png"
        )

        self.imagen = pygame.transform.scale(
            self.imagen,
            (60, 100)
        )

    def mover(self, velocidad):

        # El auto se mueve según la velocidad del ciclista
        self.y += velocidad

        # Reinicio cuando sale de pantalla
        if self.y > 600:
            self.y = -100
            self.x = random.randint(220, 530)

    def dibujar(self, pantalla):

        pantalla.blit(
            self.imagen,
            (self.x, self.y)
        )

    def obtener_rectangulo(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.ancho,
            self.alto
        )