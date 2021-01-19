from kivy.app import App

from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

from BoardTexture import *
from DropDownMenu import *
from Global import *
from Board import *
from Database import *

Window.size = (SIZE[0] / 2, SIZE[1] / 2)


# GameScreen....
class GameScreen(Screen):
    def save(self):
        popup = SavePasswdPopup()
        popup.open()

    def on_pre_enter(self):
        '''Called when the screen is about to be open'''
        self.ids.game_board.init_board_play()


# MenuScreen....
class MenuScreen(Screen):
    pass


# LoadScreen....
class LoadScreen(Screen):
    def load(self):
        popup = LoadPasswdPopup()
        popup.open()

    def on_pre_enter(self):
        '''Called when the screen is about to be open'''
        self.ids.load_board.init_board_play()


# LoadScreenPopups....
class LoadPasswdPopup(Popup):
    def on_confirm(self):
        '''When confirm button is clicked'''
        if open_database(self.ids.input.text):
            popup = LoadChooseTablePopup(tables=get_tables())
            popup.open()

        self.dismiss()


class LoadChooseTablePopup(Popup):
    tables = ListProperty()

    def on_load(self):
        '''When load button is clicked'''
        table_name = self.ids.table.text
        popup = LoadChooseGamePopup(
            table_name=table_name, games=get_games(table_name))
        popup.open()

        self.dismiss()

    def on_delete(self):
        '''When delete button is clicked'''
        delete_table(self.ids.table.text)

        self.dismiss()


class LoadChooseGamePopup(Popup):
    table_name = StringProperty()
    games = ListProperty()

    def on_load(self):
        '''When load button is clicked'''
        name, date, result, game = load(self.ids.game.text, self.table_name)
        app.sm.get_screen('load').ids.load_board.set_info(
            name, date, result, game)

        self.dismiss()

    def on_delete(self):
        '''When delete button is clicked'''
        delete_game(self.ids.game.text, self.table_name)

        self.dismiss()


# SaveScreenPopups....
class SavePasswdPopup(Popup):
    def on_confirm(self):
        '''When confirm button is clicked'''
        if open_database(self.ids.input.text):
            popup = SavePopup(tables=get_tables())
            popup.open()

        self.dismiss()


class SavePopup(Popup):
    tables = ListProperty([])

    def on_save(self):
        '''When save button is pressed'''
        date, result, game = app.sm.get_screen(
            'game').ids.game_board.get_info()

        name = self.ids.input.text
        table_name = self.ids.table.text

        save(name, date, result, game, table_name)

        self.dismiss()

    def on_add_table(self):
        '''When add table button is pressed'''
        popup = AddTablePopup()
        popup.open()

        self.dismiss()


class AddTablePopup(Popup):
    def on_add(self):
        '''When add button is pressed'''
        create_table(self.ids.input.text)

        self.dismiss()


class MainApp(App):
    _size = SIZE
    bg_color = (79 / 255, 28 / 255, 1 / 255, 1)

    def build(self):
        self.sm = ScreenManager()

        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(GameScreen(name='game'))
        self.sm.add_widget(LoadScreen(name='load'))

        self.sm.current = 'menu'

        return self.sm


if __name__ == '__main__':
    app = MainApp()
    app.run()
