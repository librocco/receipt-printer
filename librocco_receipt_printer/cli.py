import os
from couchdb import Server


from .constants import COUCH_SERVER, PRINT_OUTPUT_FILE
from .printer import DevPrinter
from .print_queue import PrintQueue


def main():
    server = Server(COUCH_SERVER)
    db = server["dev"]

    # Create a print output file if it doesn't exist
    os.makedirs(os.path.dirname(PRINT_OUTPUT_FILE), exist_ok=True)
    open(PRINT_OUTPUT_FILE, "a")

    printer = DevPrinter(PRINT_OUTPUT_FILE)
    print_queue = PrintQueue(db, "printer-1")

    print(f"Connecting to {COUCH_SERVER} and waiting for jobs")
    try:
        print_queue.start(printer)
    except KeyboardInterrupt:
        print("Exiting")


def dry_run():
    """Dry run is used for `librocco-print-test` command. It prints a canned receipt
    and is used to test the printer being connected and accessible.

    TODO: This should most definitely be an actual printer, not a test file

    TODO: When we proceed with the implementation (and formatting of receipts) we'd
    probably want to store a dummy receipt and print it out (instead of just printing out the "Test receipt" string)
    """

    printer = DevPrinter(PRINT_OUTPUT_FILE)
    printer.print("Test receipt\n")


if __name__ == "__main__":
    main()

if __name__ == "__dry_run__":
    dry_run()
