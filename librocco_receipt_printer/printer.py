from escpos.printer import Network
from escpos.printer import Usb
import re


def get_printer(printer_url):
    """printer_url might be:
    * a numeric IP address (like "10.10.10.10")
    * a string representing a USB device (like "0x04b8,0x0202")
    """
    # If the URL only contains digits and dots, it's an IP address
    if all(char in "0123456789." for char in printer_url):
        return Network(printer_url)
    elif re.fullmatch(r"0x[0-9A-Fa-f]{4},0x[0-9A-Fa-f]{4}", printer_url) is not None:
        vendor_id, product_id = map(lambda x: int(x, 16), printer_url.split(","))
        return Usb(vendor_id, product_id)
    raise RuntimeError(f"Invalid printer URL: {printer_url}")


def do_print(printer_url, receipt_data):
    printer = get_printer(printer_url)
    total = 0
    discounted_total = 0

    # Start bold text for the receipt header
    printer.set(align="center", bold=True)
    printer.text("Your local bookshop\n\n")
    printer.set(bold=False)

    for item in receipt_data["items"]:
        discount = item["discount"]
        original_price = item["price"] * item["quantity"]
        discounted_price = original_price * (100 - discount) / 100

        printer.set(align="left", bold=False)
        printer.text(f"{item['title']}\n")
        printer.text(f"Quantity: {item['quantity']}\n")

        # Enable bold for price display
        printer.set(align="right", bold=True)
        printer.text(f"Price: {item['price']:.2f} €\n")
        printer.text(f"Discount: {discount}%\n")
        printer.text(f"Discounted Price: {discounted_price:.2f} €\n\n")
        printer.set(align="left", bold=False)

        total += original_price
        discounted_total += discounted_price

    # Display totals in bold
    printer.set(bold=True)
    printer.text(f"Subtotal: {total:.2f} €\n")
    printer.text(f"Total after Discounts: {discounted_total:.2f} €\n")
    printer.set(bold=False)

    printer.cut()


def main():
    """Edit the "URL" (It's an IP address) and run
    python -m librocco_receipt_printer.printer

    to test this with a network printer
    """
    do_print("100.98.209.46", TEST_DATA)


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
