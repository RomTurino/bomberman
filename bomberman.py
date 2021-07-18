import random
import time

import arcade

# задаем ширину, высоту и заголовок окна
SCREEN_WIDTH = 660
SCREEN_HEIGHT = 660
ROW_COUNT = 11
COLUMN_COUNT = 11
CELL_WIDTH = 60
CELL_HEIGHT = 60
SCREEN_TITLE = "Bomberman"

POWER_PLAYER1 = 1
SPEED_PLAYER1 = 10
BOMB_COUNT_PLAYER1 = 1

POWER_PLAYER2 = 1
SPEED_PLAYER2 = 10
BOMB_COUNT_PLAYER2 = 1


def justify_x(position_x):
    for x in range(ROW_COUNT):
        x = x * 60 + CELL_WIDTH / 2
        if abs(position_x - x) <= 30:
            center_x = x
            return center_x


def justify_y(position_y):
    for y in range(COLUMN_COUNT):
        y = y * 60 + CELL_HEIGHT / 2
        if abs(position_y - y) <= 30:
            center_y = y
            return center_y


class SolidBlock(arcade.Sprite):
    def __init__(self):
        super().__init__('Blocks/SolidBlock.png')


class ExplodableBlock(arcade.Sprite):
    def __init__(self):
        super().__init__('Blocks/ExplodableBlock.png')


class Explosion(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__(0.7)
        print('появился взрыв')
        for i in range(5):
            self.textures.append(arcade.load_texture(f'Flame/Flame_f0{i}.png'))
        self.tm = time.time()

    def update(self):
        if time.time() - self.tm > 2:
            self.kill()


class Bombochka(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__(0.7)

        for i in range(1, 4):
            self.textures.append(arcade.load_texture(f'Bomb/Bomb_f0{i}.png'))
        self.texture = self.textures[0]
        self.time_bomb = time.time()
        self.power = 0

    def update(self):
        if time.time() - self.time_bomb > 3:
            exp = Explosion()
            exp.center_x = self.center_x
            exp.center_y = self.center_y
            for i in range(1, self.power + 1):
                exp1 = Explosion()
                exp1.center_x = exp.center_x - CELL_WIDTH * i
                exp1.center_y = exp.center_y
                window.explosions.append(exp1)
                exp2 = Explosion()
                exp2.center_x = exp.center_x + CELL_WIDTH * i
                exp2.center_y = exp.center_y
                window.explosions.append(exp2)
                exp3 = Explosion()
                exp3.center_x = exp.center_x
                exp3.center_y = exp.center_y - CELL_HEIGHT * i
                window.explosions.append(exp3)
                exp4 = Explosion()
                exp4.center_x = exp.center_x
                exp4.center_y = exp.center_y + CELL_HEIGHT * i
                window.explosions.append(exp4)

            window.explosions.append(exp)
            self.kill()


class Bomberman(arcade.AnimatedTimeSprite):
    def __init__(self, power_player, speed_player, bomb_count):
        super().__init__(0.5)
        # self.texture = arcade.load_texture('Bomberman/Front/Bman_F_f00.png')
        self.power_player = power_player
        self.speed_player = speed_player
        self.bomb_count = bomb_count
        # textures front
        self.walk_down_textures = []
        for i in range(8):
            self.walk_down_textures.append(arcade.load_texture(f'Bomberman/Front/Bman_F_f0{i}.png'))
        # textures back
        self.walk_up_textures = []
        for i in range(8):
            self.walk_up_textures.append(arcade.load_texture(f'Bomberman/Back/Bman_B_f0{i}.png'))
        # textures_right
        self.walk_right_textures = []
        for i in range(8):
            self.walk_right_textures.append(arcade.load_texture(f'Bomberman/Side/Bman_F_f0{i}.png'))
        # textures_left
        self.walk_left_textures = []
        for i in range(8):
            self.walk_left_textures.append(arcade.load_texture(f'Bomberman/Side/Bman_F_f0{i}.png',
                                                               flipped_horizontally=True))
        self.textures = self.walk_down_textures
        self.texture = self.textures[0]

        # character direction
        # left = 1; right = 2; top = 3; bottom = 4.
        self.direction = 0

    def costume_change(self):
        if self.direction == 1:
            self.textures = self.walk_left_textures
        elif self.direction == 2:
            self.textures = self.walk_right_textures
        elif self.direction == 3:
            self.textures = self.walk_up_textures
        elif self.direction == 4:
            self.textures = self.walk_down_textures

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.costume_change()
        self.collisions(window.solid_blocks)
        self.collisions(window.explodable_blocks)
        if self.left < 0:
            self.left = 0
        if self.right > window.width:
            self.right = window.width
        if self.bottom < 0:
            self.bottom = 0
        if self.top > window.height:
            self.top = window.height

    def collisions(self, spritelist):
        touch = arcade.check_for_collision_with_list(self, spritelist)
        if len(touch) > 0:
            for block in touch:
                if self.direction == 3 and self.top >= block.bottom:
                    self.top = block.bottom
                elif self.direction == 4 and self.bottom <= block.top:
                    self.bottom = block.top
                elif self.direction == 2 and self.right >= block.left:
                    self.right = block.left
                elif self.direction == 1 and self.left <= block.right:
                    self.left = block.right
        bombs_up =arcade.check_for_collision_with_list(self, window.bomb_power_up)
        flame_up = arcade.check_for_collision_with_list(self, window.flame_power_up)
        speed_up = arcade.check_for_collision_with_list(self, window.speed_power_up)
        if len(bombs_up) > 0:
            self.bomb_count+=1
            for bonus in bombs_up:
                bonus.kill()
        if len(flame_up) > 0:
            self.power_player+=1
            for bonus in flame_up:
                bonus.kill()
        if len(speed_up) > 0:
            self.speed_player+=1
            for bonus in speed_up:
                bonus.kill()



class OurGame(arcade.Window):
    # Конструктор окна
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture('Blocks/BackgroundTile.png')
        self.solid_blocks = arcade.SpriteList()
        self.explodable_blocks = arcade.SpriteList()
        self.occupied_places = []
        self.player1 = Bomberman(POWER_PLAYER1, SPEED_PLAYER1, BOMB_COUNT_PLAYER1) #power_player, speed_player, bomb_count
        self.player2 = Bomberman(POWER_PLAYER2, SPEED_PLAYER2, BOMB_COUNT_PLAYER2)
        self.player1_walk = False
        self.player2_walk = False
        self.bombs_player1 = arcade.SpriteList()
        self.bombs_player2 = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.bomb_power_up = arcade.SpriteList()
        self.flame_power_up = arcade.SpriteList()
        self.speed_power_up = arcade.SpriteList()

    # начальные значения
    def setup(self):
        for x in range(ROW_COUNT):
            for y in range(COLUMN_COUNT):
                if x % 2 == 1 and y % 2 == 1:
                    solid_block = SolidBlock()
                    solid_block.center_x = x * 60 + CELL_WIDTH / 2
                    solid_block.center_y = y * 60 + CELL_HEIGHT / 2
                    self.solid_blocks.append(solid_block)
                    self.occupied_places.append((solid_block.center_x, solid_block.center_y))
                elif random.randint(1, 2) == 1:
                    if not (x == 0 and y <= 2) and not (y == 0 and x <= 2) and not (y == 10 and x >= 9) and not (
                            x == 10 and y >= 9):  # условие должно выбросить из зоны появления блоков две площадки для главных героев
                        explodable_block = ExplodableBlock()
                        explodable_block.center_x = x * 60 + CELL_WIDTH / 2
                        explodable_block.center_y = y * 60 + CELL_HEIGHT / 2
                        bonus_place = random.randint(1,3)
                        if bonus_place == 1:
                            bonus = arcade.Sprite('Powerups/BombPowerup.png', 1)
                        elif bonus_place == 2:
                            bonus = arcade.Sprite('Powerups/FlamePowerup.png', 1)
                        else:
                            bonus = arcade.Sprite('Powerups/SpeedPowerup.png', 1)
                        bonus.center_x = explodable_block.center_x
                        bonus.center_y = explodable_block.center_y
                        if bonus_place == 1:
                            self.bomb_power_up.append(bonus)
                        elif bonus_place == 2:
                            self.flame_power_up.append(bonus)
                        else:
                            self.speed_power_up.append(bonus)
                        if (explodable_block.center_x, explodable_block.center_y) not in self.occupied_places:
                            self.explodable_blocks.append(explodable_block)
                            # self.occupied_places.append((explodable_block.center_x, explodable_block.center_y))
        self.player1.center_y = SCREEN_HEIGHT / ROW_COUNT - CELL_HEIGHT / 2
        self.player1.center_x = SCREEN_WIDTH / COLUMN_COUNT - CELL_WIDTH / 2
        self.player2.center_y = SCREEN_HEIGHT - CELL_HEIGHT / 2
        self.player2.center_x = SCREEN_WIDTH - CELL_WIDTH / 2
        # self.player2.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        self.player2.color = arcade.color.RED

    # отрисовка объектов
    def on_draw(self):
        arcade.start_render()
        for x in range(ROW_COUNT):
            for y in range(COLUMN_COUNT):
                arcade.draw_texture_rectangle(x * 60 + CELL_WIDTH / 2, y * 60 + CELL_HEIGHT / 2, CELL_WIDTH,
                                              CELL_HEIGHT, self.bg)
        self.bomb_power_up.draw()
        self.flame_power_up.draw()
        self.speed_power_up.draw()
        self.solid_blocks.draw()
        self.explodable_blocks.draw()
        self.player1.draw()
        self.player2.draw()
        self.bombs_player1.draw()
        self.bombs_player2.draw()
        self.explosions.draw()

    # игровая логика
    def update(self, delta_time):
        self.player1.update()
        self.player1.update_animation()
        self.player2.update()
        self.player2.update_animation()
        self.bombs_player1.update()
        self.bombs_player1.update_animation()
        self.bombs_player2.update()
        self.bombs_player2.update_animation()
        self.explosions.update()
        self.explosions.update_animation()
        self.solid_blocks.update()
        self.explodable_blocks.update()
        for fire in self.explosions:
            hit_list = arcade.check_for_collision_with_list(fire, self.solid_blocks)
            if len(hit_list) > 0:
                fire.kill()
            destroy = arcade.check_for_collision_with_list(fire, self.explodable_blocks)
            if len(destroy) > 0:
                for block in destroy:
                    block.kill()

    # нажатие на клавишу
    def on_key_press(self, key: int, modifiers: int):

        if key == arcade.key.LEFT and not self.player1_walk:
            self.player1.change_x = -self.player1.speed_player
            self.player1.direction = 1
            self.player1_walk = True

        if key == arcade.key.RIGHT and not self.player1_walk:
            self.player1.change_x = self.player1.speed_player
            self.player1.direction = 2
            self.player1_walk = True

        if key == arcade.key.UP and not self.player1_walk:
            self.player1.change_y = self.player1.speed_player
            self.player1.direction = 3
            self.player1_walk = True

        if key == arcade.key.DOWN and not self.player1_walk:
            self.player1.change_y = -self.player1.speed_player
            self.player1.direction = 4
            self.player1_walk = True

        if key == arcade.key.SPACE:
            if len(self.bombs_player1) < self.player1.bomb_count:
                bomb = Bombochka()
                bomb.center_x = justify_x(self.player1.center_x)
                bomb.center_y = justify_y(self.player1.center_y)
                bomb.power = self.player1.power_player
                self.bombs_player1.append(bomb)

        if key == arcade.key.A and not self.player2_walk:
            self.player2.change_x = -self.player2.speed_player
            self.player2.direction = 1
            self.player2_walk = True

        if key == arcade.key.D and not self.player2_walk:
            self.player2.change_x = self.player2.speed_player
            self.player2.direction = 2
            self.player2_walk = True

        if key == arcade.key.W and not self.player2_walk:
            self.player2.change_y = self.player2.speed_player
            self.player2.direction = 3
            self.player2_walk = True

        if key == arcade.key.S and not self.player2_walk:
            self.player2.change_y = -self.player2.speed_player
            self.player2.direction = 4
            self.player2_walk = True

        if key == arcade.key.F:
            if len(self.bombs_player2) < self.player2.bomb_count:
                bomb = Bombochka()
                bomb.center_x = justify_x(self.player2.center_x)
                bomb.center_y = justify_y(self.player2.center_y)
                bomb.power = self.player2.power_player
                self.bombs_player2.append(bomb)

    # ненажатие на клавишу
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player1.change_x = 0
            self.player1.direction = 0
            self.player1_walk = False
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player1.change_y = 0
            self.player1.direction = 0
            self.player1_walk = False

        if key == arcade.key.A or key == arcade.key.D:
            self.player2.change_x = 0
            self.player2.direction = 0
            self.player2_walk = False
        if key == arcade.key.W or key == arcade.key.S:
            self.player2.change_y = 0
            self.player2.direction = 0
            self.player2_walk = False


window = OurGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
