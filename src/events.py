from src.Service.Event import Event

# Raised when clipboard content changes, not necessarily to a valid timestamp.
# Passed a string with new clipboard content
clipboardChanged = Event()

# Raised after clipboard change, if a valid timestamp was found.
# Passed a Timestamp object
timestampChanged = Event()

# Raised when previously found timestamp should be cleared, either because new
# content was copied (but not valid timestamp to call timestampChanged()), or
# timestamp clear countdown elapsed after last valid timestamp.
# Will be raised only if either method for clearing is configured by the user.
timestampCleared = Event()
