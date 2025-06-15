# coding: ascii
"""
This is a file, sets state for VA
"""

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import logging

logger = logging.getLogger(__name__)


class StateInterface:
    def __init__(self) -> None:
        logger.debug("Initializing StateInterface...")
        devices = AudioUtilities.GetSpeakers()

        if not devices:
            logger.error("Audio device not found.")
            raise RuntimeError("Audio device not found.")

        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self._volume = interface.QueryInterface(IAudioEndpointVolume)

        if self._volume is None:
            logger.error("Failed to obtain volume control interface.")
            raise RuntimeError("Failed to obtain volume control interface.")

        logger.info("StateInterface initialized successfully.")

    def sleep(self) -> None:
        """Sets the master volume level to 0.0 (mute)."""
        logger.info("Muting system volume.")
        self._volume.SetMasterVolumeLevelScalar(0.0, None)

    def wake_up(self, audio_volume: float) -> None:
        """Restores the master volume level."""
        if not (0.0 <= audio_volume <= 1.0):
            logger.warning(f"Ignoring invalid volume level: {audio_volume}.")
            return

        self._volume.SetMasterVolumeLevelScalar(audio_volume, None)
        logger.info(f"Sets the master volume level to: {audio_volume}.")

    def volume_up(self, up_value):
        """Increase the master volume level."""
        current_volume = self._volume.GetMasterVolumeLevelScalar()
        new_volume = current_volume + up_value

        if not (0.0 <= new_volume <= 1.0):
            logger.warning(f"Ignoring invalid volume level: {current_volume + up_value}.")
            return

        self._volume.SetMasterVolumeLevelScalar(new_volume, None)
        logger.info(f"Sets the master volume level to: {new_volume}.")

    def volume_down(self, down_value):
        """Decrease the master volume level."""
        current_volume = self._volume.GetMasterVolumeLevelScalar()
        new_volume = current_volume - down_value

        if not (0.0 <= new_volume):
            logger.warning(f"Ignoring invalid volume level: {current_volume + down_value}.")
            return

        self._volume.SetMasterVolumeLevelScalar(new_volume, None)
        logger.info(f"Sets the master volume level to: {new_volume}.")
