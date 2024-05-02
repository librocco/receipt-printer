from escpos.printer import Network
import click


def do_print(printer_url, recept_data):
    printer = Network(printer_url)
    total = 0
    for element in recept_data["items"]:
        printer.text(element["title"] + "\n")
        printer.text(str(element["price"]) + "\n")
        total += element["price"] * element["quantity"]
    printer.text("")
    printer.text(f"Total: {total}")
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
            "title": "I rampicanti piÃ¹ belli. Spalliere, pergolati, pareti fiorite",
            "price": 9.9,
            "quantity": 2,
            "discount": 0,
        },
        {
            "isbn": "9788874475179",
            "title": "Prati verdi e fioriti. La preparazione del terreno, la scelta delle sementi, le cure, gli strumenti di lavoro",
            "price": 9.9,
            "quantity": 1,
            "discount": 0,
        },
        {
            "isbn": "9788874475209",
            "title": "Piante da bulbo. La scelta, le cure",
            "price": 9.9,
            "quantity": 1,
            "discount": 0,
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
