
#    15-112: Principles of Programming and Computer Science
#    Final Project
#    Name      : Nayla Al Mulla
#    AndrewID  : nimulla

# Importing Libraries
import sys
import pygame
from time import sleep
from slayer import Health
from pygame.sprite import Group
from pygame.sprite import Sprite
import pygame.font


pygame.mixer.init()
pygame.mixer.init(44100, 16, 2, 4096)

# Background Music
pygame.mixer.music.load("mountain.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Gun Sounds
shoot_sound = pygame.mixer.Sound('shoot.wav')
shoot_sound.set_volume(0.5)
# Dragon Killed sound
killed_sound = pygame.mixer.Sound('killed.wav')
killed_sound.set_volume(0.5)




class Setting:


    def __init__(self):
        # Intitialize games static settings
        self.screen_width = 800
        self.screen_height = 600
        self.background = pygame.image.load('forest.png')
        self.slayer_speed = 5.0
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_speed = 3.5
        self.bullet_color = (72, 178, 210)
        # Limiting number of Bullets, this decreases with each level
        self.bullets_allowed = 4
        # Dragon Setting
        self.dragon_speed = 6.5
        self.slayer_limit = 3
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        # These settings change throughout the game
        self.slayer_speed = 3.5
        self.bullet_speed = 3.0
        self.dragon_speed = 6.0
        self.fleet_direction = 1
        # Scores, everytime you kill a dragon you get 10 points
        self.dragon_points = 10

    def increase_speed(self):
        # Increasing the speed
        self.slayer_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.dragon_speed *= self.speedup_scale
        self.dragon_points = int(self.dragon_points * self.score_scale)


class Scoreboard:
    def __init__(self, ai_game):
        # Initializing score settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.setting = ai_game.setting
        self.stats = ai_game.stats
        self.ai_game = ai_game

        # Font settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.Font(None, 24)
        # Prep
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_health()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score = self.font.render("Score : " + str(score_str), True, (255, 255, 255))
        # Display at top right of screen
        self.score_rect = self.score.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score = self.font.render("High Score : " + str(high_score_str), True, (204, 0, 51))
        # Display at top  of screen
        self.high_score_rect = self.high_score.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        # Displays Score
        self.screen.blit(self.score, self.score_rect)
        self.screen.blit(self.high_score, self.high_score_rect)
        self.screen.blit(self.level, self.level_rect)
        self.healths.draw(self.screen)

    def check_high_score(self):
        # check to see if there is new highscore
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        level_str = str(self.stats.level)
        # Sets up Level
        self.level = self.font.render("Level : " + str(level_str), True, (255, 255, 255))
        self.level_rect = self.level.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_health(self):
        self.healths = Group()
        # Controls the slayers health
        for health_number in range(self.stats.slayer_left):
            health = Health(self.ai_game)
            health.rect.x = 10 + health_number * health.rect.width
            health.rect.y = 10
            self.healths.add(health)


class Slayer:
    def __init__(self, ai_game):
        # Initializing Slayer Settings
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('satyr.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.slayer_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.setting.slayer_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_slayer(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


class Health(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('heart.png')
        self.rect = self.image.get_rect()


class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width, self.setting.bullet_height)
        self.rect.midtop = ai_game.slayer.rect.midtop
        self.y = float(self.rect.y)
        self.color = self.setting.bullet_color

    def update(self):
        self.y -= self.setting.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Dragon(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        # Load dragon image and set rect attribute
        self.image = pygame.image.load('monster.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.setting.dragon_speed * self.setting.fleet_direction)

        self.rect.x = self.x

    def check_edges(self):
        # return True if dragon is at edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


class GameStats:
    def __init__(self, ai_game):
        self.setting = ai_game.setting
        self.game_active = False
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        self.slayer_left = self.setting.slayer_limit
        self.score = 0
        self.level = 1


class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 50, 60
        self.button_color = (103, 170, 182)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 48)
        # center the button
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class FireSlayer:
    def __init__(self):
        pygame.init()
        self.setting = Setting()
        self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))

        pygame.display.set_caption("Fire Slayer")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.slayer = Slayer(self)
        self.bullets = pygame.sprite.Group()
        self.dragons = pygame.sprite.Group()
        self._create_fleet()


        self.play_button = Button(self, "Fire Slayer   ||  Start Game")



    def _create_fleet(self):
        # creating rows of dragons
        dragon = Dragon(self)
        dragon_width, dragon_height = dragon.rect.size
        # dragon_width = dragon.rect.width
        available_space_x = self.setting.screen_width - (2 * dragon_width)
        number_dragons_x = available_space_x // (2 * dragon_width)
        slayer_height = self.slayer.rect.height
        available_space_y = (self.setting.screen_height - (3 * dragon_height) - slayer_height)
        number_rows = available_space_y // (2 * dragon_height)
        for row_number in range(number_rows):
            for dragon_number in range(number_dragons_x):
                self._create_dragon(dragon_number, row_number)

    def _create_dragon(self, dragon_number, row_number):
        dragon = Dragon(self)
        dragon_width, dragon_height = dragon.rect.size
        dragon.x = dragon_width + 2 * dragon_width * dragon_number
        dragon.rect.x = dragon.x
        dragon.rect.y = dragon.rect.height + 2 * dragon.rect.height * row_number
        self.dragons.add(dragon)

    def _fire_bullet(self):
        if len(self.bullets) < self.setting.bullets_allowed:
            shoot_sound.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # moving slayer to right
            self.slayer.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.slayer.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.slayer.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.slayer.moving_left = False

    def _check_fleet_edges(self):
        for dragon in self.dragons.sprites():
            if dragon.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for dragon in self.dragons.sprites():
            dragon.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                if event.key == pygame.K_RIGHT:
                    self.slayer.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.slayer.moving_left = False

    def _check_play_button(self, mouse_pos):
        # Starts new game when player click "Start Game"
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            self.setting.initialize_dynamic_setting()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            # self.sb.prep_level()
            self.sb.prep_health()
            # self.stats.game_active = True
            # get rid of remaining dragons and bullets
            self.dragons.empty()
            self.bullets.empty()
            # hide mouse cursor
            pygame.mouse.set_visible(False)
            # create new fleet and center slayer
            self._create_fleet()
            self.slayer.center_slayer()

    def _update_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.setting.background, (0, 0))
        self.slayer.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.dragons.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:

            self.play_button.draw_button()
        pygame.display.flip()

    def _update_dragons(self):
        self._check_fleet_edges()
        self.dragons.update()
        if pygame.sprite.spritecollideany(self.slayer, self.dragons):
            self._slayer_hit()
            self._check_dragons_bottom()
            killed_sound.play()

    def _slayer_hit(self):
        if self.stats.slayer_left > 0:
            self.stats.slayer_left -= 1
            self.sb.prep_health()
            self.dragons.empty()
            self.bullets.empty()
            self._create_fleet()
            self.slayer.center_slayer()
            # If the dragon hits the slayer, the game pauses for 0.5 seconds before starting again

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_dragon_collisions()

    def _check_bullet_dragon_collisions(self):

        collisions = pygame.sprite.groupcollide(self.bullets, self.dragons, True, True)
        if collisions:
            killed_sound.play()
            for dragons in collisions.values():
                self.stats.score += self.setting.dragon_points * len(dragons)

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.check_high_score()

        if not self.dragons:
            self.bullets.empty()
            self._create_fleet()
            self.setting.increase_speed()

            # Increasing Level
            self.stats.level += 1
            self.sb.prep_level()

    def _check_dragons_bottom(self):
        # check if any dragons reached bottom of screen
        screen_rect = self.screen.get_rect()
        for dragon in self.dragons.sprites():
            if dragon.rect.bottom >= screen_rect.bottom:
                self._slayer_hit()
                break

    def run_game(self):

        while True:
            self._check_events()
            if self.stats.game_active:
                self.slayer.update()
                self.bullets.update()
                self._update_bullets()
                self._update_dragons()

            self._update_screen()




if __name__ == '__main__':
    ai = FireSlayer()
    ai.run_game()
