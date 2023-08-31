import time

from .constants import VERSION

from .print_job import PrintJob


class PrintQueue(object):
    def __init__(self, db, printer_id):
        self.db = db
        self.printer_id = printer_id

    def stream_changes(self, since="now", selector=None):
        last_seq = since

        while True:
            changes = self.db.changes(
                since=last_seq,
                feed="longpoll",
                heartbeat=10000,
                headers={"Content-Type": "application/json"},
                filter="_selector",
                _selector=selector,
            )
            last_seq = changes["last_seq"]
            for change in changes["results"]:
                yield change
            time.sleep(1)

    def listen(self):
        basepath = f"{VERSION}/print_queue/{self.printer_id}"
        selector = {
            "selector": {"_id": {"$gte": f"{basepath}/", "$lt": f"{basepath}0"}}
        }
        for change in self.stream_changes(selector=selector):
            yield PrintJob.load(self.db, change.get("id"))
