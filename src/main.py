import platform
import src.services as services


def main():
    if services.osSwitch.isMacOS():
        _hideMacOSDockIcon()

    # TODO print app version as well
    print('OS: %s, Python: %s' % (services.osSwitch.os, platform.python_version()))

    services.clipboard.watchClipboardThreaded()
    services.statusbarApp.createApp()


def _hideMacOSDockIcon():
    import AppKit
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info["LSBackgroundOnly"] = "1"


if __name__ == '__main__':
    main()
