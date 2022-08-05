from src.Service.Event import Event

# Raised when clipboard content changes, not necessarily to a valid timestamp.
# Passed a string with new clipboard content
clipboardChanged = Event()

# Raised after clipboard change, if a valid timestamp was found.
# Passed an integer with new timestamp
timestampChanged = Event()
