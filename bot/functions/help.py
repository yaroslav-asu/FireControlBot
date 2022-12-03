from bot.config import *

available_functions = {
    'start': 'Начало работы',
    'help': 'Помощь'
}


def show_help(message, *args, **kwargs):
    bot.send_message(message.chat.id,
                     'Здесь находятся все команды, с помощью которых вы можете общаться со мной:\n' +
                     "\n".join(list(map(lambda x: f"/{x} - {available_functions[x]}", available_functions))),
                     *args,
                     **kwargs
                     )
