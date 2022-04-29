from imports import *

Config.set('kivy', 'keyboard_mode', 'systemanddock')
if exists('AppData/chat-history.db'):
    con = sl.connect('AppData/chat-history.db')
if not exists('AppData/chat-history.db'):
    con = sl.connect('AppData/chat-history.db')
    with con:
        con.execute("""
            CREATE TABLE HISTORY (
                message_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                message_from TEXT, -- bobby / user
                type TEXT, -- text / image / audio / video
                text TEXT, -- if type is text
                image_path TEXT, -- if type is image
                audio_path TEXT, -- if type is audio
                video_path TEXT, -- if type is video
                date DATE DEFAULT CURRENT_DATE , -- YY-MM-DD
                time TIME DEFAULT CURRENT_TIME , -- hh-mm-ss
                reply_to INTEGER
            );
        """)


class Message(BoxLayout):
    message_from = StringProperty()

    def rescale(self, _):
        self.size[1] = self.label.texture_size[1] + 2 * self.padding[1]


class Container(BoxLayout):
    input_panel = ObjectProperty()
    messages_panel = ObjectProperty()
    text_input = ObjectProperty()
    enter_btn = ObjectProperty()

    def send_data(self):
        if self.text_input.text != '':
            sql = 'INSERT INTO HISTORY (message_from, type, text) values(?, ?, ?)'
            data = 'user', 'text', self.text_input.text
            with con:
                con.execute(sql, data)

            message = Message(message_from='user')
            message.label.text = self.text_input.text
            Clock.schedule_once(message.rescale, 0)
            self.messages_panel.messages.size[1] += message.size[1]
            self.messages_panel.messages.add_widget(message)
            self.messages_panel.scroll_to(message)

            message = Message(message_from='bobby')
            message.label.text = self.text_input.text
            Clock.schedule_once(message.rescale, 0)
            self.messages_panel.messages.size[1] += message.size[1]
            self.messages_panel.messages.add_widget(message)
            self.messages_panel.scroll_to(message)

            self.text_input.text = ''

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
