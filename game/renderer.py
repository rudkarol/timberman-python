import pygame

from game.assets import Assets
import game.config as cfg
from game.player import Player
from game.tree import Tree


class Renderer:
    def __init__(self, window: pygame.Surface, assets: Assets):
        self.window = window
        self.assets = assets

        self.start_button_rect = pygame.Rect(
            cfg.START_BUTTON_X, cfg.START_BUTTON_Y,
            cfg.START_BUTTON_WIDTH, cfg.START_BUTTON_HEIGHT,
        )
        self.nickname_start_button = pygame.Rect(
            (cfg.WINDOW_WIDTH - cfg.START_BUTTON_WIDTH) // 2,
            cfg.WINDOW_HEIGHT // 3 + 60,
            cfg.START_BUTTON_WIDTH, cfg.START_BUTTON_HEIGHT,
        )
        self.rescue_button_rect = pygame.Rect(
            cfg.SCREEN_MIDDLE - 80,
            cfg.WINDOW_HEIGHT - 100,
            160, 60,
        )

    def draw_background(self):
        self.window.blit(self.assets.background, (0, 0))

    def draw_timer_bar(self, remaining_time: int):
        timer_rect = pygame.Rect(
            cfg.TIMER_BAR_POS_LEFT,
            cfg.TIMER_BAR_POS_TOP - cfg.TIMER_BAR_HEIGHT // 2,
            cfg.WINDOW_WIDTH // 4,
            cfg.TIMER_BAR_HEIGHT,
        )
        pygame.draw.rect(self.window, cfg.BLACK, timer_rect)

        if remaining_time > 0:
            fill_width = (remaining_time / cfg.MAX_TIME) * (cfg.WINDOW_WIDTH // 4)
            fill_rect = pygame.Rect(
                cfg.TIMER_BAR_POS_LEFT,
                cfg.TIMER_BAR_POS_TOP - cfg.TIMER_BAR_HEIGHT // 2,
                fill_width,
                cfg.TIMER_BAR_HEIGHT,
            )
            if remaining_time > cfg.MAX_TIME * 0.6:
                color = cfg.GREEN
            elif remaining_time > cfg.MAX_TIME * 0.3:
                color = cfg.YELLOW
            else:
                color = cfg.RED
            pygame.draw.rect(self.window, color, fill_rect)

    def draw_tree(self, tree: Tree):
        y_pos = cfg.TREE_BASE_Y
        for segment in tree.segments[:7]:
            if segment == cfg.TreeSegment.LEFT_BRANCH:
                sprite = self.assets.tree_left
            elif segment == cfg.TreeSegment.RIGHT_BRANCH:
                sprite = self.assets.tree_right
            else:
                sprite = self.assets.tree_empty

            rect = sprite.get_rect(center=(cfg.SCREEN_MIDDLE, y_pos))
            self.window.blit(sprite, rect)

            if segment == cfg.TreeSegment.ANIMAL:
                owl_rect = self.assets.owl.get_rect(center=(cfg.SCREEN_MIDDLE, y_pos))
                self.window.blit(self.assets.owl, owl_rect)

            y_pos -= cfg.TREE_SEGMENT_HEIGHT

    def draw_player(self, player: Player):
        sprite = self.assets.player_chopping if player.chopping else self.assets.player
        if player.position == cfg.Position.RIGHT:
            player_x = cfg.SCREEN_MIDDLE + cfg.PLAYER_OFFSET_X
        else:
            player_x = cfg.SCREEN_MIDDLE - cfg.PLAYER_OFFSET_X
            sprite = pygame.transform.flip(sprite, True, False)

        rect = sprite.get_rect(center=(player_x, cfg.TREE_BASE_Y))
        self.window.blit(sprite, rect)

    def draw_score(self, points: int, nickname: str):
        nickname_text = self.assets.small_font.render(nickname, True, cfg.BLACK)
        self.window.blit(nickname_text, (cfg.TIMER_BAR_POS_LEFT, 60))
        score_text = self.assets.score_font.render(str(points), True, cfg.BLACK)
        self.window.blit(score_text, (cfg.WINDOW_WIDTH - 50 - score_text.get_width(), 50))

    def draw_rescue_button(self):
        pygame.draw.rect(self.window, cfg.GREEN, self.rescue_button_rect)
        text = self.assets.small_font.render("RESCUE", True, cfg.BLACK)
        text_rect = text.get_rect(center=self.rescue_button_rect.center)
        self.window.blit(text, text_rect)

    def draw_start_button(self):
        pygame.draw.rect(self.window, cfg.WHITE, self.start_button_rect)
        pygame.draw.rect(self.window, cfg.BLACK, self.start_button_rect, 2)
        text = self.assets.font.render("START", True, cfg.BLACK)
        text_rect = text.get_rect(center=self.start_button_rect.center)
        self.window.blit(text, text_rect)

    def draw_nickname_input(self, nickname: str):
        input_box = pygame.Rect(cfg.WINDOW_WIDTH // 4, cfg.WINDOW_HEIGHT // 3, cfg.WINDOW_WIDTH // 2, 40)
        pygame.draw.rect(self.window, cfg.WHITE, input_box)
        pygame.draw.rect(self.window, cfg.BLACK, input_box, 2)

        nickname_surface = self.assets.small_font.render(nickname, True, cfg.BLACK)
        nickname_rect = nickname_surface.get_rect(center=input_box.center)
        self.window.blit(nickname_surface, nickname_rect)

        prompt_text = self.assets.small_font.render("Enter Nickname:", True, cfg.BLACK)
        prompt_rect = prompt_text.get_rect(centerx=cfg.SCREEN_MIDDLE, bottom=input_box.top - 10)
        self.window.blit(prompt_text, prompt_rect)

        if len(nickname) > 0:
            pygame.draw.rect(self.window, cfg.WHITE, self.nickname_start_button)
            pygame.draw.rect(self.window, cfg.BLACK, self.nickname_start_button, 2)
            start_text = self.assets.font.render("START", True, cfg.BLACK)
            start_text_rect = start_text.get_rect(center=self.nickname_start_button.center)
            self.window.blit(start_text, start_text_rect)

    def draw_game_over(self, points: int, show_record: bool):
        if points == 0:
            text = self.assets.font.render("NEW GAME", True, cfg.BLACK)
        else:
            text = self.assets.font.render("GAME OVER", True, cfg.BLACK)
        self.window.blit(text, (cfg.SCREEN_MIDDLE - text.get_width() // 2, 350))
        self.draw_start_button()

        if show_record and points > 0:
            record_text = self.assets.font.render("NEW RECORD!", True, cfg.BLACK)
            self.window.blit(record_text, (cfg.SCREEN_MIDDLE - record_text.get_width() // 2, 550))
