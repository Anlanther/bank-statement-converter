# HSBC Bank Statement Converter

This repository holds Python Notebook scripts to convert HSBC bank statements into CSV files. To generate a CSV file for your statements, simply put your e-bank statements into the `statements` directory. You can find example templates of statements that have been used to test these scripts in the [assets](./assets) directory.

All statements that go into the `statements` directory must follow the following naming convention:
`YYYY-MM.pdf`

Once all the script finishes running within a notebook, a `statement.csv` file will be generated at root. Your statement information would also all be saved into a dataframe variable `df`, which you can manipulate even after the run.

## Single Page Converter: sp_converter.ipynb

This script is currently only capable of converting statements that follow the [single page converter template](./assets/sp-converter-sample-template.jpg). While these statements can have multiple pages, this script will only look at transactions within the first page.
