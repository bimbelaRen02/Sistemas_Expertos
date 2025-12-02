import pygame
import random
import sys

pygame.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 900, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("¿Quién mató a Zeus?")
fuente = pygame.font.SysFont("aptos", 45)
clock = pygame.time.Clock()

# --- COLORES ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
DORADO = (230, 200, 70)

# --- IMÁGENES ---
fondo = pygame.image.load("fondo_olimpo.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# --- DATOS ---
sospechosos = ["Poseidón", "Hades", "Ares", "Atenea", "Hermes"]
armas = ["Rayo de Zeus", "Tridente de Poseidón", "Cetro del Inframundo", "Égida de Atenea", "Lanza de Ares"]
lugares = ["Monte Olimpo", "Inframundo", "Océanos", "Templo de Atenea", "Odeón de Herodes Ático"]

culpable = random.choice(sospechosos)
arma = random.choice(armas)
lugar = random.choice(lugares)

# --- FUNCIÓN DE TEXTO ---
def mostrar_texto(texto, x, y, color=BLANCO):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y))

# --- LOOP PRINCIPAL ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ventana.blit(fondo, (0, 0))
    mostrar_texto("¿Quién mató a Zeus?", 350, 50, DORADO)
    mostrar_texto("Haz clic para comenzar", 330, 500)
    pygame.display.flip()
    clock.tick(30)