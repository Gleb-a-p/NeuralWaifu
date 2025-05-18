import webbrowser
import config
import os

os.system(config.GOODBYE_DPI_PATH)

chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
webbrowser.register('Chrome', None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('Chrome').open_new_tab(config.BASE_URL)
# webbrowser.open_new_tab(config.BASE_URL, new=1)