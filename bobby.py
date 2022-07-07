import src.auxiliary_functions as af


class Bobby:
    def __init__(self):
        self.messages_panel = None

    def add_message_panel(self, messages_panel):
        self.messages_panel = messages_panel

    def handle_message(self, message):
        if message.content_type == 'text':
            self.send_message('Выше картинка, ниже - клава', 'logo.jpg', '{\'Здарова\':\'rep1\',\'пупсик\':\'rep2\'}')

    def handle_reply(self, callback_data):
        pass

    def send_message(self, message_text=None, image_path=None, keyboard=None):
        if image_path is not None:
            self.messages_panel.handle_message('bobby', 'image', image_path=image_path)
            self.messages_panel.get_message()
        if message_text is not None:
            self.messages_panel.handle_message('bobby', 'text', message_text)
            self.messages_panel.get_message()
        if keyboard is not None:
            self.messages_panel.handle_message('bobby', 'interactive', keyboard)
            self.messages_panel.get_message()

