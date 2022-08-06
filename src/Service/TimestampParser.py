import random
import re
import threading
import time
import src.events as events
from src.Service import Configuration
from src.Service.Debug import Debug


class TimestampParser:
    CLEARING_THREAD_SLEEP_INTERVAL = 5

    _debug: Debug
    _pattern: str
    _minValue: int
    _maxValue: int
    _clearOnChange: bool
    _clearAfterTime: int
    _lastTimestampId: int
    _timestampSet = False
    _skipTimestamp = None

    def __init__(self, config: Configuration, debug: Debug):
        self._debug = debug

        self._pattern = config.get(config.TIMESTAMP_PATTERN)
        self._minValue = config.get(config.TIMESTAMP_MIN)
        self._maxValue = config.get(config.TIMESTAMP_MAX)
        self._clearOnChange = config.get(config.CLEAR_ON_CHANGE)
        self._clearAfterTime = config.get(config.CLEAR_AFTER_TIME)

        events.clipboardChanged.append(self._process)
        events.timestampChanged.append(lambda timestamp: self._onTimestampChanged())
        events.timestampCleared.append(lambda: self._onTimestampCleared())

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

    def _onTimestampChanged(self) -> None:
        self._timestampSet = True

        if self._clearAfterTime > 0:
            self._lastTimestampId = random.randint(0, 99999)
            threading.Thread(target=self._clearTimestampAfterTime).start()

    def _onTimestampCleared(self) -> None:
        self._timestampSet = False

    def _clearTimestampAfterTime(self) -> None:
        # This is used as a stop flag - if _lastTimestampId changes during
        # thread's lifetime, that means timestamp has updated and this thread
        # should exit without clearing new timestamp - a new thread was created
        # for that with new countdown
        initialTimestampId = self._lastTimestampId
        threadStartedAt = int(time.time())
        self._debug.log(f'Auto clear - starting thread #{initialTimestampId}')

        while int(time.time()) - threadStartedAt < self._clearAfterTime:
            time.sleep(self.CLEARING_THREAD_SLEEP_INTERVAL)

            if initialTimestampId != self._lastTimestampId:
                self._debug.log(f'Auto clear - timestamp changed, exiting thread #{initialTimestampId}')
                return

        self._debug.log(f'Auto clear - clearing timestamp #{initialTimestampId}')
        events.timestampCleared()
