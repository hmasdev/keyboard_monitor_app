from copy import deepcopy
from datetime import datetime as dt
import os
from unittest.mock import call

import pytest

from keyboard_monitor.recorder import JsonRecorder


def test_instance():
    recorder = JsonRecorder()
    assert isinstance(recorder, JsonRecorder)


def test_get_current_file_path(mocker):

    # setup
    expected = "/home/user/.keyboard_monitor/20210102030405.json"
    direc = os.path.dirname(expected)
    filename = os.path.basename(expected)

    # make mock
    mock_datetime_datetime = mocker.patch("keyboard_monitor.recorder.datetime")  # noqa
    mock_datetime_datetime.now.return_value = dt.strptime(filename, "%Y%m%d%H%M%S.json")  # noqa

    # exceute
    actual = JsonRecorder(
        direc=direc,
        datetime2filename=lambda x: x.strftime("%Y%m%d%H%M%S.json"),
    ).get_current_file_path()

    # assert
    assert actual == expected
    mock_datetime_datetime.now.assert_called_once()


@pytest.mark.parametrize(
    "os_path_exist_return",
    [
        True,
        False,
    ]
)
def test_record(
    os_path_exist_return,
    mocker,
):

    # setup
    expected = "/home/user/.keyboard_monitor/20210102030405.json"
    direc = os.path.dirname(expected)
    filename = os.path.basename(expected)

    # input
    current_records = [{"a": 2}] if os_path_exist_return else []
    input_record = {"a": 1}

    # make mock
    mock_datetime_datetime = mocker.patch("keyboard_monitor.recorder.datetime")  # noqa
    mock_datetime_datetime.now.return_value = dt.strptime(filename, "%Y%m%d%H%M%S.json")  # noqa
    mock_os_makedirs = mocker.patch("os.makedirs")
    mock_os_path_exists = mocker.patch(
        "os.path.exists",
        return_value=os_path_exist_return,
    )
    mock_open = mocker.patch("builtins.open")
    mock_json_load = mocker.patch(
        "json.load",
        return_value=deepcopy(current_records),
    )
    mock_json_dump = mocker.patch("json.dump")

    # exceute
    JsonRecorder(
        direc=direc,
        datetime2filename=lambda x: x.strftime("%Y%m%d%H%M%S.json"),
    ).record(input_record)

    # assert
    mock_datetime_datetime.now.assert_called_once()
    mock_os_makedirs.assert_called_once_with(direc, exist_ok=True)
    mock_os_path_exists.assert_called_once_with(expected)
    if os_path_exist_return:
        mock_json_load.assert_called_once()
        mock_open.call_count == 2
        assert call(expected, "r", encoding="utf-8") in mock_open.call_args_list  # noqa
        assert call(expected, "w", encoding="utf-8") in mock_open.call_args_list  # noqa
    else:
        mock_json_load.assert_not_called()
        mock_open.assert_called_once_with(expected, "w", encoding="utf-8")
    assert mock_json_dump.call_args_list[0][0][0] == current_records + [input_record]  # noqa
