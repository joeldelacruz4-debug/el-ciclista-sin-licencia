import pygame

class Ciclista:

    def __init__(self):

        self.x = 375
        self.y = 500

        self.ancho = 50
        self.alto = 80

        self.velocidad = 6

        self.color = (0, 0, 0)

    def mover(self, teclas):

        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidad

        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidad

        # Limites carretera
        if self.x < 220:
            self.x = 220

        if self.x > 530:
            self.x = 530

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