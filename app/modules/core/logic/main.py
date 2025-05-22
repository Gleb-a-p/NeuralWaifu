# -*-coding: utf-8 -*-
"""
This is main file with import
of all necessary libraries and functions.
You need run this file to run project.
"""
from configparser import ConfigParser
from typing import Any

from openai import OpenAI
from PyQt6.QtWidgets import QMainWindow, QApplication
import random
import configparser
import webbrowser
import time
import sys

import app.modules.core.logic.config as config
import app.modules.graphics.gui as gui
import app.modules.core.logic.dialogue as dialogue
import app.modules.audio.audio_detection as audio_detection
import app.modules.audio.audio_speaking as audio_speaking


class MainWindow(QMainWindow, gui.Ui_MainWindow):
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
        if entered_message.strip() != '':
            self.listWidget.addItem(entered_message)
            print(f"Entered message: {entered_message}")
            self.lineEdit.setText('')
            time.sleep(random.randint(10, 30) / 1000)
            if self.mod == "base":
                self.listWidget.addItem(
                    dialogue.generate_response(
                        self.dialog, entered_message,
                        self.mod,
                        self.client
                    )
                )
            elif self.mod == "free":
                self.listWidget.addItem(
                    dialogue.generate_response(
                        dialogue_history=self.dialog,
                        message=entered_message,
                        mod=self.mod
                    )
                )
            print(self.dialog)


def main():
    start: float = time.time()

    # read data from the configuration file
    conf: ConfigParser = configparser.ConfigParser()
    conf.read("../../../etc/config.ini")
    api_key: str = conf['DEFAULT']['Api_key']

    # initializing an OpenAI client
    client: OpenAI = OpenAI(
        api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
        base_url="https://api.proxyapi.ru/openai/v1"
    )

    # list for storing dialog history
    dialogue_history: list[Any] = []

    # checking the OpenAI client for correctness
    mod: str = "base"
    print(dialogue.generate_response(
        dialogue_history,
        "Кто ты?",
        mod,
        client
    ))

    # if the api key doesn't work, use the free model
    if dialogue.generate_response(
            dialogue_history,
            "Кто ты?",
            mod,
            client
    ) is None:
        mod = "free"
    else:
        mod = dialogue.get_mod()

    # creating an application
    app: QApplication = QApplication(sys.argv)

    # creating MainWindow
    window: MainWindow = MainWindow(
        client=client,
        dialog=dialogue_history,
        mod=mod
    )
    window.show()

    # fix the browser path
    webbrowser.register(
        config.BASE_BROWSER,
        None,
        webbrowser.BackgroundBrowser(config.CHROME_PATH)
    )

    # output debugging information
    print(
        f"{config.VA_NAME} (v{config.VA_VERSION}) начал свою работу ...\n"
        f"Api key: {api_key}\n"
        f"OpenAI client: {client}\n"
        f"Mod = {mod}\n"
        f"Время на запуск: {(time.time() - start):.2f} секунд"
    )

    # starting the event loop
    app.exec()

    # starting the voice assistant
    audio_speaking.va_speak(
        random.choice(config.GREETING_LIST)
    )  # greeting at startup
    audio_detection.va_listen(
        dialogue.va_respond,
        client,
        dialogue_history,
        mod
    )  # start listening to commands


if __name__ == "__main__":
    main()
