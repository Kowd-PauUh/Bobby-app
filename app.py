from imports import *

Config.set('kivy', 'keyboard_mode', 'systemanddock')


class Container(BoxLayout):
    text_input = ObjectProperty()
    enter_btn = ObjectProperty()

    def send_data(self):
        if self.text_input.text != '':
            print(self.text_input.text)
            self.text_input.text = ''
            print(self.text_input.size)

    def rescale_text_input(self):
        pass

    def rescale_enter_btn(self):
        self.enter_btn.size[0] = self.size[1] * 0.06


class BobbyApp(App):

    def __init__(self):
        super().__init__()
        self.text_input = TextInput()

    def build(self):
        return Container()


if __name__ == '__main__':
    BobbyApp().run()
