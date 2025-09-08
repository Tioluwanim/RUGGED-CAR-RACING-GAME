import pygame
from menu import main_menu, high_score_screen, difficulty_screen, instructions_screen
from car_game import run_game

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Car Racing Game")

running = True
difficulty = "normal"



while running:
    choice = main_menu(screen)
    if choice == "play":
        result = run_game(difficulty)
        if result == "restart":
            run_game(difficulty)
    elif choice == "difficulty":
        difficulty = difficulty_screen(screen)
    elif choice == "instructions":
        instructions_screen(screen)
    elif choice == "highscore":
        high_score_screen(screen)
    elif choice == "quit":
        running = False


pygame.quit()
