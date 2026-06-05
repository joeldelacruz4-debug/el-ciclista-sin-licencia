import pygame
import sys
import time
import random
import os

from personajes.ciclista import Ciclista
from obstaculos.auto import Auto
from obstaculos.moto import Moto
from objetos.botella import Botella

# =========================
# RECORD SYSTEM
# =========================
RECORD_FILE = "record.txt"

def cargar_records():
    if os.path.exists(RECORD_FILE):
        try:
            with open(RECORD_FILE, "r") as f:
                data = f.read().splitlines()
                best = int(data[0]) if len(data) > 0 else 0
                last = int(data[1]) if len(data) > 1 else 0
                return best, last
        except:
            return 0, 0
    return 0, 0

def guardar_records(best, last):
    with open(RECORD_FILE, "w") as f:
        f.write(f"{best}\n{last}")

best_score, last_score = cargar_records()

# =========================
# FIX PYINSTALLER
# =========================
def ruta_base(rel_path):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, rel_path)

pygame.init()
pygame.mixer.init()

# =========================
# PANTALLA
# =========================
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("El Ciclista Sin Licencia - Demo")

# =========================
# FONDOS
# =========================
fondo = pygame.image.load(ruta_base("escenarios/carretera.png"))
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

fondo_menu = pygame.image.load(ruta_base("escenarios/menu.jpg"))
fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))

# =========================
# SONIDO
# =========================
def cargar_sonido(ruta):
    try:
        return pygame.mixer.Sound(ruta)
    except:
        return None

sonido_choque = cargar_sonido(ruta_base("assets/sonidos/choque.mp3"))
sonido_botella = cargar_sonido(ruta_base("assets/sonidos/botella.mp3"))

try:
    pygame.mixer.music.load(ruta_base("assets/sonidos/musica.mp3"))
    pygame.mixer.music.play(-1)
except:
    pass

sonido_activo = True

# =========================
# FUENTES
# =========================
fuente = pygame.font.SysFont("impact", 64)
fuente_peq = pygame.font.SysFont("bahnschrift", 28)

reloj = pygame.time.Clock()

# =========================
# ESTADOS
# =========================
estado = "menu"
submenu = None

# =========================
# VARIABLES JUEGO
# =========================
CARRETERA_X = 200
CARRETERA_ANCHO = 400
CARRILES = [CARRETERA_X + 50, CARRETERA_X + 170, CARRETERA_X + 290]

velocidad_base = 5
color_timer = 0

# =========================
# REINICIO
# =========================
def reiniciar():
    global jugador, autos, moto, botella, tiempo_inicio, score

    jugador = Ciclista()
    autos = [Auto() for _ in range(3)]
    moto = Moto()
    botella = Botella()

    tiempo_inicio = time.time()
    score = 0

    for i, auto in enumerate(autos):
        auto.x = CARRILES[i % len(CARRILES)]

reiniciar()

# =========================
# BOTONES
# =========================
boton_jugar = pygame.Rect(ANCHO//2 - 120, 180, 240, 50)
boton_config = pygame.Rect(ANCHO//2 - 120, 250, 240, 50)
boton_records = pygame.Rect(ANCHO//2 - 120, 320, 240, 50)
boton_mute_menu = pygame.Rect(ANCHO//2 - 120, 390, 240, 50)
boton_salir = pygame.Rect(ANCHO//2 - 120, 460, 240, 50)

boton_back = pygame.Rect(20, 520, 200, 50)

# =========================
# BOTÓN ANIMADO (PRO)
# =========================
def dibujar_boton(rect, texto, color, mouse, timer):
    hover = rect.collidepoint(mouse)

    pulse = abs((timer % 120) - 60)

    rect_draw = rect.inflate(12, 8) if hover else rect

    color_final = (
        min(255, color[0] + pulse//3 + (40 if hover else 0)),
        min(255, color[1] + pulse//3 + (40 if hover else 0)),
        min(255, color[2] + pulse//3 + (40 if hover else 0))
    )

    pygame.draw.rect(pantalla, color_final, rect_draw, border_radius=15)
    pygame.draw.rect(pantalla, (0,0,0), rect_draw, 2, border_radius=15)

    txt = fuente_peq.render(texto, True, (255,255,255))
    pantalla.blit(
        txt,
        (
            rect_draw.x + rect_draw.width//2 - txt.get_width()//2,
            rect_draw.y + 12
        )
    )

# =========================
# LOOP
# =========================
while True:

    reloj.tick(60)
    mouse = pygame.mouse.get_pos()
    color_timer += 1

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:

            # =========================
            # MENU
            # =========================
            if estado == "menu":

                if boton_jugar.collidepoint(evento.pos):
                    reiniciar()
                    estado = "jugando"

                if boton_config.collidepoint(evento.pos):
                    submenu = "config"

                if boton_records.collidepoint(evento.pos):
                    submenu = "records"

                if boton_mute_menu.collidepoint(evento.pos):
                    sonido_activo = not sonido_activo
                    pygame.mixer.music.set_volume(1 if sonido_activo else 0)

                if boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

            # =========================
            # BACK SUBMENU
            # =========================
            if submenu in ["config", "records"]:
                if boton_back.collidepoint(evento.pos):
                    submenu = None

    # =========================
    # CONFIG
    # =========================
    if submenu == "config":
        pantalla.fill((25, 25, 25))

        txt = fuente.render("CONFIGURACIÓN", True, (255,255,255))
        pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, 100))

        pygame.draw.rect(pantalla, (200,200,200), boton_back)
        pantalla.blit(fuente_peq.render("VOLVER", True, (0,0,0)),
                      (boton_back.x + 50, boton_back.y + 10))

        pygame.display.update()
        continue

    # =========================
    # RECORDS
    # =========================
    if submenu == "records":
        pantalla.fill((10, 10, 40))

        txt = fuente.render("RECORDS", True, (255,255,255))
        pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, 80))

        pantalla.blit(fuente_peq.render(f"Mejor récord: {best_score}", True, (255,255,0)), (250, 200))
        pantalla.blit(fuente_peq.render(f"Última partida: {last_score}", True, (255,255,255)), (250, 250))

        pygame.draw.rect(pantalla, (200,200,200), boton_back)
        pantalla.blit(fuente_peq.render("VOLVER", True, (0,0,0)),
                      (boton_back.x + 50, boton_back.y + 10))

        pygame.display.update()
        continue

    # =========================
    # MENU
    # =========================
    if estado == "menu":

        pantalla.blit(fondo_menu, (0, 0))

        titulo = fuente.render("EL CICLISTA SIN LICENCIA", True, (255,255,255))
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 80))

        dibujar_boton(boton_jugar, "JUGAR", (0,150,0), mouse, color_timer)
        dibujar_boton(boton_config, "CONFIGURACIÓN", (0,120,180), mouse, color_timer)
        dibujar_boton(boton_records, "RECORDS", (180,120,0), mouse, color_timer)
        dibujar_boton(boton_mute_menu, "SONIDO", (120,120,120), mouse, color_timer)
        dibujar_boton(boton_salir, "SALIR", (180,0,0), mouse, color_timer)

        pygame.display.update()
        continue

    # =========================
    # JUEGO (TU ORIGINAL)
    # =========================
    teclas = pygame.key.get_pressed()
    jugador.mover(teclas)

    tiempo_jugado = time.time() - tiempo_inicio
    velocidad = velocidad_base + tiempo_jugado * 0.2
    score = int(tiempo_jugado * 10)

    jr = jugador.obtener_rectangulo()

    for auto in autos:
        auto.mover(velocidad)
        if auto.y > ALTO:
            auto.y = -200
            auto.x = random.choice(CARRILES)

        if jr.colliderect(auto.obtener_rectangulo()):
            jugador.energia -= 25
            auto.y = -200
            if sonido_activo and sonido_choque:
                sonido_choque.play()

    moto.mover(velocidad)
    botella.mover(velocidad)

    if jr.colliderect(moto.obtener_rectangulo()):
        jugador.energia -= 20
        moto.y = -200

    if jr.colliderect(botella.obtener_rectangulo()):
        jugador.energia += 30
        botella.y = -200
        if sonido_activo and sonido_botella:
            sonido_botella.play()

    jugador.energia = max(0, min(100, jugador.energia))

    # =========================
    # GAME OVER + RECORD
    # =========================
    if jugador.energia <= 0:

        last_score = score
        best_score = max(best_score, score)

        guardar_records(best_score, last_score)

        estado = "menu"

    # =========================
    # RENDER
    # =========================
    pantalla.blit(fondo, (0, 0))

    objetos = [jugador] + autos + [moto, botella]
    objetos.sort(key=lambda obj: obj.y)

    for obj in objetos:
        obj.dibujar(pantalla)

    pygame.draw.rect(pantalla, (255,60,60), (20,20,200,20))
    pygame.draw.rect(pantalla, (0,255,0), (20,20,2*jugador.energia,20))

    pantalla.blit(fuente_peq.render(f"Score: {score}", True, (255,255,255)), (600,20))
    pantalla.blit(fuente_peq.render(f"Tiempo: {int(tiempo_jugado)}s", True, (255,255,255)), (600,50))

    pygame.draw.rect(pantalla, (0,200,0) if sonido_activo else (200,0,0),
                     pygame.Rect(20,520,160,40), border_radius=8)

    pantalla.blit(fuente_peq.render("SONIDO", True, (255,255,255)), (40,530))

    pygame.display.update()