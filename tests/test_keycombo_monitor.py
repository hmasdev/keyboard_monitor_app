from datetime import datetime as dt
from keyboard_monitor.models import KeyComboModel, StimulaneousPressedKeysModel
from keyboard_monitor.key_combo_monitor import KeyComboMonitor


def test_instantiation():
    key_combo_monitor = KeyComboMonitor()
    assert isinstance(key_combo_monitor, KeyComboMonitor)


def test_activate_key(mocker):

    # preparation
    timestamp = dt(2021, 1, 2, 3, 4, 5, 6)
    mock_datetime = mocker.patch('keyboard_monitor.key_combo_monitor.datetime')  # noqa
    mock_datetime.now.return_value = timestamp

    # test
    key_combo_monitor = KeyComboMonitor()
    key_combo_monitor.activate_key("a")
    assert key_combo_monitor.keys["a"] is True
    assert key_combo_monitor.key_combo == KeyComboModel(
        timestamp=timestamp,
        combo=[StimulaneousPressedKeysModel(timestamp=timestamp, keys=["a"])],  # noqa
    )
    key_combo_monitor.activate_key("b")
    assert key_combo_monitor.keys["a"] is True
    assert key_combo_monitor.keys["b"] is True
    assert key_combo_monitor.key_combo == KeyComboModel(
        timestamp=timestamp,
        combo=[
            StimulaneousPressedKeysModel(timestamp=timestamp, keys=["a"]),  # noqa
            StimulaneousPressedKeysModel(timestamp=timestamp, keys=["a", "b"]),  # noqa
        ]
    )


def test_deactivate_key(mocker):

    # preparation
    timestamp = dt(2021, 1, 2, 3, 4, 5, 6)
    mock_datetime = mocker.patch('keyboard_monitor.key_combo_monitor.datetime')  # noqa
    mock_datetime.now.return_value = timestamp

    # test
    key_combo_monitor = KeyComboMonitor()
    key_combo_monitor.activate_key("a")
    key_combo_monitor.deactivate_key("a")
    assert key_combo_monitor.keys["a"] is False
    assert key_combo_monitor.key_combo == KeyComboModel(
        timestamp=timestamp,
        combo=[],
    )

    key_combo_monitor.deactivate_key("b")
    assert key_combo_monitor.keys["b"] is False
    assert key_combo_monitor.key_combo == KeyComboModel(
        timestamp=timestamp,
        combo=[],
    )
    # TODO: test warning log


def test_get_pressed_keys(mocker):

    # preparation
    timestamp = dt(2021, 1, 2, 3, 4, 5, 16)
    mock_datetime = mocker.patch('keyboard_monitor.key_combo_monitor.datetime')  # noqa
    mock_datetime.now.return_value = timestamp

    key_combo_monitor = KeyComboMonitor()
    key_combo_monitor.activate_key("a")
    key_combo_monitor.activate_key("b")
    assert key_combo_monitor.get_pressed_keys() == StimulaneousPressedKeysModel(  # noqa
        timestamp=timestamp,
        keys=["a", "b"],
    )
    key_combo_monitor.deactivate_key("a")
    assert key_combo_monitor.get_pressed_keys() == StimulaneousPressedKeysModel(  # noqa
        timestamp=timestamp,
        keys=["b"],
    )


def test_combo_is_active():
    key_combo_monitor = KeyComboMonitor()
    assert key_combo_monitor.combo_is_active() is False
    key_combo_monitor.activate_key("a")
    assert key_combo_monitor.combo_is_active() is True
    key_combo_monitor.deactivate_key("a")
    assert key_combo_monitor.combo_is_active() is False
    key_combo_monitor.activate_key("a")
    key_combo_monitor.activate_key("b")
    assert key_combo_monitor.combo_is_active() is True
    key_combo_monitor.deactivate_key("a")
    assert key_combo_monitor.combo_is_active() is True
    key_combo_monitor.deactivate_key("b")
    assert key_combo_monitor.combo_is_active() is False
