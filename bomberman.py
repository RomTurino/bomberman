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


class SolidBlock(arcade.Sprite):
    def __init__(self):
        super().__init__('Blocks/SolidBlock.png')


class ExplodableBlock(arcade.Sprite):
    def __init__(self):
        super().__init__('Blocks/ExplodableBlock.png')

class Bomberman(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__(0.5)
        self.texture = arcade.load_texture('Bomberman/Front/Bman_F_f00.png')
        self.center_y = SCREEN_HEIGHT/ROW_COUNT - CELL_HEIGHT/2
        self.center_x = SCREEN_WIDTH/COLUMN_COUNT - CELL_WIDTH/2

        #textures front
        self.textures_front = []
        for i in range(8):
            self.textures_front.append(arcade.load_texture(f'Bomberman/Front/Bman_F_f0{i}.png'))
        # textures front
        self.textures_back = []
        for i in range(8):
            self.textures_back.append(arcade.load_texture(f'Bomberman/Back/Bman_B_f0{i}.png'))
        #textures_right
        self.textures_right = []
        for i in range(8):
            self.textures_right.append(arcade.load_texture(f'Bomberman/Side/Bman_F_f0{i}.png'))
        # textures_left
        self.textures_left = []
        for i in range(8):
            self.textures_left.append(arcade.load_texture(f'Bomberman/Side/Bman_F_f0{i}.png',
                                                          flipped_horizontally=True))
        self.textures = self.textures_front
        self.texture = self.textures[0]

class OurGame(arcade.Window):
    # Конструктор окна
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture('Blocks/BackgroundTile.png')
        self.blocks = arcade.SpriteList()
        self.occupied_places = []
        self.bomberman = Bomberman()
        self.walk = False

    # начальные значения
    def setup(self):
        for x in range(ROW_COUNT):
            for y in range(COLUMN_COUNT):
                if x % 2 == 1 and y % 2 == 1:
                    solid_block = SolidBlock()
                    solid_block.center_x = x * 60 + CELL_WIDTH / 2
                    solid_block.center_y = y * 60 + CELL_HEIGHT / 2
                    self.blocks.append(solid_block)
                    self.occupied_places.append((solid_block.center_x, solid_block.center_y))
                if random.randint(1, 2) == 1:
                    print(f"Ну, икс здесь {x}, а игрек {y}")
                    if not(x==0 and y<=2) and not( y == 0 and x<=2) and not(y==10  and x>=9) and not(x==10 and y>=9):#условие должно выбросить из зоны появления блоков две площадки для главных героев
                        explodable_block = ExplodableBlock()
                        explodable_block.center_x = x * 60 + CELL_WIDTH / 2
                        explodable_block.center_y = y * 60 + CELL_HEIGHT / 2
                        if (explodable_block.center_x, explodable_block.center_y) not in self.occupied_places:
                            self.blocks.append(explodable_block)


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

    # нажатие на клавишу
    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.LEFT:
            self.bomberman.change_x = -5
        if key == arcade.key.RIGHT:
            self.bomberman.change_x = 5
        if key == arcade.key.UP:
            self.bomberman.change_y = 5
        if key == arcade.key.DOWN:
            self.bomberman.change_y = -5
    # ненажатие на клавишу
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.LEFT:
            self.bomberman.change_x =  0
        if key == arcade.key.RIGHT:
            self.bomberman.change_x = 0
        if key == arcade.key.UP:
            self.bomberman.change_y = 0
        if key == arcade.key.DOWN:
            self.bomberman.change_y =  0


window = OurGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
