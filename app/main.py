# -*- coding: utf-8 -*-
"""
This is main file, includes import
of all necessary libraries and modules.
You need run this file to run project.
"""

import configparser

import app.modules.core.logic.general_config as general_config # General configuration
from app.modules.voice_assistant import VoiceAssistance, create_va, choose_va_role # Global VA creating tools


def read_config() -> str:
    # Reading data from the configuration file
    conf: configparser.ConfigParser = configparser.ConfigParser()
    conf.read("../../../etc/config.ini")
    api_key: str = conf['DEFAULT']['Api_key']

    return api_key


def main() -> None:
    api_key = read_config() # Get api key from config.ini

    models_ids: list = [] # list with ids of working models

    dialogue_history: list = [] # list for storing dialog history

    print(f"OS: {general_config.OPERATION_SYSTEM}")

    va_role = choose_va_role(general_config.VA_MODES, general_config.MODE_CHOOSING_MESSAGE)

    match va_role:
        case "j":
            import app.modules.core.roles.jarvis_config as specific_config

        case "m":
            import app.modules.core.roles.mita_config as specific_config

        case _:
            import app.modules.core.roles.jarvis_config as specific_config

    VA = create_va(general_config, specific_config, models_ids, api_key, dialogue_history) # Creating VA

    if isinstance( VA, VoiceAssistance ):
        VA.run() # Джарвис работает в штатном режиме, сэр
        print(f"Принудительное завершение работы модели (ID: {specific_config.VA_ID})")


if __name__ == "__main__":
    main()
