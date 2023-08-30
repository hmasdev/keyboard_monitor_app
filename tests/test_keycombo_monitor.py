from keyboard_monitor.key_combo_monitor import KeyComboMonitor


def test_instantiation():
    key_combo_monitor = KeyComboMonitor()
    assert isinstance(key_combo_monitor, KeyComboMonitor)


def test_activate_key():
    key_combo_monitor = KeyComboMonitor()
    key_combo_monitor.activate_key("a")
    assert key_combo_monitor.keys["a"] is True
    assert key_combo_monitor.key_combo == [["a"]]
    key_combo_monitor.activate_key("b")
    assert key_combo_monitor.keys["a"] is True
    assert key_combo_monitor.keys["b"] is True
    assert key_combo_monitor.key_combo == [["a"], ["a", "b"]]


def test_deactivate_key():
    key_combo_monitor = KeyComboMonitor()
    key_combo_monitor.activate_key("a")
    key_combo_monitor.deactivate_key("a")
    assert key_combo_monitor.keys["a"] is False
    assert key_combo_monitor.key_combo == []

    key_combo_monitor.deactivate_key("b")
    assert key_combo_monitor.keys["b"] is False
    assert key_combo_monitor.key_combo == []
    # TODO: test warning log


def test_get_pressed_keys():
    key_combo_monitor = KeyComboMonitor()
    key_combo_monitor.activate_key("a")
    key_combo_monitor.activate_key("b")
    assert key_combo_monitor.get_pressed_keys() == ["a", "b"]
    key_combo_monitor.deactivate_key("a")
    assert key_combo_monitor.get_pressed_keys() == ["b"]


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
