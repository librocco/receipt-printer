import time

from .constants import VERSION

from .print_job import PrintJob


class PrintQueue:
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

    def process_job(self, job):
        # If the print job document is deleted (which shouldn't happen, but still...),
        # it would trigger an empty result on change query, which would cause an exception.
        # We're checking for this edge case here.
        if job is None:
            return

        # Account only for pending print jobs
        if job.status != "PENDING" or job.printer_id != self.printer_id:
            return

        print(f"Received job {job.id} for printer {job.printer_id}")
        job.processing(self.db)

        print(f"Printing job {job.id}...")
        job.print(self.printer)

        job.done(self.db)
        print(f"Job {job.id} done\n")

    def listen(self):
        basepath = f"{VERSION}/print_queue/{self.printer_id}"
        selector = {
            "selector": {"_id": {"$gte": f"{basepath}/", "$lt": f"{basepath}0"}}
        }
        for change in self.stream_changes(selector=selector):
            yield PrintJob.load(self.db, change.get("id"))

    def start(self, printer):
        self.printer = printer

        # TODO: Have the printer signal that it's online and ready to receive jobs

        for job in self.listen():
            self.process_job(job)
