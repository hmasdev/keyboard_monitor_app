from datetime import datetime
from logging import getLogger, basicConfig
import os

import click

from .key_combo_monitor import KeyComboMonitor
from .keyboard_monitor import KeyboardMonitor
from .recorder import JsonRecorder


HOME_DIR = os.path.expanduser("~")
DEFAULT_RECORD_DIR = os.path.join(HOME_DIR, ".keyboard_monitor")
DEFAULT_RECORD_FILENAME = "%Y%m%d%H.json"


@click.command()
@click.option("--record-dir", default=DEFAULT_RECORD_DIR, help=f"directory to save the records. Defaults to {DEFAULT_RECORD_DIR}")  # noqa
@click.option("--record-filename", default=DEFAULT_RECORD_FILENAME, help=f"datetime format of the filename to save the records. Defaults to {DEFAULT_RECORD_FILENAME}")  # noqa
@click.option("--log-level", default="INFO")
def cli(record_dir, record_filename, log_level):
    main(
        record_dir=record_dir,
        record_filename=record_filename,
        log_level=log_level,
    )


def main(
    record_dir: str = DEFAULT_RECORD_DIR,
    record_filename: str = DEFAULT_RECORD_FILENAME,
    log_level: str = "INFO",
) -> KeyboardMonitor:

    # setup
    ###########################################################
    # create logger
    basicConfig(level=log_level)
    logger = getLogger(__name__)
    # create recorder
    recorder = JsonRecorder(
        direc=record_dir,
        datetime2filename=lambda dt: dt.strftime(record_filename),
    )
    # create key combo monitor
    key_combo_monitor = KeyComboMonitor()
    # create callback

    def on_press_callback(key):
        key_combo_monitor.activate_key(key)
        logger.debug(f"{key} pressed")

    def on_release_callback(key):
        combo = key_combo_monitor.key_combo
        key_combo_monitor.deactivate_key(key)
        if not key_combo_monitor.combo_is_active():
            recorder.record({
                "timestamp": datetime.now().isoformat(),
                "combo": [
                    {
                        "timestamp": c.timestamp.isoformat(),
                        "keys": [str(k) for k in c.keys],
                    }
                    for c in combo.combo
                ],
            })

    # create keyboard monitor
    keyboard_monitor = KeyboardMonitor(
        on_press_callback=on_press_callback,
        on_release_callback=on_release_callback,
    )

    # start
    ###########################################################
    return keyboard_monitor.start()


if __name__ == "__main__":
    cli()
