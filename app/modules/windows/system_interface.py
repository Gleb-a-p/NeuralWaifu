# coding: utf-8
"""
This is a module for executing system commands for VA
"""

import pyautogui
import webbrowser
import geocoder
import num2words
import datetime
import subprocess as sp
import os


class SystemExecutor:
    def __init__(
            self,
            browser,
            gallery_path,
            language,
            screenshot_name,
            screenshot_extension
    ) -> None:
        self.browser = browser
        self.gallery_path = gallery_path
        self.language = language
        self.screenshot_name = screenshot_name
        self.screenshot_extension = screenshot_extension

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

        print(f"Снимок экрана сохранен как { screenshot_path }")
        screenshot.save( screenshot_path )

    def run_script(self, script_file: str) -> None:
        try:
            script_path = os.path.split(script_file)[0].lstrip('"') + '/'
            print(f"Script directory: {script_path}")
            result = sp.Popen([script_file], cwd=script_path)
            print(f"Успешный запуск файла {script_file}")
            print(f"Код запуска: {result}")

        except Exception as error:
            print(f"Ошибка при запуске через субпроцесс: {error}. Файл запускается напрямую")

            try:
                os.system(script_file)
                print(f"Успешный запуск файла {script_file}")

            except Exception as err:
                print(f"Ошибка при запуске файла: {err}")

    def open_browser(self, url: str) -> None:
        webbrowser.get(self.browser).open_new_tab(url)

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
