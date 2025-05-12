import sys
sys.path.append('./source/PY')

from menu import *
import pygame
import sys


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu Pygame")

def main():
    while True:
        draw_main_menu()
        choice = handle_main_menu_events()

        if choice == "play":
            print("L'utilisateur a choisi de jouer")
            second_menu()
            break

def second_menu():
    while True:
        draw_second_menu()
        handle_second_menu_events()


if __name__ == "__main__":
    main()
