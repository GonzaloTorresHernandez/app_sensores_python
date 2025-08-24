import json
import os
from dataclasses import dataclass, asdict

@dataclass
class AppSettings:
    serial_port: str = 'COM3'
    baudrate: int = 115200
    theme: str = 'dark'



class SettingsService:

    def __init__(self, path: str = 'settings.json'):
        self._path = path
        self.data = AppSettings()
        self.load()
        

    def load(self) -> None:
        if os.path.exists(self._path):
            with open(self._path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            # Mezcla valores por defecto + lo guardado
            merged = {**asdict(AppSettings()), **raw}
            self.data = AppSettings(**merged)


    def save(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(asdict(self.data), f, indent=2, ensure_ascii=False)