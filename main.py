import pygame
import sys

from personajes.ciclista import Ciclista
from obstaculos.auto import Auto

pygame.init()

# Ventana
ANCHO = 800
ALTO = 600

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("El Ciclista Sin Licencia")

# Colores
VERDE = (34, 139, 34)
GRIS = (100, 100, 100)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Crear ciclista
jugador = Ciclista()

# Crear enemigo
enemigo = Auto()

# Líneas carretera
linea_y = 0

# Fuente
fuente = pygame.font.SysFont(None, 50)

reloj = pygame.time.Clock()

while True:

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento jugador
    teclas = pygame.key.get_pressed()

    jugador.mover(teclas)

    # Movimiento enemigo
    enemigo.mover()

    # Colisiones
    jugador_rect = jugador.obtener_rectangulo()

    enemigo_rect = enemigo.obtener_rectangulo()

    if jugador_rect.colliderect(enemigo_rect):

        texto = fuente.render(
            "GAME OVER",
            True,
            ROJO
        )

        pantalla.blit(texto, (300, 250))

        pygame.display.update()

        pygame.time.delay(3000)

        pygame.quit()
        sys.exit()

    # Fondo
    pantalla.fill(VERDE)

    # Carretera
    pygame.draw.rect(
        pantalla,
        GRIS,
        (200, 0, 400, 600)
    )

    # Líneas carretera
    for i in range(0, 600, 120):

        pygame.draw.rect(
            pantalla,
            BLANCO,
            (390, i + linea_y, 20, 80)
        )

    # Movimiento líneas
    linea_y += 10

    if linea_y >= 120:
        linea_y = 0

    # Dibujar ciclista
    jugador.dibujar(pantalla)

    # Dibujar enemigo
    enemigo.dibujar(pantalla)

    pygame.display.update()

    reloj.tick(60)