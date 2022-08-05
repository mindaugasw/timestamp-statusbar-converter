import re
import src.events as events
from src.Service import Configuration
from src.Service.Debug import Debug


class TimestampParser:
    _debug: Debug

    _pattern: str
    _minValue: int
    _maxValue: int

    def __init__(self, config: Configuration, debug: Debug):
        self._debug = debug

        self._pattern = config.get(config.TIMESTAMP_PATTERN)
        self._minValue = config.get(config.TIMESTAMP_MIN)
        self._maxValue = config.get(config.TIMESTAMP_MAX)

        events.clipboardChanged.append(self.parse)

    def parse(self, content: str) -> None:
        content = content.strip()
        regexResult = re.match(self._pattern, content)

        if regexResult is None:
            return

        try:
            number = int(content)
        except Exception as e:
            self._debug.log(
                f'Exception occurred while casting copied text to int.\n'
                f'Copied content: {content}\n'
                f'Exception: {type(e)}\n'
                f'Exception message: {str(e)}'
            )
            return

        if number < self._minValue or number > self._maxValue:
            return

        events.timestampChanged(number)
