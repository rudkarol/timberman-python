import pygame

TEXTURE_DIR = "assets/textures"


class Assets:
    def __init__(self):
        self.background = pygame.image.load(f"{TEXTURE_DIR}/background.png")

        self.tree_empty = pygame.image.load(f"{TEXTURE_DIR}/tree0.png")
        self.tree_left = pygame.image.load(f"{TEXTURE_DIR}/tree1.png")
        self.tree_right = pygame.image.load(f"{TEXTURE_DIR}/tree2.png")
        self.owl = pygame.image.load(f"{TEXTURE_DIR}/owl.png")
        self.player = pygame.image.load(f"{TEXTURE_DIR}/player.png")
        self.player_chopping = pygame.image.load(f"{TEXTURE_DIR}/player1.png")

        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 30)
        self.score_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 40)
        self.small_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 20)

        self.chop_sound = pygame.mixer.Sound("assets/sounds/chop.wav")
        self.death_sound = pygame.mixer.Sound("assets/sounds/death.wav")
        self.out_of_time_sound = pygame.mixer.Sound("assets/sounds/out_of_time.wav")
