import yaml
from src.Service.ConfigFileManager import ConfigFileManager


class Configuration:
    # Config keys
    TIMESTAMP_PATTERN = 'timestamp_pattern'
    TIMESTAMP_MIN = 'timestamp_min'
    TIMESTAMP_MAX = 'timestamp_max'
    CLEAR_ON_CHANGE = 'clear_on_change'
    FLASH_ICON_ON_CHANGE = 'flash_icon_on_change'
    CLIPBOARD_POLLING_INTERVAL = 'clipboard_polling_interval'
    FORMAT_ICON = 'format_icon'
    FORMAT_MENU_LAST_TIMESTAMP = 'format_menu_last_timestamp'
    FORMAT_MENU_LAST_DATETIME = 'format_menu_last_datetime'
    FORMAT_MENU_CURRENT_TIMESTAMP = 'format_menu_current_timestamp'
    FORMAT_MENU_CURRENT_DATETIME = 'format_menu_current_datetime'
    DEBUG = 'debug'

    _configFileManager: ConfigFileManager
    _configGlobal: dict
    _configLocal: dict
    _configInitialized = False

    def __init__(self, configFileManager: ConfigFileManager):
        self._configFileManager = configFileManager

    def get(self, key: str):
        self._initializeConfig()

        localValue = self._getFromConfigData(key, self._configLocal)

        if localValue is not None:
            return localValue

        return self._getFromConfigData(key, self._configGlobal)

    def _initializeConfig(self) -> None:
        if self._configInitialized:
            return

        globalConfigContent = self._configFileManager.getGlobalConfigContent()
        self._configGlobal = yaml.load(globalConfigContent, yaml.Loader)

        localConfigContent = self._configFileManager.getLocalConfigContent()
        self._configLocal = yaml.load(localConfigContent, yaml.Loader)

        self._configInitialized = True

    def _getFromConfigData(self, key: str, config: dict):
        if config is None:
            return None

        return config.get(key)
