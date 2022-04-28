from imports import *

Config.set('kivy', 'keyboard_mode', 'systemanddock')
con = sl.connect('bobby.db')

with con:
    con.execute("""
        CREATE TABLE USER (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        );
    """)

class Container(BoxLayout):
    input_panel = ObjectProperty()
    messages_panel = ObjectProperty()
    text_input = ObjectProperty()
    enter_btn = ObjectProperty()

    def send_data(self):
        if self.text_input.text != '':
            print(self.text_input.text)
            self.text_input.text = ''
            print(self.text_input.size)

    def rescale(self):
        self.enter_btn.size_hint[0] = self.height * 0.06 / self.width
        self.enter_btn.size_hint[1] = 0.06 * self.height / self.input_panel.height

    def rescale_input_panel(self):
        if len(self.text_input._lines) > 1 or '\n' in self.text_input.text:
            shift = len(self.text_input._lines) * self.text_input.line_height / self.height
            print(shift)
            self.input_panel.size_hint[1] = 0.06 + shift
            self.messages_panel.size_hint[1] = 0.84 - shift
        else:
            self.input_panel.size_hint[1] = 0.06
            self.messages_panel.size_hint[1] = 0.84

    def loop(self, _):
        self.rescale()
        self.rescale_input_panel()


class BobbyApp(App):

    def __init__(self):
        super().__init__()
        self.text_input = TextInput()

    def build(self):
        container = Container()
        Clock.schedule_interval(container.loop, .1)
        return container


if __name__ == '__main__':
    BobbyApp().run()
