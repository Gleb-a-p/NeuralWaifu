# coding: utf-8
"""
This is a module for executing system commands for VA
"""

import os
import pyautogui
import webbrowser
import geocoder
import num2words
import datetime
import subprocess as sp
import psutil


class SystemExecutor:
    def __init__(
            self,
            system_name,
            operation_system,
            browser,
            gallery_path,
            language,
            screenshot_name,
            screenshot_extension
    ) -> None:
        self.system_name = system_name
        self.operation_system = operation_system
        self.browser = browser
        self.gallery_path = gallery_path
        self.language = language
        self.screenshot_name = screenshot_name
        self.screenshot_extension = screenshot_extension

    def __str__(self) -> str:
        return f"{self.system_name} system interface for OS: {self.operation_system}"

    def get_current_time(self) -> str:
        now = datetime.datetime.now()
        text = (f"Сейчас {num2words.num2words(now.hour, lang=self.language)} "
                f"{num2words.num2words(now.minute, lang=self.language)} "
                "по системному времени.")

        return text

    def take_screenshot(self) -> None:
        gallery = os.listdir(self.gallery_path)
        last_screenshot_ind = -1

        if gallery:
            last_screenshot = os.listdir(self.gallery_path)[-1].lstrip(self.screenshot_name).strip(self.screenshot_extension)
            last_screenshot_ind = int( last_screenshot + "0" * (last_screenshot == '') )

        screenshot: pyautogui.screenshot = pyautogui.screenshot()
        screenshot_path = self.gallery_path + '/' + self.screenshot_name + str(last_screenshot_ind + 1) + self.screenshot_extension

        print(f"{self.system_name} сделал снимок экрана")
        print(f"Снимок экрана сохранен как { screenshot_path }")

        screenshot.save( screenshot_path )

    def run_script(self, script_file: str) -> None:
        try:
            script_path = os.path.split(script_file)[0].lstrip('"') + '/'
            print(f"Script directory: {script_path}")
            result = sp.Popen([script_file], cwd=script_path)
            print(f"{self.system_name} выполнил успешный запуск файла {script_file}")
            print(f"Код запуска: {result}")

        except Exception as error:
            print(f"Ошибка при запуске через субпроцесс: {error}. Файл запускается напрямую")

            try:
                os.system(script_file)
                print(f"{self.system_name} выполнил успешный запуск файла {script_file}")

            except Exception as err:
                print(f"Ошибка при запуске файла: {err}")

    def open_browser(self, url: str) -> None:
        webbrowser.get(self.browser).open_new_tab(url)
        print(f"{self.system_name} открыл сайт: {url}")

    def search_file(self, file_name, search_directory) -> str:
        if os.path.exists(search_directory):
            print(f"Searching file {file_name} in {search_directory}...")

            potential_files = []
            ind = 0

            for root, dirs, files in os.walk(search_directory):
                if file_name in files:
                    potential_files.append(os.path.join(root, file_name))

            if len(potential_files) > 1:
                print("Several matches were found: \n" + "\n".join(
                    [f"{file}. {potential_files[file]}" for file in range(len(potential_files))]))
                ind = int(input("Please, select the required file number: "))

            return potential_files[ind]

        else:
            print(f"Error: Directory {search_directory} does not exists.")

            return "NONE"

    def open_text_file(self, directory, file_name) -> None:
        # directory, file_name = os.path.split(relative_path)

        abs_path = self.search_file(file_name=file_name, search_directory=directory)
        if abs_path != "NONE":
            print(f"Open file: {abs_path}")

            os.startfile(abs_path)

    def get_location(self) -> tuple[str, str]:
        try:
            geo_location = geocoder.ip("me")

            if geo_location.ok:
                location = geo_location.latlng
                latitude, longitude = location
                print(f"Location: {location}\n"
                      f"Широта: {latitude},\n"
                      f"Долгота: {longitude}")

                return num2words.num2words(latitude, lang=self.language), num2words.num2words(longitude, lang=self.language)

            return "нет информации", "нет информации" # "Не удалось определить широту", "Не удалось определить долготу"

        except Exception as err:
            print(f"Возникла ошибка при определении геолокации: {err}")

            return "нет информации", "нет информации" # "Не удалось определить широту", "Не удалось определить долготу"

    def get_battery_charge(self) -> str:
        battery_info = psutil.sensors_battery()
        print(f"Текущий заряд батареи: {battery_info.percent}% \n"
              f"Подключение к зарядке: {battery_info.power_plugged}")

        return num2words.num2words(battery_info.percent, lang=self.language)
