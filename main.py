import json
from os import path
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from random import randrange


DATA = 'data'

def load_json(file):
        file = path.join(DATA, file)
        return json.load(open(file))


class Bot:
    TOKEN = open(path.join(DATA, 'YLTB token')).read().strip()
    REQUEST_KWARGS = load_json('proxy socks5.json')
    QUESTIONS = load_json('questions.json')['questions']
    # Структура файла вопросов:
    # {'questions': [[вопрос1, правильный ответ, неправильный ответ], ...]}

    def __init__(self):
        updater = Updater(self.TOKEN, use_context=True, 
                          request_kwargs=self.REQUEST_KWARGS)

        # Получаем из него диспетчер сообщений.
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("help", self.help))
        conv_handler = ConversationHandler(
            # Точка входа в диалог.
            # В данном случае — команда /start. Она задаёт первый вопрос.
            entry_points=[CommandHandler('start', self.start)],

            states={
                1: [MessageHandler(Filters.text, self.answer, pass_user_data=True)]
            },

            # Точка прерывания диалога. В данном случае — команда /stop.
            fallbacks=[CommandHandler('stop', self.stop)]
        )
        dp.add_handler(conv_handler)
        
        # Запускаем цикл приема и обработки сообщений.
        updater.start_polling()

        # Ждём завершения приложения.
        updater.idle()

    def ask(self, update, context):
        n_left = len(context.user_data['not asked'])
        if n_left <= 0:
            self.finish(update, context, n_left)
            return True
        q = context.user_data['not asked'].pop(randrange(n_left))
        context.user_data['q'] = q
        update.message.reply_text(self.QUESTIONS[q][0])
##                                  reply_markup=self.markup(q))
##
##    def markup(self, q):
##        return ReplyKeyboardMarkup(

    def answer(self, update, context):
        update.message.reply_text("Ответ пришёл!")
        ans = update.message.text
        if ans == self.QUESTIONS[context.user_data['q']][1]:
            context.user_data['right'] += 1
        if self.ask(update, context):
            return ConversationHandler.END
        return 1

    def start(self, update, context):
        context.user_data['not asked'] = list(range(len(self.QUESTIONS)))
        context.user_data['right'] = 0
        update.message.reply_text("Дороу! Щя буит мяса!")
        self.ask(update, context)
        return 1

    def help(self, update, context):
        update.message.reply_text(
            """/start - запуск викторины
/help - помощь
/stop - завершить викторину

deployed by heroku v.0.9.21
""")

    def stop(self, update, context):
        update.message.reply_text("Хотите завершить игру?")

    def finish(self, update, context, n_left):
        print(context.user_data['right'])
        res = context.user_data['right']
        update.message.reply_text(f"Ваш результат: {context.user_data['right']}"
                                  f" из {len(self.QUESTIONS) - n_left}.")


if __name__ == '__main__':
    bot = Bot()
