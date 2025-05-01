# -*-coding: utf-8 -*-
from gui import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow
from openai import OpenAI
import configparser
import sys
# import time
# from dialog import *


# Функция получения ответа от ChatGPT
def get_response(client, question): # Получение ответа от ИИ(ChatGPT 3.5 turbo 1106)
    # Обращение к OpenAI API
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": question}]
        )
        response = chat_completion.choices[0].message.content.strip()

        return response

    except Exception as err: # Вывод ошибки
        print(f"Произошла ошибка: {str(err)}")
        print(f"Вопрос: {question}")
        exit()


# Класс MainWindow для настройки главного окна приложения
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.button_clicked)
        self.pushButton.setCheckable(True)

    def button_clicked(self):
        print("Clicked!")
        entered_message = self.lineEdit.text()
        if entered_message.strip() != "": # Если сообщение не пустое
            self.listWidget.addItem(entered_message)
            print(entered_message)
            self.lineEdit.setText("")


# Main
def main():
    # Читаеем данные из файла конфигурации
    config = configparser.ConfigParser()
    config.read('../../../etc/config.ini')
    api_key = config['DEFAULT']['Api_key']
    print(f"Api key: {api_key}")

    # Инициализация OpenAI клиента
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.proxyapi.ru/openai/v1",
    )

    app = QApplication(sys.argv)

    # Создаём MainWindow
    window = MainWindow()
    window.show()

    # Запускаем цикл событий.
    app.exec()


if __name__ == "__main__":
    main()
