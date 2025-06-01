# -*-coding: utf-8 -*-
# This is main file with import of all necessary libraries and functions, you need run this file to run project.

# Импорт библиотек
from openai import OpenAI
from PyQt6.QtWidgets import QApplication, QMainWindow
from random import randint, choice
import configparser
import webbrowser
import time
# import os
import sys

# Импорт модулей
import app.modules.core.logic.config as config # Модуль конфигурации
from app.modules.graphics.gui import Ui_MainWindow # Модуль графического интерфейса
import app.modules.core.logic.dialogue as dialogue # Модуль диалоговой логики(ChatGPT)
import app.modules.audio.audio_detection as audio_detection # Модуль работы с речью(распознавание)
import app.modules.audio.audio_speaking as audio_speaking # Модуль работы с речью(синтез)


# Класс MainWindow для настройки главного окна приложения
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, client, dialog, mod):
        super().__init__()
        self.setupUi(self)
        self.client = client
        self.dialog = dialog
        self.mod = mod

        self.pushButton.clicked.connect(self.button_clicked)
        self.pushButton.setCheckable(True)

    def button_clicked(self):
        print("Clicked!")
        entered_message = self.lineEdit.text()

        if entered_message.strip() != "": # Если сообщение не пустое
            self.listWidget.addItem(f"User: {entered_message}")
            print(f"Entered message: {entered_message}")

            self.lineEdit.setText("")
            time.sleep(randint(10, 30) / 1000)

            response = dialogue.va_respond("Джарвис " * (not(entered_message.startswith(config.VA_NAME))) + entered_message, self.client, self.dialog, self.mod)
            self.listWidget.addItem(f"Джарвис: {response}")

            # if self.mod == "base":
            #     self.listWidget.addItem(dialogue.generate_response(self.dialog, entered_message, self.mod, self.client))
            # elif self.mod == "free":
            #     self.listWidget.addItem(dialogue.generate_response(dialogue_history=self.dialog, message=entered_message, mod=self.mod))

            print(self.dialog)


# Main
def main():
    # Записываем время запуска программы
    start = time.time()

    # Читаеем данные из файла конфигурации
    conf = configparser.ConfigParser()
    conf.read('../../../etc/config.ini')
    api_key = conf['DEFAULT']['Api_key']

    # Инициализация OpenAI клиента
    client = OpenAI(
        api_key=api_key,
        base_url=config.BASE_GPT_URL # base_url="https://api.proxyapi.ru/openai/v1",
    )

    # Список для хранения истории диалога
    dialogue_history = []

    # Проверка клиента OpenAI на корректность
    mod = "base"
    # print(dialogue.generate_response(dialogue_history, "Кто ты?", mod, client))
    if dialogue.generate_response(dialogue_history, config.CHECKING_MESSAGE, mod, client) == None: # Если апи-ключ не работает, то используем свободную модель
        mod = "free"
    else:
        mod = dialogue.get_mod() # Если апи-ключ рабочий, то предлагаем выбор между бесплатной моделью и моделью через апи-ключ

    # Создание приложения
    app = QApplication(sys.argv)

    # Создание MainWindow
    window = MainWindow(client=client, dialog=dialogue_history, mod=mod)
    window.show()

    # Фиксируем путь к браузеру
    webbrowser.register(config.BASE_BROWSER, None, webbrowser.BackgroundBrowser(config.CHROME_PATH))

    # Фиксирование окончания запуска бота
    end = time.time()

    # Вывод отладочной информации
    print(f"{config.VA_NAME} (v{config.VA_VERSION}) начал свою работу ...")
    print(f"Api key: {api_key}")
    print(f"OpenAI client: {client}")
    print(f"Mod = {mod}")
    print(f"Время на запуск: {round(end - start, 2)} секунд")

    # Запускаем цикл событий.
    app.exec()

    # Запуск голосового ассистента
    audio_speaking.va_speak(choice(config.GREETING_LIST)) # Приветствие при запуске
    audio_detection.va_listen(dialogue.va_respond, client, dialogue_history, mod) # Начать прослушивание команд


if __name__ == "__main__":
    main()
