# coding: utf-8

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


def sleep():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )
    volume = interface.QueryInterface(
        IAudioEndpointVolume
    )
    volume.SetMasterVolumeLevelScalar(0, None)
