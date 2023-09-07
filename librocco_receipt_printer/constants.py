import tempfile

COUCH_SERVER = "http://admin:admin@localhost:5000"

VERSION = "v1"

PRINT_OUTPUT_FILE = tempfile.mktemp(dir="/tmp/librocco-receipt-prints")
