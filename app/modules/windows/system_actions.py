# coding: utf-8
# This is a file for executing system commands

import pyautogui
import webbrowser
import num2words
import datetime
import os


class SystemExecutor:
    def __init__(
            self,
            goodbye_dpi_path,
            browser,
            youtube_url,
            gallery_path,
            language,
            screenshot_name,
            screenshot_extension
    ) -> None:
        self.goodbye_dpi_path = goodbye_dpi_path
        self.browser = browser
        self.youtube_url = youtube_url
        self.gallery_path = gallery_path
        self.language = language
        self.screenshot_name = screenshot_name
        self.screenshot_extension = screenshot_extension

    def get_current_time(self) -> str:
        now = datetime.datetime.now()
        text = (f"Сейчас {num2words.num2words(now.hour, lang=self.language)} "
                f"{num2words.num2words(now.minute, lang=self.language)} "
                "по московскому времени")

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

    def run_goodbye_dpi(self) -> None:
        os.system(self.goodbye_dpi_path)

    def open_browser(self, url: str) -> None:
        webbrowser.get(self.browser).open_new_tab(url)

    def open_youtube(self) -> None:
        webbrowser.get(self.browser).open_new_tab(self.youtube_url)
