from keyboard_monitor.keyboard_monitor import KeyboardMonitor


def test_instantiation():
    keyboard_monitor = KeyboardMonitor()
    assert isinstance(keyboard_monitor, KeyboardMonitor)


def test_start(mocker):
    # create mock
    mock_self_listener = mocker.MagicMock()
    mock_keyboard_listener = mocker.patch(
        "keyboard_monitor.keyboard_monitor.keyboard.Listener",
        return_value=mock_self_listener,
    )

    # execute
    keyboard_monitor = KeyboardMonitor()
    keyboard_monitor.start()

    # assert
    mock_keyboard_listener.assert_called_once()
    mock_self_listener.start.assert_called_once()
    mock_self_listener.join.assert_called_once()


def test_end(mocker):
    # create mock
    mock_self_listener = mocker.MagicMock()
    mock_keyboard_listener = mocker.patch(
        "keyboard_monitor.keyboard_monitor.keyboard.Listener",
        return_value=mock_self_listener,
    )

    # executes
    keyboard_monitor = KeyboardMonitor()
    keyboard_monitor.start()
    keyboard_monitor.stop()

    # assert
    mock_keyboard_listener.assert_called_once()
    mock_self_listener.stop.assert_called_once()
