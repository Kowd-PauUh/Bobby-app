import src.auxiliary_functions as af


class Bobby:
    def __init__(self):
        self.messages_panel = None

    def add_message_panel(self, messages_panel):
        self.messages_panel = messages_panel

    @staticmethod
    def handle_message(message):
        if message.content_type == 'text':
            pass

    @staticmethod
    def handle_reply(callback_data):
        pass

    def send_keyboard(self):
        pass
