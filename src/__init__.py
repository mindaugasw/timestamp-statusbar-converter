import platform
import src.services as services
import sys
from src.Service.StatusbarApp import StatusbarApp


def main():
    print(
        f'\n{StatusbarApp.APP_NAME} v{services.statusbarApp.appVersion}\n'
        f'Platform: {platform.platform()}\n'
        f'Detected OS: {services.osSwitch.os}\n'
        f'Python: {sys.version}\n'
        f'Debug: {"enabled" if services.debug.isDebugEnabled() else "disabled"}'
    )

    services.clipboardManager.initializeClipboardWatch()
    services.appLoop.startLoop()
    services.statusbarApp.createApp()


main()
