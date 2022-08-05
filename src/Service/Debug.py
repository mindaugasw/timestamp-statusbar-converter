import time
from src.Service.Configuration import Configuration
import src.events as events


class Debug:
    _config: Configuration
    _debugEnabled: bool

    def __init__(self, config: Configuration):
        self._config = config
        self._debugEnabled = config.get(config.DEBUG)

        events.clipboardChanged.append(lambda content: self.log('Clipboard changed: ' + str(content)))
        events.timestampChanged.append(lambda timestamp: self.log('Timestamp detected: ' + str(timestamp)))

    def log(self, content):
        if self._debugEnabled:
            print(time.strftime('%H:%M:%S:'), content)
