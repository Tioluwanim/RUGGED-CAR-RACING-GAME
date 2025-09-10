import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        # 🎵 Background music
        self.background_music = "audio/background-sound.wav"

        # 🔊 Sound effects
        self.sounds = {
            "crash": pygame.mixer.Sound("audio/car-crash.wav"),
            # "menu_click": pygame.mixer.Sound("audio/menu-click.wav"),
            "game_over": pygame.mixer.Sound("audio/game_over.wav"),
        }

        # volumes (optional fine-tuning)
        self.sounds["crash"].set_volume(1.0)
      #   self.sounds["level_up"].set_volume(0.7)
      #   self.sounds["menu_click"].set_volume(0.5)
        self.sounds["game_over"].set_volume(0.8)

    # ===== Background Music =====
    def play_music(self, loop: bool = True):
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()

    # ===== Sound Effects =====
    def play(self, name: str):
        if name in self.sounds:
            self.sounds[name].play()
