import os
# TODO remove
from abc import ABCMeta, abstractmethod
import rumps
from src.Service.StatusbarApp import StatusbarApp


class ConfigFileManager(metaclass=ABCMeta):
    CONFIG_GLOBAL = 'config.yml'
    CONFIG_LOCAL = 'config.local.yml'
    CONFIG_LOCAL_EXAMPLE = 'config.local.example.yml'

    # TODO remove
    # @abstractmethod
    # def openFile(self):
    #     pass

    # def __init__(self):
    #     events.clipboardChanged.append(lambda x: self.getLocalConfigContent())

    def getLocalConfigContent(self) -> str:
        if not self._localConfigExists():
            self._createLocalConfig()

        with open(self._getLocalConfigFullPath(), 'r') as localConfigFile:
            return localConfigFile.read()

    def getGlobalConfigContent(self) -> str:
        with open(self._getGlobalConfigFullPath(), 'r') as globalConfigFile:
            return globalConfigFile.read()

    def _getTempFilesDirectory(self) -> str:
        return rumps.application_support(StatusbarApp.APP_NAME)

    def _getLocalConfigFullPath(self) -> str:
        return f"{self._getTempFilesDirectory()}/{self.CONFIG_LOCAL}"

    def _localConfigExists(self) -> bool:
        return os.path.isfile(self._getLocalConfigFullPath())

    def _createLocalConfig(self) -> None:
        copyFrom = '../' + self.CONFIG_LOCAL_EXAMPLE
        copyTo = self._getLocalConfigFullPath()

        os.popen(f'cp "{copyFrom}" "{copyTo}"')

    def _getGlobalConfigFullPath(self) -> str:
        return '../' + self.CONFIG_GLOBAL
