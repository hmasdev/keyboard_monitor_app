from logging import Logger, getLogger
from typing import Callable
from pynput import keyboard
from pynput.keyboard._base import KeyCode


class KeyboardMonitor:

    def __init__(
        self,
        on_press_callback: Callable[[KeyCode], None] = lambda key: print(f"Pressed {key}"),  # noqa
        on_release_callback: Callable[[KeyCode], None] = lambda key: print(f"Released {key}"),  # noqa
        logger: Logger = getLogger(__name__)
    ):
        self._on_press_callback = on_press_callback
        self._on_release_callback = on_release_callback
        self.logger = logger

    def start(self):
        self.listener = keyboard.Listener(
            on_press=self._on_press_callback,
            on_release=self._on_release_callback,
        )
        self.listener.start()
        self.listener.join()
        return self

    def stop(self):
        self.listener.stop()
