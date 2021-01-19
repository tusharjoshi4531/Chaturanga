from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

from kivy.properties import ListProperty

from kivy.clock import Clock


class DropDownMenu(Button):
    '''Drop down menu'''
    contents = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__()

        Clock.schedule_once(self.after_init)

    def after_init(self, dt):
        '''By default python files are run before kv files,therefore any assignments made in kv file is undetected.
           This function is called after the kv files are run to overcome this issue.'''
        self.dropdown = DropDown()

        for i in self.contents:
            btn = Button(text=i, size_hint_y=None,
                         height=50, background_color=(0, 0, 0, 1))
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.bind(on_release=self.dropdown.open)

        self.dropdown.bind(on_select=lambda instance,
                           x: setattr(self, 'text', x))
