import random
import time

import arcade

# задаем ширину, высоту и заголовок окна
SCREEN_WIDTH = 660
SCREEN_HEIGHT = 660
CELL_WIDTH = 60
CELL_HEIGHT = 60
SCREEN_TITLE = "Bomberman"


class SolidBlock(arcade.Sprite):
    def __init__(self):
        super().__init__('Blocks/SolidBlock.png')


class ExplodableBlock(arcade.Sprite):
    def __init__(self):
        super().__init__('Blocks/ExplodableBlock.png')


class OurGame(arcade.Window):
    # Конструктор окна
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture('Blocks/BackgroundTile.png')
        self.blocks = arcade.SpriteList()
        self.occupied_places = []

    # начальные значения
    def setup(self):
        for x in range(11):
            for y in range(11):
                if x % 2 == 1 and y % 2 == 1:
                    solid_block = SolidBlock()
                    solid_block.center_x = x * 60 + CELL_WIDTH / 2
                    solid_block.center_y = y * 60 + CELL_HEIGHT / 2
                    self.blocks.append(solid_block)
                    self.occupied_places.append((solid_block.center_x, solid_block.center_y))
                if random.randint(1, 2) == 1:
                    print(f"Ну, икс здесь {x}, а игрек {y}")
                    if (x>=2 and y>0) or (x>0 and y>=2) or (x>10 and y<10) or (x<10 and y>10):#условие должно выбросить из зоны появления блоков две площадки для главных героев
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

    # игровая логика
    def update(self, delta_time):
        pass

    # нажатие на клавишу
    def on_key_press(self, symbol: int, modifiers: int):
        pass

    # ненажатие на клавишу
    def on_key_release(self, symbol: int, modifiers: int):
        pass


window = OurGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
