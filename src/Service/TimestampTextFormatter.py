import datetime
import time
from src.Service.Configuration import Configuration


class TimestampTextFormatter:
    # _iconFormat: str | None = None
    _iconFormats: dict[int, str]

    def __init__(self, config: Configuration):
        # self._iconFormat = config.get(config.FORMAT_ICON)
        self._iconFormats = config.get(config.ICON_FORMATS)

    # Supports all standard strftime() formats and additional custom formats:
    # TODO update documentation
    # {ts} - unix timestamp, e.g. 1658655236
    # %r - relative time, e.g. '5.5 min ago', 'in 3.2 months'
    # TODO add method _formatInternal, while this shouldn't have relativeTimeData param?
    def format(self, timestamp: int, formatTemplate: str, relativeTimeData: dict) -> str:
        formatted = formatTemplate.format(
            ts=str(timestamp),
            r_in='' if relativeTimeData['past'] else 'in ',
            r_ago=' ago' if relativeTimeData['past'] else '',
            r_float='%.1f' % relativeTimeData['number'],
            r_int=int(relativeTimeData['number']),
            r_unit=relativeTimeData['unit'],
        )

        dateTime = datetime.datetime.fromtimestamp(timestamp)
        formatted = dateTime.strftime(formatted)

        # TODO inline return
        return formatted

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

        # [time amount (e.g. 5.5), unit (e.g. 'months'), is past time?]
        config: tuple[float, str, bool]

        if diff < 60:
            # up to 60 seconds, return seconds
            return {'diff': diff, 'number': float(diff), 'unit': 's', 'past': isPastTime}
        elif diff < 3600:
            # up to 60 minutes
            return {'diff': diff, 'number': diff / 60.0, 'unit': 'min', 'past': isPastTime}
        elif diff < 86400:
            # up to 24 hours
            return {'diff': diff, 'number': diff / 3600.0, 'unit': 'h', 'past': isPastTime}
        elif diff < 2678400:
            # up to 31 days
            return {'diff': diff, 'number': diff / 86400.0, 'unit': 'd', 'past': isPastTime}
        elif diff < 31536000:
            # up to 365 days
            return {'diff': diff, 'number': diff / 2678400.0, 'unit': 'months', 'past': isPastTime}
        else:
            return {'diff': diff, 'number': diff / 31536000.0, 'unit': 'years', 'past': isPastTime}

    # Format timestamp for main icon, according to user config
    def formatForIcon(self, timestamp: int) -> str:
        # if self._iconFormat is None:
        #     self._iconFormat = services.config.get(services.config.FORMAT_ICON)

        timeData = self._getRelativeTimeData(timestamp)
        formatTemplate: str | None = None

        for key, template in self._iconFormats.items():
            if key == 'default' or int(key) > timeData['diff']:
                formatTemplate = template
                break

        if formatTemplate is None:
            raise Exception('No suitable format found for timestamp: ' + str(timestamp))

        # TODO inline
        formatted = self.format(timestamp, formatTemplate, timeData)

        return formatted
