class Timestamp:
    seconds: int
    milliseconds: int | None

    def __init__(self, seconds: int, milliseconds: int | None = None):
        self.seconds = seconds
        self.milliseconds = milliseconds

    def __str__(self) -> str:
        return self.getStringPretty()

    def getStringPretty(self) -> str:
        """Get timestamp with milliseconds separated for better readability"""

        return self._getString('.')

    def getStringValid(self) -> str:
        """Get valid timestamp, without milliseconds separation"""

        return self._getString('')

    def _getString(self, msSeparator: str) -> str:
        if self.milliseconds is None:
            return str(self.seconds)
        else:
            return '%d%s%03d' % (self.seconds, msSeparator, self.milliseconds)
