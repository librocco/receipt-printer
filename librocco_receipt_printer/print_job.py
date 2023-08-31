from couchdb.mapping import Document, TextField


class PrintJob(Document):
    """A CouchDB document mapping for a print job document.

    The print job document is essentially a message stored stored in the print queue part of the
    database, used to schedule and keep track of print jobs.

    Fields:
        printer_id: The ID of the printer that this print job is for
        content: The content of the print job

    TODO: Make this more elaborate, this is just a placeholder
    """

    printer_id = TextField()
    content = TextField()
