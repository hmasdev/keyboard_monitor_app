from datetime import datetime
from logging import Logger, getLogger
from pynput.keyboard._base import KeyCode

from .models import KeyComboModel, StimulaneousPressedKeysModel


class KeyComboMonitor:
    # NOTE:
    # The definition of a key combo refers to a list of key combinations pressed  # noqa
    # between the state where no keys are pressed and the subsequent state where no keys are pressed again.  # noqa

    def __init__(self, logger: Logger = getLogger(__name__)):
        self.logger = logger
        self.keys: dict[KeyCode, bool] = {}
        self.key_combo: KeyComboModel = KeyComboModel(timestamp=datetime.now(), combo=[])  # noqa

    def activate_key(self, key: KeyCode):
        self.logger.debug(f"Activating key {key}")
        self.keys[key] = True  # update the state of the key
        # record the current pressed keys
        self.key_combo.combo.append(self.get_pressed_keys())

    def deactivate_key(self, key: KeyCode):
        self.logger.debug(f"Deactivating key {key}")
        if key not in self.keys:
            self.logger.warning(f"Deactivating key {key} although {key} is not activated in the current combo")  # noqa
        self.keys[key] = False  # update the state of the key
        if not self.combo_is_active():
            self.logger.debug(f"Key combo {self.key_combo} is not active anymore")  # noqa
            # reset the keycombo when combo is deactivated
            self.key_combo = KeyComboModel(timestamp=datetime.now(), combo=[])  # noqa

    def get_pressed_keys(self) -> StimulaneousPressedKeysModel:
        return StimulaneousPressedKeysModel(
            timestamp=datetime.now(),
            keys=[str(k) for k, v in self.keys.items() if v],
        )

    def combo_is_active(self):
        pressed_keys = self.get_pressed_keys()
        self.logger.debug(f"Pressed keys: {pressed_keys}")
        return len(pressed_keys.keys) > 0
