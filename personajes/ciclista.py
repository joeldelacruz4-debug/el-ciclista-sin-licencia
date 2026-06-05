import pygame

class Ciclista:

    def __init__(self):

        self.x = 400
        self.y = 500

        self.velocidad_x = 0
        self.aceleracion = 0.8
        self.friccion = 0.85
        self.max_vel = 8

        self.energia = 100
        self.energia_max = 100

        self.imagen = pygame.image.load("assets/imagenes/ciclista.png")
        self.imagen = pygame.transform.scale(self.imagen, (60, 80))

    def mover(self, teclas):

        # movimiento suave lateral
        if teclas[pygame.K_LEFT]:
            self.velocidad_x -= self.aceleracion

        if teclas[pygame.K_RIGHT]:
            self.velocidad_x += self.aceleracion

        self.velocidad_x *= self.friccion

        # límite velocidad lateral
        self.velocidad_x = max(-self.max_vel, min(self.velocidad_x, self.max_vel))

        self.x += self.velocidad_x

        # límites pista
        if self.x < 220:
            self.x = 220
            self.velocidad_x = 0

        if self.x > 520:
            self.x = 520
            self.velocidad_x = 0

        # energía
        if teclas[pygame.K_UP] and self.energia > 0:
            self.energia -= 0.2

        if teclas[pygame.K_DOWN]:
            self.energia += 0.2

        self.energia = max(0, min(self.energia, self.energia_max))

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def obtener_rectangulo(self):
        return pygame.Rect(self.x + 10, self.y + 10, 40, 60)