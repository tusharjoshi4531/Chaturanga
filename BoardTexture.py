from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label

from kivy.graphics import *

from kivy.properties import *

from Global import *

class BoardTexture(RelativeLayout):
    '''Draws board on the screen'''

    padding = NumericProperty(0.95)
    square_side_length = NumericProperty(0)
    square_size = ListProperty([])

    square_texture = {0: 'assets/square_brown_light_1x.png',
                      1: 'assets/square_brown_dark_1x.png'}

    true_board_pos = ListProperty([])
    true_board_size = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='hi'))

        board_size = (SIZE[1] * self.padding, SIZE[1] * self.padding)
        board_pos = (SIZE[1] * (1 - self.padding) / 2,
                     SIZE[1] * (1 - self.padding) / 2)

        self.true_board_pos = (SIZE[1] * (1 - self.padding * 0.95) / 2,
                               SIZE[1] * (1 - self.padding * 0.95) / 2)

        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=board_size, pos=board_pos)

        self.square_side_length = SIZE[1] * self.padding * 0.95 / 8

        self.true_board_size = (
            self.square_side_length * 8, self.square_side_length * 8)

        self.square_size = (self.square_side_length, self.square_side_length)

        for i in range(8):
            for j in range(8):

                square_pos = (self.true_board_pos[0] + j * self.square_side_length,
                              self.true_board_pos[1] + i * self.square_side_length)

                self.add_widget(Image(source=self.square_texture[(
                    i + j) % 2], size=self.square_size, size_hint=(None, None), pos=square_pos))
