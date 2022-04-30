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
                content_type TEXT, -- text / image / audio / video
                text TEXT, -- if type is text
                image_path TEXT, -- if type is image
                audio_path TEXT, -- if type is audio
                video_path TEXT, -- if type is video
                date DATE DEFAULT CURRENT_DATE , -- YY-MM-DD
                time TIME DEFAULT CURRENT_TIME , -- hh-mm-ss
                reply_to INTEGER
            );
        """)


class MessageBlock(BoxLayout):
    date = StringProperty(defaultvalue='date')


class Message(BoxLayout):
    messages_panel = ObjectProperty()  # панель в которой находятся блоки с сообщениями
    block = ObjectProperty()  # блок в котором находятся сообщения (в каждом блоке сообщения определенной даты отправки)
    message_from = StringProperty()
    content_type = StringProperty()

    @staticmethod
    def handle_message(message_from: str, content_type: str, text: str = None, reply_to: int = None,
                       image_path: str = None, audio_path: str = None, video_path: str = None):
        sql = 'INSERT INTO HISTORY (message_from, content_type, text, image_path, audio_path, video_path, reply_to) ' \
              'values(?, ?, ?, ?, ?, ?, ?)'
        data = message_from, content_type, text, image_path, audio_path, video_path, reply_to
        with con:
            con.execute(sql, data)

    @staticmethod
    def get_message(messages_panel: ScrollView, message_id: int = None):
        """ If message_id is None, shows the last message, if True shows all messages,
            if integer, shows one selected message, if [id1, id2] range, shows messages from range"""

        if message_id is True:  # all messages
            sql = 'SELECT * FROM HISTORY'
        else:  # the last message
            sql = 'SELECT * FROM HISTORY WHERE message_id = (SELECT MAX(message_id) FROM HISTORY)'

        with con:
            messages_info = con.execute(sql)
        for message_info in messages_info:
            message_id, message_from, content_type, text, image_path, audio_path, video_path, date, time, reply_to \
                = message_info

            if not messages_panel.message_blocks.children:  # создание блока сообщения
                Message().add_block(messages_panel, date)
            elif messages_panel.message_blocks.children[0].date != date:
                Message().add_block(messages_panel, date)
            Message().show_message(messages_panel, message_id, message_from, content_type, text,
                                   image_path, audio_path, video_path, date, time, reply_to)

    @staticmethod
    def add_block(messages_panel: ScrollView, date):
        new_block = MessageBlock(date=date)
        new_block.date_label.text = f'{date[8:]}.{date[5:7]}.{date[:4]}'
        new_block.size[1] = 37
        messages_panel.message_blocks.add_widget(new_block)
        messages_panel.message_blocks.size[1] += new_block.size[1] + messages_panel.message_blocks.spacing

    @staticmethod
    def show_message(messages_panel: ScrollView, message_id: int, message_from: str, content_type: str, text: str,
                     image_path, audio_path, video_path, date, time, reply_to: int):
        if content_type == 'text':
            message = TextMessage(message_from=message_from, messages_panel=messages_panel, content_type=content_type)
            message.content_label.text = text
            message.time_label.text = time[:5]
            message.block = messages_panel.message_blocks.children[0]

        Clock.schedule_once(message._rescale, 0)
        messages_panel.message_blocks.children[0].add_widget(message)
        messages_panel.scroll_to(message)

    def _rescale(self, _):
        if self.content_type == 'text':
            size = self.content_label.texture_size[1] + 2 * self.padding[1]
            self.size[1] = size
            self.messages_panel.message_blocks.size[1] += \
                size + self.messages_panel.message_blocks.spacing
            self.block.size[1] += size + self.block.spacing


class TextMessage(Message):
    pass


class ImageMessage(Message):
    pass


class ClickableLabel(Label):
    container = ObjectProperty()

    def on_touch_down(self, touch):
        if touch.is_triple_tap:  # refresh chat
            self.container.load_chat()


class Container(BoxLayout):
    upper_panel = ObjectProperty()
    messages_panel = ObjectProperty()
    input_panel = ObjectProperty()
    text_input = ObjectProperty()
    enter_btn = ObjectProperty()

    def get_data_from_user(self):
        if self.text_input.text == '' and self.messages_panel.message_blocks.children:
            self.messages_panel.scroll_to(self.messages_panel.message_blocks.children[0])

        if self.text_input.text != '':
            Message().handle_message('user', 'text', self.text_input.text)
            Message().get_message(self.messages_panel)  # show last message

            # Message().handle_message('bobby', 'text', self.text_input.text)
            # Message().get_message(self.messages_panel)  # show last message

            self.text_input.text = ''

    def load_chat(self):
        self.messages_panel.message_blocks.clear_widgets()
        self.messages_panel.message_blocks.size[1] = self.messages_panel.message_blocks.spacing
        Message().get_message(self.messages_panel, message_id=True)  # show all messages

    def rescale_enter_btn(self):
        self.enter_btn.size_hint[0] = self.height * 0.06 / self.width
        self.enter_btn.size_hint[1] = 0.06 * self.height / self.input_panel.height

    def rescale_input_panel(self):
        if len(self.text_input._lines) > 1 or '\n' in self.text_input.text:
            shift = len(self.text_input._lines) * self.text_input.line_height / self.height
            self.input_panel.size_hint[1] = 0.06 + shift
            self.messages_panel.size_hint[1] = 0.84 - shift
        else:
            self.input_panel.size_hint[1] = 0.06
            self.messages_panel.size_hint[1] = 0.84

    def loop(self, _):
        self.rescale_enter_btn()
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
