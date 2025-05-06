import pygame
import sys
import os

# Ajoute le chemin vers la racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
# Maintenant tu peux importer
from Option_marche.marche import Marche


# Initialisation de pygame
pygame.init()

# Définir la taille de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu Pygame")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Polices
font = pygame.font.Font(None, 36)

def draw_main_menu():
    screen.fill(WHITE)

    # Texte du menu
    title_text = font.render("Menu Principal", True, BLACK)
    play_text = font.render("Jouer", True, BLACK)
    quit_text = font.render("Quitter", True, BLACK)

    # Afficher le titre et les options
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, 200))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 300))

    pygame.display.update()

def handle_main_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 200 < event.pos[1] < 240:  # Vérifie si "Jouer" est cliqué
                return "play"
            if 300 < event.pos[1] < 340:  # Vérifie si "Quitter" est cliqué
                pygame.quit()
                sys.exit()

    return None

def draw_second_menu():
    screen.fill(WHITE)

    # Texte du menu
    title_text = font.render("Deuxième Menu", True, BLACK)
    option1_text = font.render("Bouger une patte", True, BLACK)
    option2_text = font.render("Marche télécommandée (z,q,s,d)", True, BLACK)
    option3_text = font.render("Option 3", True, BLACK)
    option4_text = font.render("Option 4", True, BLACK)

    # Afficher le titre et les options
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(option1_text, (SCREEN_WIDTH // 2 - option1_text.get_width() // 2, 200))
    screen.blit(option2_text, (SCREEN_WIDTH // 2 - option2_text.get_width() // 2, 250))
    screen.blit(option3_text, (SCREEN_WIDTH // 2 - option3_text.get_width() // 2, 300))
    screen.blit(option4_text, (SCREEN_WIDTH // 2 - option4_text.get_width() // 2, 350))

    pygame.display.update()

def handle_second_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 200 < event.pos[1] < 240:  # Vérifie si "Option 1" est cliqué
                return "Bouger une patte"
            if 250 < event.pos[1] < 290:  # Vérifie si "Option 2" est cliqué
                marche = Marche()
                marche.run()
                
            if 300 < event.pos[1] < 340:  # Vérifie si "Option 3" est cliqué
                return "option3"
            if 350 < event.pos[1] < 390:  # Vérifie si "Option 4" est cliqué
                return "option4"

    return None
