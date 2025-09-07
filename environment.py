import pygame
import random

environments = {
    "forest": {"road": (60, 60, 60), "background": "images/bg_forest.jpg"},
    "desert": {"road": (194, 178, 128), "background": "images/bg_desert.jpg"},
    "snow": {"road": (220, 220, 220), "background": "images/bg_snow.jpg"},
    "lava": {"road": (80, 0, 0), "background": "images/bg_lava.jpg"},
    "beach": {"road": (210, 180, 90), "background": "images/bg_beach.jpg"},
    "daytime_city": {"road": (120, 120, 120), "background": "images/bg_daytime_city.jpg"},
    "city": {"road": (30, 30, 30), "background": "images/bg_city.jpg"},
    "countryside": {"road": (70, 70, 70), "background": "images/bg_countryside.jpg"},
    "river": {"road": (40, 40, 50), "background": "images/bg_river.jpg"},
}


class EnvironmentManager:
    def __init__(self, duration=5000, transition_duration=1000):
        """
        duration: how long each environment stays before transition (ms)
        transition_duration: fade duration in ms
        """
        self.duration = duration
        self.transition_duration = transition_duration
        self.last_change = pygame.time.get_ticks()

        self.themes = []
        for theme in environments.values():
            theme_copy = theme.copy()
            bg_path = theme.get("background")
            if bg_path:
                try:
                    bg_img = pygame.image.load(bg_path).convert()
                    theme_copy["background_img"] = bg_img
                except Exception as e:
                    print(f"Failed to load {bg_path}: {e}")
                    theme_copy["background_img"] = None
            else:
                theme_copy["background_img"] = None
            self.themes.append(theme_copy)

        self.index = 0
        self.current_theme = self.themes[self.index]
        self.next_theme = None
        self.transition_alpha = 0
        self.transition_start_time = 0

    def update(self):
        """Call this every frame. Returns (road_color, current_bg_img, next_bg_img, alpha)"""
        now = pygame.time.get_ticks()
        # check if it's time to start a transition
        if now - self.last_change > self.duration and self.next_theme is None:
            self.index = (self.index + 1) % len(self.themes)
            self.next_theme = self.themes[self.index]
            self.transition_alpha = 0
            self.transition_start_time = now
            self.last_change = now

        # handle transition alpha
        if self.next_theme:
            elapsed = now - self.transition_start_time
            self.transition_alpha = min(
                255, 255 * elapsed / self.transition_duration)
            if self.transition_alpha >= 255:
                # transition complete
                self.current_theme = self.next_theme
                self.next_theme = None
                self.transition_alpha = 0

        return (
            self.get_colors(),
            self.current_theme["background_img"],
            self.next_theme["background_img"] if self.next_theme else None,
            self.transition_alpha,
        )

    def get_colors(self):
        return self.current_theme["road"]


def lerp_color(c1, c2, t):
    """Linearly interpolate between two RGB colors. t = 0..1"""
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )


def get_random_car():
    car_sprites = [
        "Ambulance.png",
        "Audi.png",
        "Black_viper.png",
        "car.png",
        "Mini_truck.png",
        "Mini_van.png",
        "Police.png",
        "taxi.png",
        "truck.png"
    ]

    return random.choice(car_sprites)
