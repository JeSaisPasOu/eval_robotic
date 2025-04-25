import sys
sys.path.append('./source/PY')

from menu import draw_menu, handle_events
import pygame # type: ignore
import sys

# Initialisation de pygame
pygame.init()

# Définir la taille de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spider-man")

def main():
    while True:
        draw_menu()
        choice = handle_events()

        if choice == "play":
            print("L'utilisateur a choisi de jouer")
            # Ici, tu peux démarrer un autre écran ou une autre scène du jeu
            # Par exemple, appeler une fonction `game_loop()`
            break

if __name__ == "__main__":
    main()
