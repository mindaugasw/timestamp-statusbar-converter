import time
import pasteboard

pb = pasteboard.Pasteboard()

print("START")

while True:
    contents = pb.get_contents(type=pasteboard.String, diff=True)

    if contents is not None:
        print(contents)
    time.sleep(0.5)

print("END")
