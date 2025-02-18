# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "datasets==3.3.0",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from datasets import load_dataset

    ds = load_dataset("wikimedia/wikipedia", "20231101.en")
    return ds, load_dataset


@app.cell
def _(ds):
    df = ds["train"].to_pandas()
    return (df,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
