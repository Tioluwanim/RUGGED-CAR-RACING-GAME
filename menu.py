# menu.py
import pygame
from pygame.locals import *

pygame.init()

# Colors and font
WHITE, YELLOW, BLACK = (255, 255, 255), (255, 232, 0), (0, 0, 0)
FONT = pygame.font.Font(pygame.font.get_default_font(), 28)

# --- Utility Functions ---
def draw_text(screen, text, pos, color=WHITE):
    """Helper to draw centered text"""
    label = FONT.render(text, True, color)
    rect = label.get_rect(center=pos)
    screen.blit(label, rect)


# --- High Score Persistence ---
def save_high_score(score, filename="highscore.txt"):
    """Save new high score if it's greater than the stored one"""
    try:
        best = load_high_score(filename)
        if score > best:
            with open(filename, "w") as f:
                f.write(str(score))
    except Exception:
        with open(filename, "w") as f:
            f.write(str(score))


def load_high_score(filename="highscore.txt"):
    """Load the saved high score, defaulting to 0 if missing"""
    try:
        with open(filename, "r") as f:
            return int(f.read().strip())
    except Exception:
        return 0


# --- Screens ---
def main_menu(screen):
    """Main menu screen: returns play, highscore, difficulty, instructions, or quit"""
    clock = pygame.time.Clock()
    menu_items = ["Start Game", "High Score", "Difficulty", "Instructions", "Exit"]
    selected = 0

    while True:
        screen.fill(BLACK)
        draw_text(screen, "🚗 Car Racing Game 🚦", (250, 80), YELLOW)

        for i, item in enumerate(menu_items):
            color = YELLOW if i == selected else WHITE
            draw_text(screen, item, (250, 180 + i * 50), color)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == K_RETURN:
                    if menu_items[selected] == "Start Game":
                        return "play"
                    elif menu_items[selected] == "High Score":
                        return "highscore"
                    elif menu_items[selected] == "Difficulty":
                        return "difficulty"
                    elif menu_items[selected] == "Instructions":
                        return "instructions"
                    elif menu_items[selected] == "Exit":
                        return "quit"

        clock.tick(30)


def high_score_screen(screen):
    """Show the high score screen"""
    score = load_high_score()
    screen.fill(BLACK)
    draw_text(screen, "🏆 High Score 🏆", (250, 100), YELLOW)
    draw_text(screen, f"Best: {score}", (250, 200), WHITE)
    draw_text(screen, "Press ESC to return", (250, 400), WHITE)
    pygame.display.flip()
    wait_for_back()


def difficulty_screen(screen):
    """Difficulty selection screen"""
    screen.fill(BLACK)
    draw_text(screen, "Choose Difficulty", (250, 100), YELLOW)
    draw_text(screen, "1. Easy", (250, 180), WHITE)
    draw_text(screen, "2. Medium", (250, 220), WHITE)
    draw_text(screen, "3. Hard", (250, 260), WHITE)
    draw_text(screen, "ESC to cancel", (250, 350), WHITE)
    pygame.display.flip()
    return wait_for_difficulty()


def instructions_screen(screen):
    """Instructions / controls screen"""
    screen.fill(BLACK)
    draw_text(screen, "Instructions / Controls", (250, 100), YELLOW)
    draw_text(screen, "← → : Move left/right", (250, 180), WHITE)
    draw_text(screen, "Avoid cars & obstacles", (250, 220), WHITE)
    draw_text(screen, "Score points by surviving", (250, 260), WHITE)
    draw_text(screen, "Press ESC to return", (250, 400), WHITE)
    pygame.display.flip()
    wait_for_back()


# --- Wait Helpers ---
def wait_for_back():
    """Wait until user presses ESC or closes window"""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                waiting = False


def wait_for_difficulty():
    """Wait for difficulty key press"""
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_1:
                    return "easy"
                elif event.key == K_2:
                    return "normal"
                elif event.key == K_3:
                    return "hard"
                elif event.key == K_ESCAPE:
                    return "normal"  # default if canceled
            if event.type == QUIT:
                return "normal"
