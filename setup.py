from setuptools import setup, find_packages


setup(
    name='librocco-receipt-printer',
    version='0.1.0',
    url='https://github.com/librocco/receipt-printer',
    author='Code Myriad',
    author_email='codemyriad@example.com',
    description='Connects to a POS printer and print receipts from a CouchDB database',
    packages=find_packages(),    
    install_requires=[
        "couchdb"
    ],
    entry_points={
        'console_scripts': [
            'librocco-receipt-printer=librocco_receipt_printer.cli:main',
        ],
    },
)
