from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout  # размещение виджетов по сетке
from kivy.uix.stacklayout import StackLayout  # размещение виджетов сколько везет в строку
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class Container(BoxLayout):
    pass


class BobbyApp(App):

    def __init__(self):
        super().__init__()
        self.text_input = TextInput()

    def build(self):
        return Container()


if __name__ == '__main__':
    BobbyApp().run()
