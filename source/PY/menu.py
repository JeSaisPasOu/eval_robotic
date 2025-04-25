import pygame # type: ignore
import sys

# Initialisation de pygame
pygame.init()

# Définir la taille de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spider-man")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Polices
font = pygame.font.Font(None, 36)

def draw_menu():
    screen.fill(WHITE)

    # Texte du menu
    title_text = font.render("Spiderman", True, BLACK)
    play_text = font.render("Jouer", True, BLACK)
    quit_text = font.render("Quitter", True, BLACK)

    # Afficher le titre et les options
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, 200))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 300))

    pygame.display.update()

def handle_events():
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
