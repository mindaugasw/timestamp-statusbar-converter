import yaml
from src.Service.ConfigFileManager import ConfigFileManager


class Configuration:
    # Config keys
    # TIMESTAMP_PATTERN = ['timestamp_parsing', 'pattern']
    TIMESTAMP_PATTERN = ['timestamp_pattern']
    TIMESTAMP_MIN = ['timestamp_min']
    TIMESTAMP_MAX = ['timestamp_max']
    CLIPBOARD_POLLING_INTERVAL = ['clipboard_polling_interval']

    # FORMAT_ICON = ['formatting', 'icon_format']
    ICON_FORMATS = ['format_icon', 'icon_formats']
    DEBUG_ENABLED = ['debug']

    _configFileManager: ConfigFileManager

    _configGlobal: dict
    _configLocal: dict
    _configInitialized = False

    def __init__(self, configFileManager: ConfigFileManager):
        self._configFileManager = configFileManager

    def get(self, key: list):
        self._initializeConfig()

        localValue = self._getFromConfigData(key, self._configLocal)

        if localValue is not None:
            return localValue

        # TODO inline return
        globalVal = self._getFromConfigData(key, self._configGlobal)
        return globalVal

    def _initializeConfig(self) -> None:
        if self._configInitialized:
            return

        globalConfigContent = self._configFileManager.getGlobalConfigContent()
        self._configGlobal = yaml.load(globalConfigContent, yaml.Loader)

        localConfigContent = self._configFileManager.getLocalConfigContent()
        self._configLocal = yaml.load(localConfigContent, yaml.Loader)

        self._configInitialized = True

    def _getFromConfigData(self, key: list, config: dict):
        if config is None:
            return None

        item = config.get(key[0])

        for i in range(1, len(key)):
            if item is None:
                return None

            item = item.get(key[i])

        return item
