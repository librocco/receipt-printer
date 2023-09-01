from escpos.printer import File


class DevPrinter:
    def __init__(self, file):
        print(f"Using dev printer. The print output will be saved to: {file}")
        self.printer = File(devfile=file)

    def print(self, content):
        self.printer.text(content)
        self.printer.cut()
