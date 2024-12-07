from typing import TypeVar

from src.Constant.ModalId import ModalId
from src.Service.AppLoop import AppLoop
from src.Service.ArgumentParser import ArgumentParser
from src.Service.AutostartManager import AutostartManager
from src.Service.ClipboardManager import ClipboardManager
from src.Service.ConfigFileManager import ConfigFileManager
from src.Service.Configuration import Configuration
from src.Service.Conversion.ThousandsDetector import ThousandsDetector
from src.Service.ConversionManager import ConversionManager
from src.Service.Converter.ConverterInterface import ConverterInterface
from src.Service.Converter.SimpleUnit.SimpleUnitConverter import SimpleUnitConverter
from src.Service.Converter.SimpleUnit.TemperatureConverter import TemperatureConverter
from src.Service.Converter.SimpleUnit.UnitPreprocessor import UnitPreprocessor
from src.Service.Converter.TimestampConverter import TimestampConverter
from src.Service.Debug import Debug
from src.Service.ExceptionHandler import ExceptionHandler
from src.Service.FilesystemHelper import FilesystemHelper
from src.Service.Logger import Logger
from src.Service.ModalWindow.AboutBuilder import AboutBuilder
from src.Service.ModalWindow.DemoBuilder import DemoBuilder
from src.Service.ModalWindow.DialogBuilder import DialogBuilder
from src.Service.ModalWindow.ModalWindowBuilderInterface import ModalWindowBuilderInterface
from src.Service.ModalWindow.ModalWindowManager import ModalWindowManager
from src.Service.ModalWindow.SettingsBuilder import SettingsBuilder
from src.Service.OSSwitch import OSSwitch
from src.Service.StatusbarApp import StatusbarApp
from src.Service.TimestampTextFormatter import TimestampTextFormatter
from src.Service.UpdateManager import UpdateManager


class ServiceContainer:
    T = TypeVar('T')

    _services: dict[type, object]

    def __init__(self, initialize: bool):
        _: dict[type, object] = {}

        # Core services
        _[OSSwitch] = osSwitch = OSSwitch()
        _[FilesystemHelper] = filesystemHelper = self._getFilesystemHelper(osSwitch)
        _[Logger] = logger = Logger(filesystemHelper)

        if initialize:
            logger.logRaw(filesystemHelper.getInitializationLogs())
            ExceptionHandler.initialize()

        _[ConfigFileManager] = configFileManager = ConfigFileManager(filesystemHelper, logger)
        _[Configuration] = config = Configuration(configFileManager, logger)
        _[ArgumentParser] = argumentParser = ArgumentParser()
        _[Debug] = debug = Debug(config, argumentParser)

        # Conversion services
        _[TimestampTextFormatter] = timestampTextFormatter = TimestampTextFormatter(config)
        _[UnitPreprocessor] = unitPreprocessor = UnitPreprocessor()
        _[ThousandsDetector] = thousandsDetector = ThousandsDetector()
        _[TemperatureConverter] = temperatureConverter = TemperatureConverter(unitPreprocessor, config)
        _[list[ConverterInterface]] = converters = [
            TimestampConverter(timestampTextFormatter, config, logger),
            SimpleUnitConverter(temperatureConverter, thousandsDetector),
        ]
        _[ConversionManager] = conversionManager = ConversionManager(converters, config, logger, debug)

        # GUI services
        _[list[ModalWindowBuilderInterface]] = modalWindowBuilders = self._getModalWindowBuilders(config)
        _[ModalWindowManager] = modalWindowManager = ModalWindowManager(modalWindowBuilders, osSwitch, logger)

        # App services
        _[UpdateManager] = updateManager = UpdateManager(filesystemHelper, config, logger, debug)
        _[AutostartManager] = autostartManager = self._getAutostartManager(osSwitch, config, filesystemHelper, logger)
        _[ClipboardManager] = clipboardManager = self._getClipboardManager(osSwitch, logger)
        _[StatusbarApp] = statusbarApp = self._getStatusbarApp(osSwitch, timestampTextFormatter, clipboardManager, conversionManager, config, configFileManager, autostartManager, updateManager, modalWindowManager, logger, debug)
        _[AppLoop] = appLoop = AppLoop(osSwitch)

        self._services = _

    def __getitem__(self, item: type[T]) -> T:
        if item not in self._services:
            raise Exception(f'Service with id "{item}" not found in the container')

        return self._services[item]

    def get(self, _id: type):
        if _id not in self._services:
            raise Exception(f'Service with id "{_id}" not found in the container')

        return self._services[_id]

    def _getFilesystemHelper(self, osSwitch: OSSwitch) -> FilesystemHelper:
        if osSwitch.isMacOS():
            from src.Service.FilesystemHelperMacOs import FilesystemHelperMacOs
            return FilesystemHelperMacOs()
        else:
            from src.Service.FilesystemHelperLinux import FilesystemHelperLinux
            return FilesystemHelperLinux()

    def _getModalWindowBuilders(self, config: Configuration) -> dict[str, ModalWindowBuilderInterface]:
        return {
            ModalId.demo: DemoBuilder(),
            ModalId.settings: SettingsBuilder(),
            ModalId.about: AboutBuilder(config),
            ModalId.dialog: DialogBuilder(),
        }

    def _getAutostartManager(
        self,
        osSwitch: OSSwitch,
        config: Configuration,
        filesystemHelper: FilesystemHelper,
        logger: Logger,
    ) -> AutostartManager:
        if osSwitch.isMacOS():
            from src.Service.AutostartManagerMacOS import AutostartManagerMacOS
            return AutostartManagerMacOS(config, filesystemHelper, logger)
        else:
            from src.Service.AutostartManagerLinux import AutostartManagerLinux
            return AutostartManagerLinux(config, filesystemHelper, logger)

    def _getClipboardManager(self, osSwitch: OSSwitch, logger: Logger) -> ClipboardManager:
        if osSwitch.isMacOS():
            from src.Service.ClipboardManagerMacOs import ClipboardManagerMacOs
            return ClipboardManagerMacOs(logger)
        else:
            from src.Service.ClipboardManagerLinux import ClipboardManagerLinux
            return ClipboardManagerLinux(logger)

    def _getStatusbarApp(
        self,
        osSwitch: OSSwitch,
        timestampTextFormatter: TimestampTextFormatter,
        clipboardManager: ClipboardManager,
        conversionManager: ConversionManager,
        config: Configuration,
        configFileManager: ConfigFileManager,
        autostartManager: AutostartManager,
        updateManager: UpdateManager,
        modalWindowManager: ModalWindowManager,
        logger: Logger,
        debug: Debug,
    ) -> StatusbarApp:
        if osSwitch.isMacOS():
            from src.Service.StatusbarAppMacOs import StatusbarAppMacOs
            return StatusbarAppMacOs(
                osSwitch,
                timestampTextFormatter,
                clipboardManager,
                conversionManager,
                config,
                configFileManager,
                autostartManager,
                updateManager,
                modalWindowManager,
                logger,
                debug,
            )
        else:
            from src.Service.StatusbarAppLinux import StatusbarAppLinux
            return StatusbarAppLinux(
                osSwitch,
                timestampTextFormatter,
                clipboardManager,
                conversionManager,
                config,
                configFileManager,
                autostartManager,
                updateManager,
                modalWindowManager,
                logger,
                debug,
            )
