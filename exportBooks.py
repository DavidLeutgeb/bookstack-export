#!/usr/bin/env python3

import requests
import json
import os
from datetime import date

# Change this vars as you need

bookstack_url = "https://wiki.yourbookstack.local"  # Bookstack Base URL
header = {'Authorization': 'Token xxxx:xxxx'}  # API Token
cert_verify_url = "/etc/ssl/certs/ca-certificates.crt"  # Cert Store for verifying the SSL Cert
export_path = "exports/"  # Where the exported books will be saved

# Leave this vars UNCHANGED

books_url = "{}/api/books".format(bookstack_url)

# Get a list of books available on the Bookstack instance

books = requests.get(books_url, headers=header, verify=cert_verify_url)
books_data = json.dumps(books.json(), separators=(',', ':'))
books_data_loads = json.loads(books_data)
books_data_data = books_data_loads['data']

# Create folder with the current date, if it already exists exit

folder_name = "{}/{}".format(export_path, date.today())

if not os.path.exists(folder_name):
    os.mkdir(folder_name)
else:
    print("Folder already exists")
    exit()


# For every book export it as html

for book in books_data_data:
    export_url = "{}/{}/export/html".format(books_url, book['id'])
    export_file_name = "{}/{}.html".format(folder_name, book['name'])

    book_html = requests.get(export_url, headers=header, verify=cert_verify_url)
    with open(export_file_name, "w+") as file:
        file.write(book_html.text)

    print("Successfully exported book {}".format(book['name']))

print("Export finished")
