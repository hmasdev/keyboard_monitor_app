# Keyboard Monitor App: Python Application to Monitor Your Keyboard

![GitHub top language](https://img.shields.io/github/languages/top/hmasdev/keyboard_monitor_app)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hmasdev/keyboard_monitor_app?sort=semver)
![GitHub](https://img.shields.io/github/license/hmasdev/keyboard_monitor_app)
![GitHub last commit](https://img.shields.io/github/last-commit/hmasdev/keyboard_monitor_app)

Keyboard Monitor App is a Python package that allows monitoring and recording key combinations pressed on the keyboard. It uses the pynput library to listen for keyboard events.

CAUTION: **DO NOT USE THIS APPLICATION TO MONITOR OTHERS' KEYBOARD INPUT**!

## Installation

To install Keyboard Monitor App, use pip:

```shell
pip install git+https://github.com/hmasdev/keyboard_monitor_app.git
```

## Usage

Keyboard Monitor App can be used to monitor and record key combinations pressed on your keyboard. The recorded data can be saved as JSON files.

### Simple Case

If you just want to record your keyboard input, you can run the following command:

```bash
python -m keyboard_monitor
```

You can specify some options:

```bash
python -m keyboard_monitor --record-dir ${PATH_TO_DIREC_WHERE_YOU_WANT_TO_SAVE_RECORDS} --record-filename ${FILENAME_FORMAT_FOR_RECORDS} --log-level {LOG_LEVEL}
```

- `--record-dir`:

  path to the directory where you want to save records from your keyboard;

- `--record-filename`:

  format of filenames of records which depend on `datetime` objects. For example, you can specify "%Y%m%d%H%M%S.json". Note that

  1. this option also indicates how often to create a new file to record;
  2. this option must end with the ".json";

- `--log-level`:

  logging level. You can specify the following levels:

  - `CRITICAL`
  - `ERROR`
  - `WARNING`
  - `INFO`
  - `DEBUG`

You can see the details of the optional arguments from the command line:

```bash
python -m keyboard_monitor --help
```

### Use `keyboard_monitor` in python codes

You can also use this application in your python codes.
Here are 2 examples.

- Simpler example:

```python
# import
from keyboard_monitor.main import main as keyboard_monitor_main

# run
keyboard_monitor_main(
    record_dir='PATH TO DIREC',
    record_filename='FILENAME FORMAT LIKE %Y%m%d%H%M%S',
    log_level='INFO',
)
```

- Complex exampe:

```python
# import
from copy import deepcopy
from datetime import datetime
from keyboard_monitor.key_combo_monitor import KeyComboMonitor
from keyboard_monitor.keyboard_monitor import KeyboardMonitor
from keyboard_monitor.recorder import JsonRecorder

# create key combo monitor
key_combo_monitor = KeyComboMonitor()

# create recorder
recorder = JsonRecorder(
    direc="PATH2DIREC",
    datetime2filename=lambda dt: dt.strftime("FILENAME FORMAT %Y%m%d"),
)

# create callback
def on_press_callback(key):
    key_combo_monitor.activate_key(key)

def on_release_callback(key):
    combo = deepcopy(key_combo_monitor.key_combo)
    key_combo_monitor.deactivate_key(key)
    if not key_combo_monitor.combo_is_active():
        recorder.record({
            "timestamp": datetime.now().isoformat(),
            "combo": [[str(k) for k in c] for c in combo]
        })

# create keyboard monitor
keyboard_monitor = KeyboardMonitor(
    on_press_callback=on_press_callback,
    on_release_callback=on_release_callback,
)

# run
keyboard_monitor.start()

######

# stop
keyboard_monitor.stop()
```

## Format of Record Keys

Recorded keys are output to a JSON file in the specified directory.

The format of contents of the JSON file is as follows:

```json
[
    {
        "timestamp": "%Y-%m-%dT%H:%M:%S.%f",
        "combo": [
            ["KEY1"],
            ["KEY1", "KEY2"],
            ...
        ]
    },
    ...
]
```

NOTE: The definition of a key combo refers to a list of key combinations pressed between the state where no keys are pressed and the subsequent state where no keys are pressed again. For example, `[["KEY1"],["KEY1", "KEY2"],["KEY1"]]` describe tapping "KEY2" with "KEY1" held.

## LICENSE

Keyboard Monitor is licensed under the [MIT](https://github.com/hmasdev/keyboard_monitor_app/tree/main/LICENSE) License. See the LICENSE file for more details.

## Authors

[hmasdev](https://github.com/hmasdev)
