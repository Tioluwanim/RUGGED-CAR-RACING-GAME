import pygame
pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound("audio/car-crash.wav")
sound.play()
input("Press Enter after you hear the sound...")
