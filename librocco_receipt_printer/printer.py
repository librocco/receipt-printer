from contextlib import contextmanager
from escpos.printer import Network
from escpos.printer import Usb
import usb.core
import usb.util
import click
import re


@contextmanager
def get_printer(printer_url):
    """printer_url might be:
    * a numeric IP address (like "10.10.10.10")
    * a string representing a USB device (like "0x04b8,0x0202")
    """
    printer = None

    try:
        if all(char in "0123456789." for char in printer_url):
            printer = Network(printer_url, port=9100)
        elif (
            re.fullmatch(r"0x[0-9A-Fa-f]{4},0x[0-9A-Fa-f]{4}", printer_url) is not None
        ):
            vendor_id, product_id = map(lambda x: int(x, 16), printer_url.split(","))
            printer = Usb(vendor_id, product_id)
        else:
            raise RuntimeError(f"Invalid printer URL: {printer_url}")

        yield printer

    finally:
        if isinstance(printer, Usb):
            # Ensure the USB interface is released
            usb.util.release_interface(printer.device, 0)
            # Ensure the USB device is closed
            printer.device.reset()
            usb.util.dispose_resources(printer.device)


def do_print(printer_url, receipt_data):
    total = 0
    discounted_total = 0

    with get_printer(printer_url) as printer:

        # Start bold text for the receipt header
        printer.set(align="center", font="a", width=2, height=2, bold=True)
        printer.text("Il Libraio\n")
        printer.text("via XX Settembre, 5, Cuneo\n")
        printer.text("0171/602018\n")
        printer.text("illibraio.cuneo@gmail.com\n\n\n")
        printer.set(bold=False)

        for item in receipt_data["items"]:
            discount = item["discount"]
            original_price = item["price"] * item["quantity"]
            discounted_price = original_price * (100 - discount) / 100

            printer.set(align="left", bold=False)
            printer.text(f"{item['title']}\n")
            if item["quantity"] != 1:
                printer.text(f"Quantità: {item['quantity']}\n")

            # Enable bold for price display
            printer.set(align="right", bold=True)
            printer.text(f"Prezzo: {item['price']:.2f} €\n")
            printer.text(f"Sconto: {discount}%\n")
            printer.text(f"Prezzo scontato: {discounted_price:.2f} €\n\n")
            printer.set(align="left", bold=False)

            total += original_price
            discounted_total += discounted_price

        total_discount = total - discounted_total

        printer.set(bold=True)
        if total_discount != 0:
            printer.text(f"Subtotale:\t{total:.2f} €\n")
            printer.text(f"Sconto:\t{total_discount:.2f} €\n")
            printer.text(f"Totale scontato:\t{discounted_total:.2f} €\n")
        else:
            printer.text(f"Totale:\t{discounted_total:.2f} €\n")
        printer.set(bold=False)

        printer.cut()


@click.command()
@click.option("--printer-url", default=None, required=True, help="URL for the printer")
def main(printer_url):
    """Edit the "URL" (It's an IP address) and run
    python -m librocco_receipt_printer.printer

    to test this with a network printer
    """
    do_print(printer_url, TEST_DATA)


TEST_DATA = {
    "items": [
        {
            "isbn": "9788874475155",
            "title": "I rampicanti più belli. Spalliere, pergolati, pareti fiorite",
            "price": 9.9,
            "quantity": 2,
            "discount": 20,
        },
        {
            "isbn": "9788874475179",
            "title": "Prati verdi e fioriti. La preparazione del terreno, la scelta delle sementi, le cure, gli strumenti di lavoro",
            "price": 9.9,
            "quantity": 1,
            "discount": 50,
        },
        {
            "isbn": "9788874475209",
            "title": "Piante da bulbo. La scelta, le cure",
            "price": 9.9,
            "quantity": 1,
            "discount": 10,
        },
        {
            "isbn": "9788874476282",
            "title": "Agrumi in vaso e in piena terra. Scelta, cura, messa a dimora (Gli)",
            "price": 9.9,
            "quantity": 1,
            "discount": 0,
        },
        {
            "isbn": "9788874476305",
            "title": "Piante aromatiche. Una sinfonia di profumi e di sapori in giardino e in casa",
            "price": 9.9,
            "quantity": 2,
            "discount": 0,
        },
        {
            "isbn": "9788874476367",
            "title": "Angoli relax in giardino. Le piante, gli arbusti fioriti, gli arredi",
            "price": 9.9,
            "quantity": 1,
            "discount": 0,
        },
    ],
    "timestamp": 1714654899541,
}


if __name__ == "__main__":
    main()
