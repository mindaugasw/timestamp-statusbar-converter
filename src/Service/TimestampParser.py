import re
import src.events as events
from src.Service import Configuration
from src.Service.Debug import Debug


class TimestampParser:
    _debug: Debug
    _pattern: str
    _minValue: int
    _maxValue: int
    _clearOnChange: bool
    _timestampSet = False
    _skipTimestamp = None

    def __init__(self, config: Configuration, debug: Debug):
        self._debug = debug

        self._pattern = config.get(config.TIMESTAMP_PATTERN)
        self._minValue = config.get(config.TIMESTAMP_MIN)
        self._maxValue = config.get(config.TIMESTAMP_MAX)
        self._clearOnChange = config.get(config.CLEAR_ON_CHANGE)

        events.clipboardChanged.append(self._process)
        events.timestampChanged.append(lambda timestamp: self._setTimestampSet(True))
        events.timestampCleared.append(lambda: self._setTimestampSet(False))

    def skipNextTimestamp(self, timestamp: str) -> None:
        """Set next expected timestamp value that should be ignored and not parsed

        Can be used to intentionally ignore timestamp when it was set by the
        application itself
        """

        self._skipTimestamp = timestamp

    def _process(self, content: str) -> None:
        if self._skipTimestamp == content:
            self._skipTimestamp = None
            return

        timestamp = self._extractTimestamp(content)

        if timestamp is False:
            if self._clearOnChange and self._timestampSet:
                events.timestampCleared()

            return

        events.timestampChanged(timestamp)

    def _extractTimestamp(self, content: str) -> int | bool:
        """
        Returns:
             Timestamp as integer, or False if no valid timestamp was found
        """

        content = content.strip()
        regexResult = re.match(self._pattern, content)

        if regexResult is None:
            return False

        try:
            number = int(content)
        except Exception as e:
            self._debug.log(
                f'Exception occurred while converting copied text to integer.\n'
                f'Copied content: {content}\n'
                f'Exception: {type(e)}\n'
                f'Exception message: {str(e)}'
            )
            return False

        if number < self._minValue or number > self._maxValue:
            return False

        return number

    def _setTimestampSet(self, timestampSet: bool) -> None:
        self._timestampSet = timestampSet
