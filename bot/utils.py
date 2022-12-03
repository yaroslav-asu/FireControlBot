# gets command that user writes to bot
def command_params_parser(command_text: str) -> list:
    return command_text.split()[1:]
