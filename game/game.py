import pygame

import connection
from game.assets import Assets
from game.config import (
    BONUS_REDUCTION,
    FPS,
    INITIAL_TIME,
    MAX_NICKNAME_LENGTH,
    MAX_TIME,
    MIN_TIME_BONUS,
    SCREEN_MIDDLE,
    TIME_BONUS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    Position,
    TreeSegment,
)
from game.player import Player
from game.renderer import Renderer
from game.tree import Tree


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Timberman")
        self.clock = pygame.time.Clock()

        self.assets = Assets()
        self.tree = Tree()
        self.player = Player()
        self.renderer = Renderer(self.window, self.assets)

        self.points = 0
        self.game_running = False
        self.game_over_sound_played = False
        self.show_rescue_button = False
        self.animal_rescued = False
        self.show_record_text = False

        self.remaining_time = INITIAL_TIME
        self.last_update = pygame.time.get_ticks()

        self.nickname = ""
        self.nickname_active = True

    def reset(self):
        self.tree.reset()
        self.player.reset()
        self.points = 0
        self.game_running = False
        self.game_over_sound_played = False
        self.show_rescue_button = False
        self.animal_rescued = False
        self.show_record_text = False
        self.remaining_time = INITIAL_TIME
        self.last_update = pygame.time.get_ticks()

    def _start_game(self):
        self.reset()
        self.game_running = True

    def _confirm_nickname(self):
        if len(self.nickname) > 0:
            self.nickname_active = False

    def _handle_mouse_click(self, pos):
        if self.nickname_active:
            if len(self.nickname) > 0 and self.renderer.nickname_start_button.collidepoint(pos):
                self._confirm_nickname()
            return

        if not self.game_running:
            if self.renderer.start_button_rect.collidepoint(pos):
                self._start_game()
            return

        if self.show_rescue_button and self.renderer.rescue_button_rect.collidepoint(pos):
            self._rescue_animal()
            return

        x, _ = pos
        position = Position.LEFT if x < SCREEN_MIDDLE else Position.RIGHT
        self.player.chop(position)
        self._cut_tree()

    def _handle_key(self, event):
        if self.nickname_active:
            if event.key == pygame.K_BACKSPACE:
                self.nickname = self.nickname[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._confirm_nickname()
            elif len(self.nickname) < MAX_NICKNAME_LENGTH and event.unicode.isalnum():
                self.nickname += event.unicode
            return

        if not self.game_running:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._start_game()
            return

        if event.key == pygame.K_SPACE and self.show_rescue_button:
            self._rescue_animal()
        elif event.key in (pygame.K_a, pygame.K_LEFT):
            self.player.chop(Position.LEFT)
            self._cut_tree()
        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            self.player.chop(Position.RIGHT)
            self._cut_tree()

    def _rescue_animal(self):
        if self.tree.rescue_animal():
            self.animal_rescued = True
            self.show_rescue_button = False
            self.points += 5

    def _cut_tree(self):
        danger_segment = self.tree.segments[1]

        if danger_segment == TreeSegment.ANIMAL and not self.animal_rescued:
            self.points = max(0, self.points - 10)

        self.tree.cut()
        self.animal_rescued = False

        if ((danger_segment == TreeSegment.LEFT_BRANCH and self.player.position == Position.LEFT) or
                (danger_segment == TreeSegment.RIGHT_BRANCH and self.player.position == Position.RIGHT)):
            self.game_running = False
            self.assets.death_sound.play()
            self._save_score()
            return

        self.assets.chop_sound.play()
        self.points += 1

        time_reduction = (self.points // 10) * BONUS_REDUCTION
        bonus = max(MIN_TIME_BONUS, TIME_BONUS - time_reduction)
        self.remaining_time = min(self.remaining_time + bonus, MAX_TIME)

        self.show_rescue_button = self.tree.has_animal_next()

    def _save_score(self):
        try:
            user_data = connection.get_user_max_scores(self.nickname)
            if not user_data.items:
                connection.create_user(self.nickname, self.points)
            elif self.points > user_data.items[0].score:
                self.show_record_text = True
                connection.update_user_max_scores(user_data.items[0].id, self.points)
        except Exception as e:
            print(e)

    def _update_time(self):
        if not self.game_running:
            return

        current_time = pygame.time.get_ticks()
        reduction = current_time - self.last_update
        self.last_update = current_time

        self.remaining_time = max(0, self.remaining_time - reduction)
        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.game_running = False
            if not self.game_over_sound_played:
                self.assets.out_of_time_sound.play()
                self.game_over_sound_played = True
                self._save_score()

    def _draw(self):
        self.renderer.draw_background()

        if self.nickname_active:
            self.renderer.draw_nickname_input(self.nickname)
            return

        self.renderer.draw_timer_bar(self.remaining_time)
        self.renderer.draw_tree(self.tree)
        self.renderer.draw_player(self.player)
        self.renderer.draw_score(self.points, self.nickname)

        if self.show_rescue_button and self.game_running:
            self.renderer.draw_rescue_button()

        if not self.game_running:
            self.renderer.draw_game_over(self.points, self.show_record_text)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_mouse_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self._handle_key(event)

            self._update_time()
            self.player.update()
            self._draw()
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
