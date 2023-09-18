import time
import sys
from src.Service.Configuration import Configuration
import src.events as events


class Debug:
    _debugEnabled: bool

    def __init__(self, config: Configuration):
        self._debugEnabled = config.get(config.DEBUG) or '--debug' in sys.argv

        if self._debugEnabled:
            events.clipboardChanged.append(lambda content: self.log('Clipboard changed: ' + str(content)))
            events.timestampChanged.append(lambda timestamp: self.log('Timestamp detected: ' + str(timestamp)))
            events.timestampClear.append(lambda: self.log('Timestamp cleared'))

    def log(self, content) -> None:
        if self._debugEnabled:
            print(time.strftime('%H:%M:%S:'), content)

    def isDebugEnabled(self) -> bool:
        return self._debugEnabled
