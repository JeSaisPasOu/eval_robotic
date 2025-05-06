import sys
sys.path.append('./source/PY')

# Maintenant tu peux importer le fichier menu.py
from menu import *
import pygame
import sys

# Initialisation de pygame
pygame.init()

# Définir la taille de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu Pygame")

# Boucle principale
def main():
    # Menu principal
    while True:
        draw_main_menu()  # Affiche le menu principal
        choice = handle_main_menu_events()  # Gère les événements du menu principal

        if choice == "play":
            print("L'utilisateur a choisi de jouer")
            second_menu()  # Affiche le deuxième menu
            break

def second_menu():
    # Menu secondaire avec 4 choix
    while True:
        draw_second_menu()  # Affiche le deuxième menu
        choice = handle_second_menu_events()  # Gère les événements du menu secondaire

        if choice == "Bouger une patte":
            print("Bouger une patte choisie")
            # Ajoute l'action correspondante ici
            break
        elif choice == "option2":
            print("Option 2 choisie")
            # Ajoute l'action correspondante ici
            break
        elif choice == "option3":
            print("Option 3 choisie")
            # Ajoute l'action correspondante ici
            break
        elif choice == "option4":
            print("Option 4 choisie")
            # Ajoute l'action correspondante ici
            break

if __name__ == "__main__":
    main()
