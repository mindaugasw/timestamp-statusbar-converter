import time
from src.Service.Configuration import Configuration
import src.events as events


class Debug:
    _config: Configuration
    _debugEnabled: bool

    def __init__(self, config: Configuration):
        self._config = config
        self._debugEnabled = config.get(config.DEBUG)

        if self._debugEnabled:
            events.clipboardChanged.append(lambda content: self.log('Clipboard changed: ' + str(content)))
            events.timestampChanged.append(lambda timestamp: self.log('Timestamp detected: ' + str(timestamp)))
            events.timestampCleared.append(lambda: self.log('Timestamp cleared'))

    def log(self, content):
        if self._debugEnabled:
            print(time.strftime('%H:%M:%S:'), content)
