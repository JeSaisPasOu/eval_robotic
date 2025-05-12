import pygame
import sys
import os

# Import des classes des modules
from Option_marche.marche import Marche
from Option_rotation.rotate import Rotate 
from Option_acceleration.acceleration import Acceleration
from Option_controle_records.records import Marche_controle

# Initialisation Pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu Pygame")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)

def draw_main_menu():
    screen.fill(WHITE)
    title = font.render("Menu Principal", True, BLACK)
    play = font.render("Jouer", True, BLACK)
    quit_ = font.render("Quitter", True, BLACK)

    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(play, (SCREEN_WIDTH // 2 - play.get_width() // 2, 200))
    screen.blit(quit_, (SCREEN_WIDTH // 2 - quit_.get_width() // 2, 300))

    pygame.display.update()

def handle_main_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 200 < event.pos[1] < 240:
                return "play"
            if 300 < event.pos[1] < 340:
                return "quit"
    return None

def draw_second_menu():
    screen.fill(WHITE)

    options = [
        "Bouger une patte",
        "Marche télécommandée (z,q,s,d)",
        "Rotation Hexapode",
        "Gérer accélération hexapode",
        "Enregistrer les mouvements effectués et les lire"
    ]

    title = font.render("Deuxième Menu", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    for i, text in enumerate(options):
        rendered = font.render(text, True, BLACK)
        screen.blit(rendered, (SCREEN_WIDTH // 2 - rendered.get_width() // 2, 200 + i * 50))

    pygame.display.update()

def handle_second_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            y = event.pos[1]
            if 200 < y < 240:
                print("Bouger une patte choisie")
                return "Bouger une patte"
            elif 250 < y < 290:
                marche = Marche()
                marche.run()
            elif 300 < y < 340:
                rotate = Rotate()
                rotate.run()
            elif 350 < y < 390:
                accel = Acceleration()
                accel.run()
            elif 400 < y < 440:
                controle = Marche_controle()
                controle.run()
    return None
