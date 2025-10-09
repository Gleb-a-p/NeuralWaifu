# coding: utf-8
"""
This is config, includes list of plugins
"""


required_modules = {
    "Core": "NeuralWaifu/app/modules/core/logic/logic_interface.py",
    "GUI": "NeuralWaifu/app/modules/graphics/gui.py",
    "Audio": "NeuralWaifu/app/modules/audio/audio_interface.py",
    "System": "NeuralWaifu/app/modules/windows/system_interface.py",
    "State": "NeuralWaifu/app/modules/core/state_interface.py",
    "Keys": "NeuralWaifu/app/etc/config.ini",
    "General": "NeuralWaifu/app/modules/core/logic/general_config.py",
    "Roles": "NeuralWaifu/app/modules/core/roles/"
}

plugins = {}
