from rumps import App, MenuItem
from src.Service.StatusbarApp import StatusbarApp
from src.Service.TimestampTextFormatter import TimestampTextFormatter
import src.events as events


class StatusbarAppMacOs(StatusbarApp):
    _timestampTextFormatter: TimestampTextFormatter

    _rumpsApp: App
    _menuItems: dict[str, MenuItem | None]

    def __init__(self, timestampTextFormatter: TimestampTextFormatter):
        self._timestampTextFormatter = timestampTextFormatter
        events.timestampChanged.append(self._onTimestampChange)

    def createApp(self) -> None:
        self._menuItems = self._createMenuItems()

        self._rumpsApp = App(
            StatusbarApp.APP_NAME,
            None,
            '../assets/icon.png',
            True,
            self._menuItems.values(),
        )
        self._rumpsApp.run()

    def _onTimestampChange(self, timestamp: int) -> None:
        # TODO remove/change
        # if self.rumpsApp is not None:
        niceText = self._timestampTextFormatter.formatForIcon(timestamp)
        self._rumpsApp.title = niceText
        asd = 5  # TODO remove

    def _createMenuItems(self) -> dict[str, MenuItem | None]:
        # TODO is dict needed here? maybe array is enough
        return {
            'click_to_copy_label': MenuItem('Click to copy'),
            'separator_1': None,
            'last_timestamp_label': MenuItem('Last timestamp'),
            'last_timestamp': MenuItem('Last timestamp', self._onClickTime),
            'last_datetime': MenuItem('Last datetime', self._onClickTime),
            'separator_2': None,
            'current_timestamp': MenuItem('Current timestamp', self._onClickTime),
            'current_datetime': MenuItem('Current datetime', self._onClickTime),
            'separator_3': None,
            'edit_config': MenuItem('Edit configuration'), # TODO
            'check_for_updates': MenuItem('Check for updates'), # TODO
            'open_website': MenuItem('Open website'), # TODO
        }

    def _onClickTime(self, item: MenuItem):
        print('Clicked: ' + item.title) # TODO test if item.title changes or is original. If changes, handle timestamp title
        # TODO
        pass
