import os
import subprocess
import sys
import threading
import time
from rumps import App, MenuItem, rumps
from src.Service.ClipboardManager import ClipboardManager
from src.Service.ConfigFileManager import ConfigFileManager
from src.Service.Configuration import Configuration
from src.Service.StatusbarApp import StatusbarApp
from src.Service.TimestampParser import TimestampParser
from src.Service.TimestampTextFormatter import TimestampTextFormatter
import src.events as events
from src.Entity.Timestamp import Timestamp


class StatusbarAppMacOs(StatusbarApp):
    WEBSITE = 'https://github.com/mindaugasw/timestamp-statusbar-converter'
    ICON_DEFAULT = '../assets/icon.png'
    ICON_FLASH = '../assets/icon_flash.png'
    ICON_FLASH_DURATION = 0.35

    _formatter: TimestampTextFormatter
    _clipboard: ClipboardManager
    _timestampParser: TimestampParser
    _configFileManager: ConfigFileManager
    _rumpsApp: App

    _menuItems: dict[str, MenuItem | None]
    _formatLastTimestamp: str
    _formatLastDatetime: str
    _formatCurrentTimestamp: str
    _formatCurrentDatetime: str
    _flashIconOnChange: bool

    def __init__(
        self,
        formatter: TimestampTextFormatter,
        clipboard: ClipboardManager,
        timestampParser: TimestampParser,
        config: Configuration,
        configFileManager: ConfigFileManager,
    ):
        self._formatter = formatter
        self._clipboard = clipboard
        self._timestampParser = timestampParser
        self._configFileManager = configFileManager

        self._formatLastTimestamp = config.get(config.FORMAT_MENU_LAST_TIMESTAMP)
        self._formatLastDatetime = config.get(config.FORMAT_MENU_LAST_DATETIME)
        self._formatCurrentTimestamp = config.get(config.FORMAT_MENU_CURRENT_TIMESTAMP)
        self._formatCurrentDatetime = config.get(config.FORMAT_MENU_CURRENT_DATETIME)
        self._flashIconOnChange = config.get(config.FLASH_ICON_ON_CHANGE)

        events.timestampChanged.append(self._onTimestampChange)
        events.timestampCleared.append(self._onTimestampClear)

    def createApp(self) -> None:
        self._menuItems = self._createMenuItems()
        self._rumpsApp = App(
            StatusbarApp.APP_NAME,
            None,
            self.ICON_DEFAULT,
            True,
            self._menuItems.values(),
        )
        self._rumpsApp.run()

    def _createMenuItems(self) -> dict[str, MenuItem | None]:
        lastTimestamp = Timestamp(int(time.time()))

        return {
            # Items without callback are disabled and act as informational labels
            'last_timestamp_label': MenuItem('Last timestamp - click to copy'),
            'last_timestamp': MenuItem(
                self._getLastTimestampText(lastTimestamp),
                self._onMenuClickLastTime,
            ),
            'last_datetime': MenuItem(
                self._getLastDatetimeText(lastTimestamp),
                self._onMenuClickLastTime,
            ),
            'separator_1': None,
            'current_timestamp_label': MenuItem('Current timestamp - click to copy'),
            'current_timestamp': MenuItem('Current timestamp', self._onMenuClickCurrentTime),
            'current_datetime': MenuItem('Current datetime', self._onMenuClickCurrentTime),
            'separator_2': None,
            'clear_timestamp': MenuItem('Clear timestamp', self._onMenuClickClearTimestamp),
            'edit_config': MenuItem('Edit configuration', self._onMenuClickEditConfiguration),
            'check_for_updates': MenuItem('Check for updates'),  # TODO
            'open_website': MenuItem('Open website', self._onMenuClickOpenWebsite),
            'restart': MenuItem('Restart application', self._onMenuClickRestart),
        }

    def _getLastTimestampText(self, timestamp: Timestamp) -> str:
        return self._formatter.format(timestamp, self._formatLastTimestamp)

    def _getLastDatetimeText(self, timestamp: Timestamp) -> str:
        return self._formatter.format(timestamp, self._formatLastDatetime)

    def _onTimestampChange(self, timestamp: Timestamp) -> None:
        self._rumpsApp.title = self._formatter.formatForIcon(timestamp)
        self._menuItems['last_timestamp'].title = self._getLastTimestampText(timestamp)
        self._menuItems['last_datetime'].title = self._getLastDatetimeText(timestamp)

        if self._flashIconOnChange:
            threading.Thread(target=self._flashIcon).start()

    def _onTimestampClear(self) -> None:
        self._rumpsApp.title = None

    def _onMenuClickLastTime(self, item: MenuItem) -> None:
        self._clipboard.setClipboardContent(item.title)

    def _onMenuClickCurrentTime(self, item: MenuItem) -> None:
        template: str

        if item is self._menuItems['current_timestamp']:
            template = self._formatCurrentTimestamp
        else:
            template = self._formatCurrentDatetime

        text = self._formatter.format(int(time.time()), template)
        self._timestampParser.skipNextTimestamp(text)
        self._clipboard.setClipboardContent(text)

    def _onMenuClickClearTimestamp(self, item: MenuItem) -> None:
        events.timestampCleared()

    def _onMenuClickEditConfiguration(self, item: MenuItem) -> None:
        configFilePath = self._configFileManager.getLocalConfigFullPath()

        alertResult = rumps.alert(
            'Edit configuration',
            f'Configuration can be edited in the file: \n{configFilePath}\n\n'
            'After editing, the application must be restarted.\n\n'
            'All supported configuration can be found at:\n'
            'https://github.com/mindaugasw/timestamp-statusbar-converter/blob/master/config.yml',
            'Open in default editor',
            'Close',
        )

        if alertResult == 1:
            subprocess.Popen(['open', configFilePath])

    def _onMenuClickOpenWebsite(self, item: MenuItem) -> None:
        subprocess.Popen(['open', self.WEBSITE])
        # TODO use xdg-open on Linux
        # https://stackoverflow.com/a/4217323/4110469

    def _onMenuClickRestart(self, item: MenuItem) -> None:
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    def _flashIcon(self) -> None:
        self._rumpsApp.icon = self.ICON_FLASH
        time.sleep(self.ICON_FLASH_DURATION)
        self._rumpsApp.icon = self.ICON_DEFAULT
