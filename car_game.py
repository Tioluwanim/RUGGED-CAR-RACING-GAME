# car_game.py
# Mortti X 🚗💨 — Clean, fast, and smooth gameplay engine.

import pygame
from pygame.locals import *
import random
from environment import EnvironmentManager, lerp_color, get_random_car
from menu import save_high_score  # save high score to disk (menu provides this)
from sound import SoundManager
pygame.init()

# create the window
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Car Game")

# Mortti X
# Environment manager
env_manager = EnvironmentManager(duration=15000)

# update environment (initial)
road_color, current_bg, next_bg, alpha = env_manager.update()

# background scroll variables
bg_y = 0

# colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (255, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)


# game settings
gameover = False
speed = 2
score = 0
last_milestone = 0

# markers size
marker_width = 10
marker_height = 50

# road and edge markers
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

sound = SoundManager()
sound.play_music()
# x coordinates of lanes
left_lane = 150
center_lane = 250
right_lane = 350
lanes = (left_lane, center_lane, right_lane)

# for animating movement of the lane markers
lane_marker_move_y = 0


# --- SPRITE CLASSES ---
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # scale the image down so it fits in the lane
        image_scale = 70 / image.get_rect().width
        now_width = int(image.get_rect().width * image_scale)
        now_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (now_width, now_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


player_car = get_random_car()


class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load(f"images/{player_car}")
        super().__init__(image, x, y)


# player's starting coordinates
player_x = 250
player_y = 400

# create the player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Load the other vehicle images
image_filenames = ["Mini_truck.png", "truck.png",
                   "Mini_van.png", "Black_viper.png", "Police.png"]
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load("images/" + image_filename)
    vehicle_images.append(image)

# sprite group of vehicles
vehicle_group = pygame.sprite.Group()

# Load the crash image
crash = pygame.image.load("images/crash.png")
crash_rect = crash.get_rect()


# --- GAME LOOP FUNCTION ---
def run_game(difficulty="normal"):
    """
    Runs the game loop. Returns:
      - "restart" if the player chose to restart,
      - "menu" if the player chose to go back to menu,
      - "quit" if the player closed the window.
    """
    global gameover, speed, score, last_milestone, lane_marker_move_y, bg_y, current_bg, next_bg, alpha, road_color

    # reset state
    gameover = False
    paused = False
    score = 0
    last_milestone = 0
    vehicle_group.empty()
    player.rect.center = [player_x, player_y]
    lane_marker_move_y = 0
    bg_y = 0

    # adjust speed based on difficulty
    if difficulty == "easy":
        speed = 1
    elif difficulty == "hard":
        speed = 3
    else:
        speed = 2

    clock = pygame.time.Clock()
    fps = 120
    running = True

    while running:
        clock.tick(fps)

        # Update environment every frame - Mortti X
        road_color, current_bg, next_bg, alpha = env_manager.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                try:
                    save_high_score(score)
                except Exception:
                    pass
                running = False
                return "quit"

            # Handle inputs differently if paused or gameover
            if not gameover and not paused:
                if event.type == KEYDOWN:
                    if event.key == K_LEFT and player.rect.center[0] > left_lane:
                        player.rect.x -= 100
                    elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                        player.rect.x += 100
                    elif event.key == K_ESCAPE:  # ESC pauses game now
                        paused = True

                    # instant collision check (sideswipe)
                    for vehicle in vehicle_group:
                        if pygame.sprite.collide_rect(player, vehicle):
                            sound.stop_music()
                            sound.play("crash")
                            gameover = True
                            if event.key == K_LEFT:
                                player.rect.left = vehicle.rect.right
                                crash_rect.center = [player.rect.left,
                                                     (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                            elif event.key == K_RIGHT:
                                player.rect.right = vehicle.rect.left
                                crash_rect.center = [player.rect.right,
                                                     (player.rect.center[1] + vehicle.rect.center[1]) / 2]

            elif paused:
                if event.type == KEYDOWN:
                    if event.key == K_c:  # continue
                        paused = False
                    elif event.key == K_m:  # menu
                        try:
                            save_high_score(score)
                        except Exception:
                            pass
                        return "menu"

            else:  # game over
                if event.type == KEYDOWN:
                    sound.play_music()
                    if event.key == K_y:  # restart
                        try:
                            save_high_score(score)
                        except Exception:
                            pass
                        return "restart"
                    elif event.key in (K_n, K_ESCAPE):  # back to menu
                        try:
                            save_high_score(score)
                        except Exception:
                            pass
                        return "menu"

        # --- DRAWING ---

        # Mortti X code: scrolling roadside background
        if current_bg:
            bg_y += speed if not paused and not gameover else 0
            if bg_y >= height:
                bg_y = 0
            screen.blit(pygame.transform.scale(current_bg, (width, height)), (0, bg_y - height))
            screen.blit(pygame.transform.scale(current_bg, (width, height)), (0, bg_y))
            if next_bg:
                temp_img = pygame.transform.scale(next_bg, (width, height)).copy()
                temp_img.set_alpha(alpha)
                screen.blit(temp_img, (0, bg_y - height))
                screen.blit(temp_img, (0, bg_y))
        else:
            screen.fill((34, 139, 34))  # fallback green

        # road
        road_color = env_manager.current_theme["road"]
        if env_manager.next_theme:
            t = env_manager.transition_alpha / 255
            road_color = lerp_color(env_manager.current_theme["road"], env_manager.next_theme["road"], t)
        pygame.draw.rect(screen, road_color, road)
        pygame.draw.rect(screen, yellow, left_edge_marker)
        pygame.draw.rect(screen, yellow, right_edge_marker)

        # lane markers
        if not paused and not gameover:
            lane_marker_move_y += speed
            if lane_marker_move_y >= marker_height * 2:
                lane_marker_move_y = 0
        for y in range(marker_height * -2, height, marker_height * 2):
            pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
            pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

        # player car
        player_group.draw(screen)

        if not gameover and not paused:
            if len(vehicle_group) < 2:
                add_vehicle = True
                for vehicle in vehicle_group:
                    if vehicle.rect.top < vehicle.rect.height * 1.5:
                        add_vehicle = False
                if add_vehicle:
                    lane = random.choice(lanes)
                    image = random.choice(vehicle_images)
                    vehicle = Vehicle(image, lane, height / -2)
                    vehicle_group.add(vehicle)

            # move vehicles
            for vehicle in vehicle_group:
                vehicle.rect.y += speed
                if vehicle.rect.top >= height:
                    vehicle.kill()
                    score += 1
                    if score % 5 == 0 and score != last_milestone:
                        speed += 0.2
                        last_milestone = score

            # collision check
            if pygame.sprite.spritecollide(player, vehicle_group, True):
                sound.stop_music()
                sound.play("crash")
                gameover = True
                crash_rect.center = [player.rect.center[0], player.rect.top]

        # draw vehicles
        vehicle_group.draw(screen)

        # score
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render("Score: " + str(score), True, white)
        screen.blit(text, (20, 20))

        # overlays
        if paused:
            pygame.draw.rect(screen, (0, 0, 0, 180), (0, 0, width, height))
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            pause_text = font.render("⏸ Paused", True, white)
            instructions = font.render("C = Continue | M = Menu", True, white)
            screen.blit(pause_text, (width/2 - pause_text.get_width()/2, 200))
            screen.blit(instructions, (width/2 - instructions.get_width()/2, 250))

        if gameover:
            screen.blit(crash, crash_rect)
            pygame.draw.rect(screen, red, (0, 50, width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 20)
            text = font.render("Game Over! Play again? (Y/N or ESC)", True, white)
            text_rect = text.get_rect(center=(width / 2, 100))
            screen.blit(text, text_rect)

        pygame.display.update()

    return "menu"
