from datetime import datetime
import json
from logging import Logger, getLogger
import os
from typing import Callable


class JsonRecorder:

    def __init__(
        self,
        direc: str = os.path.join(
            os.path.expanduser("~"),
            ".keyboard_monitor",
        ),
        datetime2filename: Callable[[datetime], str] = lambda dt: dt.strftime("%Y%m%d%H.json"),  # noqa
        logger: Logger = getLogger(__name__),
    ):
        self.direc = direc
        self.datetime2filename = datetime2filename
        self.logger = logger

    def get_current_file_path(self) -> str:
        return os.path.join(
            self.direc,
            self.datetime2filename(datetime.now()),
        )

    def record(
        self,
        convertible_to_json: list | dict,
    ):
        self.logger.debug(f"Recording {convertible_to_json}")
        # get path
        path = self.get_current_file_path()
        # create directory if not exists
        os.makedirs(self.direc, exist_ok=True)
        # read the record
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                records = json.load(f)
        else:
            records = []
        # append the record
        records.append(convertible_to_json)
        # write the record
        with open(path, "w", encoding='utf-8') as f:
            json.dump(records, f, indent=4, ensure_ascii=False)
        self.logger.debug(f"Recorded {convertible_to_json} to {path}: {convertible_to_json}")  # noqa
