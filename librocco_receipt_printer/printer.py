import time

from escpos.printer import File


class DevPrinter:
    def __init__(self, file):
        print(f"Using dev printer. The print output will be saved to: {file}")
        self.printer = File(devfile=file)

    def print(self, content):
        # We're sleeping for 2 secs to simulate the printing process
        time.sleep(2)

        self.printer.text(content)
        self.printer.cut()
