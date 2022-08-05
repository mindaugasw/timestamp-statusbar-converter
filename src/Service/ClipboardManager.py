from abc import ABCMeta, abstractmethod


class ClipboardManager(metaclass=ABCMeta):
    @abstractmethod
    def watchClipboardThreaded(self) -> None:
        pass

    @abstractmethod
    def watchClipboard(self) -> None:
        pass

    @abstractmethod
    def setClipboardContent(self, content: str) -> None:
        pass
