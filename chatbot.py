from telegram.ext import Updater, MessageHandler, Filters
import configparser
import logging
from ChatGPT_HKBU import HKBU_ChatGPT


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # 注册一个处理器来处理消息
    conversation_handler = MessageHandler(Filters.text & (~Filters.command), conversation)
    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()
    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)
    # dispatcher for chatgpt
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),
                                     equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)


def conversation(update, context):
    user_input = update.message.text.lower()

    # 在这里添加您的对话逻辑
    if user_input == "你好":
        reply_message = "你好！"
    elif user_input == "你叫什么名字":
        reply_message = "我是KLBot，很高兴认识你！"
    else:
        reply_message = "抱歉，我不明白你在说什么。"

    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


if __name__ == '__main__':
    main()
