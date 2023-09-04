from datetime import datetime
from pydantic import BaseModel


class StimulaneousPressedKeysModel(BaseModel):
    timestamp: datetime
    keys: list[str]


class KeyComboModel(BaseModel):
    timestamp: datetime
    combo: list[StimulaneousPressedKeysModel]
