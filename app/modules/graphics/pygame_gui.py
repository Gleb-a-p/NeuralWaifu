# coding: utf-8
"""
This is module, includes GUI, based on Pygame
"""

import pygame


class MainWindow:
    def __init__(self, name):
        self.name = name

    def show(self):
        pass

    def exec(self):
        run = True

        while run:
            pass


class GUI:
    def __init__(self, lcore, window_sizes):
        self.lcore = lcore
        self.sizes = window_sizes

    def run(self):
        main_window = MainWindow(self.lcore.name)
        main_window.show()
        main_window.exec()
