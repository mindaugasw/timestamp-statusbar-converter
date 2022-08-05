import platform
import src.services as services


def main():
    if services.osSwitch.isMacOS():
        _hideMacOSDockIcon()

    print('OS: ' + str(services.osSwitch.os) + ', Python: ' + platform.python_version())

    services.clipboard.watchClipboardThreaded()
    services.statusbarApp.createApp()


def _hideMacOSDockIcon():
    import AppKit
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info["LSBackgroundOnly"] = "1"


if __name__ == '__main__':
    main()
