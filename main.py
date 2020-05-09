from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import json
from os import path


DATA = 'data'

def load_json(file):
        file = path.join(DATA, file)
        return json.load(open(file))


class Bot:
    TOKEN = open(path.join(DATA, 'YLTB token')).read().strip()
    REQUEST_KWARGS = load_json('proxy socks5.json')
    # SCENARIO = load_json('SCENARIO.json')

    def __init__(self):
        updater = Updater(self.TOKEN, use_context=True, 
                          request_kwargs=self.REQUEST_KWARGS)

        # Получаем из него диспетчер сообщений.
        dp = updater.dispatcher

        # Регистрируем обработчик в диспетчере.
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(MessageHandler(Filters.text, self.resp))
        # Запускаем цикл приема и обработки сообщений.
        updater.start_polling()

        # Ждём завершения приложения.
        updater.idle()

    def resp(self, update, context):
        update.message.reply_text("Ответ пришёл!")
  
    def start(self, update, context):
        update.message.reply_text(
            "Привет! Напишите мне что-нибудь, и я пришлю ответ!")

    def help(self, update, context):
        update.message.reply_text(
            """/start - запуск бота
/help - помощь""")


if __name__ == '__main__':
    bot = Bot()
