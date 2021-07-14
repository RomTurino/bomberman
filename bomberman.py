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
REPULSION = 12


def position_check(position_x, position_y):
    for x, y in window.occupied_places:
        if position_x >= x and position_y >= y:
            position_x = x
            position_y = y
            return position_x, position_y
        else:
            return position_x,position_y


class SolidBlock(arcade.Sprite):
    def __init__(self):
        super().__init__('Blocks/SolidBlock.png')

    def update(self):
        if arcade.check_for_collision(self, window.bomberman):
            window.bomberman.stop()


class ExplodableBlock(arcade.Sprite):
    def __init__(self):
        super().__init__('Blocks/ExplodableBlock.png')

    def update(self):
        '''if arcade.check_for_collision(self, window.bomberman):
            if self.top < window.bomberman.bottom:

                self.top = window.bomberman.bottom - 50
            elif self.bottom > window.bomberman.top:

                self.bottom = window.bomberman.bottom
            elif self.right < window.bomberman.left:

                self.right = window.bomberman.left
            elif self.left > window.bomberman.right:

                self.left = window.bomberman.right'''


class Bomberman(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__(0.5)
        self.texture = arcade.load_texture('Bomberman/Front/Bman_F_f00.png')
        self.center_y = SCREEN_HEIGHT / ROW_COUNT - CELL_HEIGHT / 2
        self.center_x = SCREEN_WIDTH / COLUMN_COUNT - CELL_WIDTH / 2

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
        self.state = arcade.FACE_RIGHT
        self.textures = self.walk_down_textures

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        if self.right > window.width:
            self.right = window.width
        if self.bottom < 0:
            self.bottom = 0
        if self.top > window.height:
            self.top = window.height

        '''touch = self.collides_with_list(window.blocks)
        if len(touch) > 0:
          for block in touch:
                if self.top > block.bottom:
                    print(f'Низ у бомбера: {self.bottom}, Верх у блока {block.top}')
                    self.top = block.bottom - 50
                elif self.bottom < block.top:
                    print(f'Верх у бомбера: {self.top}, Низ у блока {block.bottom}')
                    self.bottom = block.bottom
                elif self.right > block.left:
                    print(f'Право у бомбера: {self.right}, лево у блока {block.left}')
                    self.right = block.left
                elif self.left < block.right:
                    print(f'Лево у бомбера: {self.left}, Право у блока {block.right}')
                    self.left = block.right'''


class OurGame(arcade.Window):
    # Конструктор окна
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture('Blocks/BackgroundTile.png')
        self.blocks = arcade.SpriteList(use_spatial_hash=True)
        self.grid = []
        self.occupied_places = []
        self.bomberman = Bomberman()
        self.walk = False
        self.step = time.time()

    # начальные значения
    def setup(self):
        for x in range(ROW_COUNT):
            self.grid.append([])
            for y in range(COLUMN_COUNT):
                if x == 0:
                    print(f'Итак, x = {x}, y = {y}')
                if x % 2 == 1 and y % 2 == 1:
                    self.grid[x].append(1)
                    solid_block = SolidBlock()
                    solid_block.center_x = x * 60 + CELL_WIDTH / 2
                    solid_block.center_y = y * 60 + CELL_HEIGHT / 2
                    self.blocks.append(solid_block)
                    self.occupied_places.append((solid_block.center_x, solid_block.center_y))

                    if x == 0:
                        print(f'вот добавили единичку - {self.grid[0]}')
                elif random.randint(1, 2) == 1:
                    if not (x == 0 and y <= 2) and not (y == 0 and x <= 2) and not (y == 10 and x >= 9) and not (
                            x == 10 and y >= 9):  # условие должно выбросить из зоны появления блоков две площадки для главных героев
                        explodable_block = ExplodableBlock()
                        explodable_block.center_x = x * 60 + CELL_WIDTH / 2
                        explodable_block.center_y = y * 60 + CELL_HEIGHT / 2
                        if (explodable_block.center_x, explodable_block.center_y) not in self.occupied_places:
                            self.grid[x].append(2)
                            self.blocks.append(explodable_block)
                            self.occupied_places.append((explodable_block.center_x, explodable_block.center_y))

                            if x == 0:
                                print(f'вот добавили двоечку - {self.grid[0]}')
                else:
                    self.grid[x].append(0)
                    if x == 0:
                        print(f'вот добавили нолик - {self.grid[0]}')
        for i in self.grid:
            print(i)

    # отрисовка объектов
    def on_draw(self):
        arcade.start_render()
        for x in range(11):
            for y in range(11):
                arcade.draw_texture_rectangle(x * 60 + CELL_WIDTH / 2, y * 60 + CELL_HEIGHT / 2, CELL_WIDTH,
                                              CELL_HEIGHT, self.bg)
        self.blocks.draw()
        self.bomberman.draw()

    # игровая логика
    def update(self, delta_time):
        self.bomberman.update()
        self.bomberman.update_animation()
        self.blocks.update()

    # нажатие на клавишу
    def on_key_press(self, key: int, modifiers: int):
        touch = arcade.check_for_collision_with_list(self.bomberman, self.blocks)

        if key == arcade.key.LEFT and not self.walk:
            self.bomberman.change_x = -10
            self.walk = True

        if key == arcade.key.RIGHT and not self.walk:
            self.bomberman.change_x = 10
            self.walk = True



        if key == arcade.key.UP and not self.walk:
            self.bomberman.change_y = 10
            self.walk = True

        if key == arcade.key.DOWN and not self.walk:
            self.bomberman.change_y = -10
            self.walk = True

        # self.step = time.time()

    # ненажатие на клавишу
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.bomberman.change_x = 0
            self.walk = False
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.bomberman.change_y = 0
            self.walk = False


window = OurGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
