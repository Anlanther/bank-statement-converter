# Bank Statement Converter

This repository holds a Python Notebook script, `src/main.ipynb` to convert bank statements into CSV files. To generate a CSV file for your statements, simply put your e-bank statements into the `statements` directory. You can find example templates of statements that have been used to test these scripts in the [assets](./assets) directory.

All statements that go into the `statements` directory must follow the following naming convention:
`YYYY-MM.pdf`

Once all the script finishes running within a notebook, a `statement.csv` file will be generated in the `src` directory. Your statement information would also all be saved into a dataframe variable `df`, which you can manipulate even after the run.

## Script Limitations

**Unable to differentiate between withdrawal**
Currently, both Deposit and Withdrawal amounts are combined under the same column: `Amount`, as there is currently no way for the current algorithm to differentiate between the two. This is due to the extraction process putting the values of a row all into one since the delineator between a deposit and withdraw is always a space, whereas a balance can always be identified as the last number next to another number or when the entry is the `C/F BALANCE`.

Furthermore, since multi-day transactions only show the balance at the end of the day instead of it being recalculated after each transaction, simply comparing the final end of day balance to the amount deposited/withdrawn will not work. A more advanced algorithm needs to be created to allow for the calculation of which amounts are supposed to be added/subtracted to get to the final value.

This repository will be open to any contributions that could get these scripts to overcome this limitation.
