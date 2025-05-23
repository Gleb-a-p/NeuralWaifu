# coding: utf-8

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

import app.modules.core.logic.config as config


def wake_up():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMasterVolumeLevelScalar(config.BASE_VOLUME, None)
