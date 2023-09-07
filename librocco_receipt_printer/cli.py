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


if __name__ == "__main__":
    main()
