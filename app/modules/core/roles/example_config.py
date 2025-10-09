# coding: utf-8
"""
This is a module with specific VA's settings for [имя]
"""

# Base options
VA_NAME: str = "" # Name
VA_SYSTEM_NAME: str = "" # System name(English)
VA_ID: int = 0 # ID

# WW list
VA_WAKE_WORD_LIST: list[str] = [
    ""
]

# Prompt
VA_PROMPT: str = ""

# Responses to commands
VA_GREETING_LIST: list[str] = [
    ""
]

VA_GREETING_MESSAGE: str = (
    "Приветствую!\n"
    f"Меня зовут {VA_NAME}, "
    "я - текстовый и голосовой компьютерный помощник!\n"
    "Я умею:\n"
    " - сообщать время,\n"
    " - отвечать на ваши вопросы,\n"
    " - рассказывать анекдоты,\n"
    " - запускать игры и скрипты, \n"
    " - запускать музыку, \n"
    " - делать скриншоты, \n"
    " - и открывать браузер.\n"
    "Буду всегда рад(а) помочь!"
)

VA_EXECUTED_ANSWER_LIST: list[str] = [
    ""
]

VA_PRAISE_ANSWERS: list[str] = [
    ""
]

VA_CENSURE_ANSWERS: list[str] = [
    ""
]

VA_CALL_ANSWERS: list[str] = [
    ""
]

VA_POTENTIAL_CALL_ANSWERS = [
    ""
]

VA_POWEROFF_MESSAGE_LIST: list[str] = [
    ""
]

# Constants
VA_SPEAKER: str = "aidar" # baya / kseniya / xenia / random
