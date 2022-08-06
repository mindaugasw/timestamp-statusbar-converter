from src.Service.OSSwitch import OSSwitch
from src.Service.Configuration import Configuration
from src.Service.TimestampParser import TimestampParser
from src.Service.ConfigFileManager import ConfigFileManager
from src.Service.TimestampTextFormatter import TimestampTextFormatter
from src.Service.Debug import Debug
from src.Service.ClipboardManager import ClipboardManager
from src.Service.StatusbarApp import StatusbarApp

osSwitch = OSSwitch()
configFileManager = ConfigFileManager()
config = Configuration(configFileManager)
debug = Debug(config)
timestampParser = TimestampParser(config, debug)
timestampTextFormatter = TimestampTextFormatter(config)
clipboard: ClipboardManager
statusbarApp: StatusbarApp

if osSwitch.isMacOS():
    from src.Service.ClipboardManagerMacOs import ClipboardManagerMacOs
    from src.Service.StatusbarAppMacOs import StatusbarAppMacOs

    clipboard = ClipboardManagerMacOs(config, debug)
    statusbarApp = StatusbarAppMacOs(timestampTextFormatter, clipboard, timestampParser, config, configFileManager)
else:
    from src.Service.ClipboardManagerLinux import ClipboardManagerLinux
    from src.Service.StatusbarAppLinux import StatusbarAppLinux

    clipboard = ClipboardManagerLinux()
    statusbarApp = StatusbarAppLinux()
