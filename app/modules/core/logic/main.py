# -*-coding: utf-8 -*-
"""
This is main file with import
of all necessary libraries and functions.
You need run this file to run project.
"""

from openai import OpenAI
from PyQt6.QtWidgets import QMainWindow, QApplication
import random
import configparser
import webbrowser
import time
import sys

import app.modules.core.logic.config as config # Configuration
import app.modules.graphics.gui as gui # Graphical interface
import app.modules.core.logic.dialogue as dialogue # Dialogue logic(Chat GPT)
import app.modules.audio.audio_detection as audio_detection # Audio(recognition)
import app.modules.audio.audio_speaking as audio_speaking # Audio(synthesis)


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

        # If message is not empty
        if entered_message.strip() != '':
            self.listWidget.addItem(f"User: {entered_message}")
            print(f"Entered message: {entered_message}")

            self.lineEdit.setText("")
            time.sleep(random.randint(10, 30) / 1000)

            response = dialogue.va_respond(
                f"{config.VA_NAME} " * (not(entered_message.startswith(config.VA_NAME))) + entered_message,
                self.client,
                self.dialog,
                self.mod
            )
            self.listWidget.addItem(f"Джарвис: {response}")

            # if self.mod == "base":
            #     self.listWidget.addItem(dialogue.generate_response(self.dialog, entered_message, self.mod, self.client))
            # elif self.mod == "free":
            #     self.listWidget.addItem(dialogue.generate_response(dialogue_history=self.dialog, message=entered_message, mod=self.mod))

            print(self.dialog)


def main():
    start: float = time.time() # recording the program launch time

    # Reading data from the configuration file
    conf: configparser.ConfigParser = configparser.ConfigParser()
    conf.read("../../../etc/config.ini")
    api_key: str = conf['DEFAULT']['Api_key']

    # Initializing an OpenAI client
    client: OpenAI = OpenAI(
        api_key=api_key,
        base_url=config.BASE_GPT_URL # base_url="https://api.proxyapi.ru/openai/v1",
    )

    dialogue_history: list = [] # list for storing dialog history

    # Checking the OpenAI client for correctness
    mod: str = "base"
    if dialogue.generate_response(
            dialogue_history,
            config.CHECKING_MESSAGE,
            mod,
            client
    ) == '': # If api key does not work, use free model
        mod = "free"
    else:
        mod = dialogue.get_mod()

    # Creating an application
    app: QApplication = QApplication(sys.argv)

    # Creating MainWindow
    window: MainWindow = MainWindow(
        client=client,
        dialog=dialogue_history,
        mod=mod
    )
    window.show()

    # Fix the browser path
    webbrowser.register(
        config.BASE_BROWSER,
        None,
        webbrowser.BackgroundBrowser(config.CHROME_PATH)
    )

    end: float = time.time() # recording the end time of the program launch

    # Output debugging information
    print(
        f"{config.VA_NAME} (v{config.VA_VERSION}) начал свою работу ...\n"
        f"Api key: {api_key}\n"
        f"OpenAI client: {client}\n"
        f"Mod = {mod}\n"
        f"Время на запуск: {(end - start):.2f} секунд"
    )

    # Starting the event loop
    app.exec()

    # Starting the voice assistant
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
