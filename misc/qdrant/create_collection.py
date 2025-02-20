# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "datasets==3.3.0",
#     "fastembed==0.5.1",
#     "marimo",
#     "openai==1.63.2",
#     "qdrant-client==1.13.2",
# ]
# ///

import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    run_button = mo.ui.run_button()
    run_button
    return (run_button,)


@app.cell
def _(mo, run_button):
    mo.stop(not run_button.value)

    from datasets import load_dataset

    ds = load_dataset("wikimedia/wikipedia", "20231101.en", split="train[:100]")
    df = ds.to_pandas()
    return df, ds, load_dataset


@app.cell
def _(df):
    df.columns
    return


@app.cell
def _(df):
    df["text"]
    return


@app.cell
def _():
    def create_chunks(row):
        text: str = row["text"]

        sentences = text.split("\n\n")

        filtered_sentences = [sentence for sentence in sentences if len(sentence) >= 20 and len(sentence) <= 500]

        return filtered_sentences
    return (create_chunks,)


@app.cell
def _():
    def count_chunks(row):
        return len(row["chunks"])
    return (count_chunks,)


@app.cell
def _(count_chunks, create_chunks, df):
    df["chunks"] = df.apply(create_chunks, axis=1)
    df["chunk_count"] = df.apply(count_chunks, axis=1)
    return


@app.cell
def _(df):
    df[["chunks", "chunk_count"]]
    return


@app.cell
def _(df):
    df_exploded = df.explode("chunks")
    return (df_exploded,)


@app.cell
def _(df_exploded):
    df_exploded["chunks"]
    return


@app.cell
def _():
    from openai import OpenAI

    openai = OpenAI(base_url="http://localhost:4000", api_key="none_but_required")
    return OpenAI, openai


@app.cell
def _(openai):
    def create_embeddings(row):
        chunk: str = row["chunks"]

        response = openai.embeddings.create(input=chunk, model="text-embedding-3-large")

        embedding = response.data[0].embedding

        return embedding
    return (create_embeddings,)


@app.cell
def _(create_embeddings, df_exploded):
    df_exploded["vectors"] = df_exploded.apply(create_embeddings, axis=1)
    return


@app.cell
def _():
    from fastembed import SparseTextEmbedding

    bm25 = SparseTextEmbedding("Qdrant/bm25")
    return SparseTextEmbedding, bm25


@app.cell
def _(bm25):
    def create_sparse_embeddings(row):
        chunk: str = row["chunks"]

        response = next(iter(bm25.query_embed(chunk)))

        embedding = (
            response.indices.astype(float).tolist(),
            response.values.astype(float).tolist(),
        )

        return embedding
    return (create_sparse_embeddings,)


@app.cell
def _(create_sparse_embeddings, df_exploded):
    df_exploded["sparse_vectors"] = df_exploded.apply(create_sparse_embeddings, axis=1)
    return


@app.cell
def _():
    from qdrant_client import QdrantClient, models

    qdrant = QdrantClient()
    return QdrantClient, models, qdrant


@app.cell
def _(models, qdrant):
    qdrant.recreate_collection(
        collection_name="Wikipedia",
        vectors_config={"dense": models.VectorParams(size=3072, distance=models.Distance.COSINE)},
        sparse_vectors_config={"sparse": models.SparseVectorParams()},
    )
    return


@app.cell
def _(df_exploded):
    records = df_exploded.to_dict(orient="records")
    return (records,)


@app.cell
def _(records):
    records[0].keys()
    return


app._unparsable_cell(
    r"""
    2points = [
        models.PointStruct(
            id=id,
            vector={
                \"dense\": row[\"vectors\"],
                \"sparse\": {
                    \"indices\": row[\"sparse_vectors\"][0],
                    \"values\": row[\"sparse_vectors\"][1],
                },
            },
            payload={
                \"content\": row[\"chunks\"],
                \"url\": row[\"url\"],
                \"title\": row[\"title\"],
            },
        )
        for id, row in enumerate(records)
    ]
    """,
    name="_"
)


@app.cell
def _(points, qdrant):
    for point in points:
        qdrant.upsert("Wikipedia", [point], wait=True)
    return (point,)


if __name__ == "__main__":
    app.run()
