from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Bobby(App):

    def __init__(self):
        super().__init__()
        self.text_input = TextInput()

    def build(self):

        enter_btn = Button(text='Enter')

        layout = BoxLayout()
        layout.add_widget(self.text_input)
        layout.add_widget(enter_btn)
        return layout


if __name__ == '__main__':
    Bobby().run()
