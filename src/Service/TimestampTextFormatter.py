import datetime
import time
from src.Service.Configuration import Configuration


class TimestampTextFormatter:
    _iconFormats: dict[int, str]

    def __init__(self, config: Configuration):
        self._iconFormats = config.get(config.FORMAT_ICON)

    def format(self, timestamp: int, template: str) -> str:
        return self._formatInternal(timestamp, template, self._getRelativeTimeData(timestamp))

    def formatForIcon(self, timestamp: int) -> str:
        """Format timestamp for main icon, according to user config"""

        timeData = self._getRelativeTimeData(timestamp)
        formatTemplate: str | None = None

        for key, template in self._iconFormats.items():
            if key == 'default' or int(key) > timeData['diff']:
                formatTemplate = template
                break

        if formatTemplate is None:
            raise Exception('No suitable format found for timestamp: ' + str(timestamp))

        return self._formatInternal(timestamp, formatTemplate, timeData)

    def _formatInternal(self, timestamp: int, template: str, relativeTimeData: dict) -> str:
        """Format timestamp with relative time support

        Formatter supports all standard strftime() codes:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        and these custom codes to for relative time:
        - {ts} - unix timestamp.
        - {r_int} - relative time with integer number, e.g. '5 h ago'.
        - {r_float} - relative time with float number, e.g. '5.5 h ago'.
        """

        relativeFormatArguments = (
            '' if relativeTimeData['past'] else 'in ',
            relativeTimeData['number'],
            relativeTimeData['unit'],
            ' ago' if relativeTimeData['past'] else '',
        )

        formatted = template.format(
            ts=str(timestamp),
            r_int='%s%d %s%s' % relativeFormatArguments,
            r_float='%s%.1f %s%s' % relativeFormatArguments,
        )

        dateTime = datetime.datetime.fromtimestamp(timestamp)

        return dateTime.strftime(formatted)

    def _getRelativeTimeData(self, timestamp: int) -> dict[str, float | str | bool]:
        """
        Returns:
            Dictionary with the following keys:
            - diff: int, absolute difference in seconds between given timestamp and now
            - number: float, relative time amount, e.g. 5.5
            - unit: str, relative time unit, e.g. 'd'
            - past: bool, if timestamp is in the past or in the future
        """

        currentTimestamp = int(time.time())
        diff = abs(currentTimestamp - timestamp)
        isPastTime = currentTimestamp > timestamp

        data = {'diff': diff, 'past': isPastTime}

        if diff < 60:
            # up to 60 seconds, return seconds
            data.update({'number': float(diff), 'unit': 's'})
        elif diff < 3600:
            # up to 60 minutes
            data.update({'number': diff / 60.0, 'unit': 'min'})
        elif diff < 86400:
            # up to 24 hours
            data.update({'number': diff / 3600.0, 'unit': 'h'})
        elif diff < 2678400:
            # up to 31 days
            data.update({'number': diff / 86400.0, 'unit': 'days'})
        elif diff < 31536000:
            # up to 365 days
            data.update({'number': diff / 2678400.0, 'unit': 'months'})
        else:
            data.update({'number': diff / 31536000.0, 'unit': 'years'})

        return data
