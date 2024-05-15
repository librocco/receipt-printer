from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
import click
import json
import uvicorn
from .printer import do_print
from .printer import get_printer
from .constants import OPTIONS

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "An http endpoint to print ESC/POS receipts"


@app.get("/printreceipt")
async def print_label():
    return {"message": f"Use POST instead"}


@app.post("/printreceipt")
async def print_label(request: Request):
    # Get the  book data from bookData POST var
    try:
        receipt_data = await request.json()
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=405, detail="Invalid JSON data: %s" % e)

    do_print(printer_url=OPTIONS["PRINTER_URL"], receipt_data=receipt_data)

    return {"status": "OK", "message": f"Receipt printed"}


@click.command()
@click.option("--printer-url", default=None, help="URL for the printer")
@click.option("--port", default="8000", help="Port to run the server on", type=int)
def main(port, printer_url):
    # Smoke test the printer
    with get_printer(printer_url) as printer:
        pass
    OPTIONS["PRINTER_URL"] = printer_url
    print(f"Starting server with printer url {printer_url}")
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
