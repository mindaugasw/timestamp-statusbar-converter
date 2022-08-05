import pasteboard
import threading
import time
from src.Service.ClipboardManager import ClipboardManager
from src.Service.Configuration import Configuration
from src.Service.Debug import Debug
import src.events as events


class ClipboardManagerMacOs(ClipboardManager):
    _pb: pasteboard.Pasteboard
    _debug: Debug
    _pollingInterval: float

    def __init__(self, config: Configuration, debug: Debug):
        self._debug = debug
        self._pb = pasteboard.Pasteboard()
        self._pollingInterval = config.get(config.CLIPBOARD_POLLING_INTERVAL)

    def watchClipboardThreaded(self) -> None:
        # TODO move this to common class?
        threading.Thread(target=self.watchClipboard).start()

    def watchClipboard(self) -> None:
        firstIteration = True

        while True:
            content = self._pb.get_contents(type=pasteboard.String, diff=True)

            # If content did not change between 2 polls, pb.get_content will
            # return None.
            # On first iteration will return content copied before opening app,
            # which is not desired
            if content is not None and not firstIteration:
                events.clipboardChanged(content)
            else:
                firstIteration = False

            time.sleep(self._pollingInterval)
