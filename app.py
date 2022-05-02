from imports import *
from bobby import Bobby
bobby = Bobby()

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

    # параметры сообщения
    message_id = Property(None)
    message_from = Property(None)
    content_type = Property(None)
    text = Property(None)
    image_path = Property(None)
    audio_path = Property(None)
    video_path = Property(None)
    date = Property(None)
    time = Property(None)
    reply_to = Property(None)

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
        kwargs_names = ['message_id', 'message_from', 'content_type', 'text', 'image_path',
                        'audio_path', 'video_path', 'date', 'time', 'reply_to']
        with con:
            messages_info = con.execute(sql)
        for message_info in messages_info:
            # создаю словарь параметров сообщения который потом распакую
            kwargs = dict(zip(kwargs_names, message_info))

            date = message_info[-3]
            if not messages_panel.message_blocks.children:  # создание блока сообщения
                Message().add_block(messages_panel, date)
            elif messages_panel.message_blocks.children[0].date != date:  # если блок есть, просто добавляю сообщение
                Message().add_block(messages_panel, date)
            Message().show_message(messages_panel, **kwargs)

        return Message(**kwargs)

    @staticmethod
    def add_block(messages_panel: ScrollView, date):
        new_block = MessageBlock(date=date)
        new_block.date_label.text = f'{date[8:]}.{date[5:7]}.{date[:4]}'
        new_block.size[1] = 37
        messages_panel.message_blocks.add_widget(new_block)
        messages_panel.message_blocks.size[1] += new_block.size[1] + messages_panel.message_blocks.spacing

    @staticmethod
    def show_message(messages_panel: ScrollView, **kwargs):
        """ В kwargs должны быть определены все параметры сообщения. """
        content_type = kwargs.get('content_type')
        if content_type == 'text':
            message = TextMessage(messages_panel=messages_panel, **kwargs)
            message.content_label.text = message.text
            message.time_label.text = message.time[:5]
        elif content_type == 'image':
            message = ImageMessage(messages_panel=messages_panel, **kwargs)
            message.image.source = message.image_path
        elif content_type == 'interactive':
            message = InteractiveMessage(messages_panel=messages_panel, **kwargs)
            buttons = literal_eval(message.text)
            for button_name in buttons:
                callback_data = buttons.get(button_name)
                button = CallbackButton(callback_data=callback_data, text=button_name)
                message.buttons_panel.add_widget(button)

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
        elif self.content_type == 'image':
            if self.block.size[0] - 2 * self.padding[0] - 2 * self.block.padding[0] < self.image.texture_size[0]:
                scale = \
                    (self.block.size[0] - 2 * self.padding[0] - 2 * self.block.padding[0]) / self.image.texture_size[0]
                self.image.size[0], self.image.size[1] = self.image.size[0] * scale, self.image.size[1] * scale

            self.size[0] = self.image.size[0] + 2 * self.padding[0]
            self.size[1] = self.image.size[1] + 2 * self.padding[1]
            self.messages_panel.message_blocks.size[1] += \
                self.image.size[1] + self.messages_panel.message_blocks.spacing + 2 * self.block.spacing
            self.block.size[1] += self.size[1] + self.block.spacing
            if self.message_from == 'user':
                self.pos_hint = {'right': 1}
        elif self.content_type == 'interactive':
            rows = [[]]
            max_row_len = 0
            width = 0
            counter = 0
            max_width = self.block.size[0] - 2 * self.padding[0] - 2 * self.block.padding[0]

            reversed_panel = []
            for button in self.buttons_panel.children:
                reversed_panel.insert(0, button)

            for button in reversed_panel:
                button.size = button.texture_size
                if width + button.size[0] <= max_width:
                    width += button.size[0]
                    rows[-1].append((counter, button.size[0]))
                    if width > max_row_len:
                        max_row_len = width
                else:
                    if width > max_row_len:
                        max_row_len = width
                    rows.append([])
                    rows[-1].append((counter, button.size[0]))
                    width = button.size[0]
                counter += 1

            for row in rows:
                sum_width = sum([w for i, w in row])
                if max_row_len / max_width >= 0.75:
                    scale = max_width / sum_width
                else:
                    scale = max_row_len / sum_width

                for i, w in row:
                    reversed_panel[i].size[0] *= scale

            size = len(rows) * button.size[1] + (len(rows) - 1) * self.buttons_panel.spacing[1]
            self.size[1] = size
            self.messages_panel.message_blocks.size[1] += \
                size + self.messages_panel.message_blocks.spacing
            self.block.size[1] += size + self.block.spacing


class CallbackButton(Button):
    callback_data = Property(None)

    def reply(self):
        bobby.handle_reply(self.callback_data)


class InteractiveMessage(Message):
    pass


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
            self.text_input.text = ''
            message = Message().get_message(self.messages_panel)  # show last message
            bobby.handle_message(message)

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
        bobby.add_message_panel(container.messages_panel)
        Clock.schedule_interval(container.loop, .1)
        return container


if __name__ == '__main__':
    BobbyApp().run()
