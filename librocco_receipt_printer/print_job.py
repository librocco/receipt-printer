from couchdb.mapping import (
    Document,
    TextField,
    ListField,
    DictField,
    IntegerField,
    FloatField,
    LongField,
    Mapping,
)


class PrintJob(Document):
    """A CouchDB document mapping for a print job document.

    The print job document is essentially a message stored stored in the print queue part of the
    database, used to schedule and keep track of print jobs.

    Fields:
        printer_id: The ID of the printer that this print job is for
        content: The content of the print job

    TODO: Make this more elaborate, this is just a placeholder
    """

    def __str__(self):
        # Last segment of the id, e.g. 'print_queue/printer1/1' -> '1'
        short_id = self.id.split("/")[-1]

        str = f"Receipt '{short_id}':\n"
        str += f"  Items:\n"
        for entry in self.items:
            str += f"    isbn = '{entry['isbn']}'"
            str += f" title = '{entry['title']}'"
            str += f" quantity = {entry['quantity']}"
            str += f" price = {entry['price']}\n"
        str += f"\n  Total: {self.total}\n"
        return str

    def processing(self, db):
        """Set the status of the print job to 'PROCESSING' and store it in the database."""
        self.status = "PROCESSING"
        self.store(db)

    def done(self, db):
        """Set the status of the print job to 'DONE' and store it in the database."""
        self.status = "DONE"
        self.store(db)

    def error(self, db, error):
        """Set the status of the print job to 'ERROR' and store it in the database."""
        self.status = "ERROR"
        self.error = error
        self.store(db)

    def print(self, printer):
        """Print the print job to the printer."""
        printer.print(str(self))

    # Job data
    printer_id = TextField()
    status = TextField()
    error = TextField()

    # Receipt data
    items = ListField(
        DictField(
            Mapping.build(
                isbn=TextField(),
                title=TextField(),
                quantity=IntegerField(),
                price=FloatField(),
            )
        )
    )
    total = FloatField()
    timestamp = LongField()
