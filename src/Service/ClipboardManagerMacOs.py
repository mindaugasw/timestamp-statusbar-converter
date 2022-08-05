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

            # On first iteration Pasteboard will return content copied before
            # opening app, which is not desired
            if firstIteration:
                firstIteration = False
                continue

            # If content did not change between 2 polls, pb.get_contents() will
            # return None.
            if content is not None:
                events.clipboardChanged(content)

            time.sleep(self._pollingInterval)

    def setClipboardContent(self, content: str) -> None:
        try:
            self._pb.set_contents(content)
        except Exception as e:
            # TODO create a custom exception class that allows passing previous exception
            raise Exception('Could not set clipboard content.\nOriginal exception: ' + str(e))
