# Bank Statement Converter

## Overview

This repository contains Python Notebook scripts to convert and analyze bank statements.

### `main.ipynb`

The primary notebook converts bank statements into CSV files. Once the script finishes running, a `statement.csv` file will be generated in the `src` directory. The statement information is also available as a dataframe variable `df` for further manipulation.

### `net_positions.ipynb`

This notebook extracts net positions from each bank statement and generates individual CSV files for each bank. It then reads all generated bank CSVs and combines them into a single dataframe for cross-bank analysis and comparison.

## Preparing Your Statements

Place your e-bank statements in the `statements` directory following the naming convention:

```
YYYY-MM.pdf
```

Example templates of supported statement formats can be found in the [assets](./assets) directory.

## How To Run

1. **Install uv**: Download and install [uv](https://docs.astral.sh/uv/) from the official website.
2. **Sync dependencies**: Run `uv sync` to install all project dependencies.
3. **Configure notebook kernel**: Open `main.ipynb` and point the kernel to the generated `.venv` environment.
4. **Run the notebook**: Execute the cells in `main.ipynb` to process your bank statements.

At this current moment, it has the ability to read through the following bank account statements:

- Bank of China
- Citibank
- Hang Seng
- HSBC One
- HSBC Savings
- Standard Chartered

## Script Limitations

### Unable to differentiate between deposits and withdrawals

**Current behavior:**

- Both Deposit and Withdrawal amounts are combined under the same `Amount` column.
- There is no way for the current algorithm to differentiate between the two.

**Root causes:**

1. The extraction process combines all row values into one, and the delineator between deposits and withdrawals is always a space.
2. Balance values can be reliably identified as the last number or when the entry is `C/F BALANCE`.
3. Multi-day transactions only show the balance at the end of the day instead of being recalculated after each transaction.

**Why simple comparison doesn't work:**
Simply comparing the final end-of-day balance to the amount deposited/withdrawn is insufficient. A more advanced algorithm is needed to calculate which amounts should be added/subtracted to reach the final balance.

**Contributions welcome!**
This repository is open to any contributions that could help overcome this limitation.
