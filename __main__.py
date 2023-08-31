from couchdb import Server


from constants import COUCH_SERVER
from print_queue import PrintQueue


def main():
    server = Server(COUCH_SERVER)
    db = server["dev"]

    print_queue = PrintQueue(db, "printer-1")

    for job in print_queue.listen():
        print(job)


if __name__ == "__main__":
    main()
