# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "docling",
#     "fastembed",
#     "marimo",
#     "openai",
#     "qdrant-client",
# ]
# ///

import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import httpx

    from openai import OpenAI
    from qdrant_client import QdrantClient, models
    from docling.document_converter import DocumentConverter
    from docling.chunking import HybridChunker, HierarchicalChunker
    from fastembed import SparseTextEmbedding

    bm25 = SparseTextEmbedding("Qdrant/bm25")
    openai = OpenAI(base_url="http://localhost:4000", api_key="None")
    qdrant = QdrantClient(url="http://localhost:6333")
    converter = DocumentConverter()

    model_list_request = httpx.get('http://localhost:4000/v1/model/info').json()
    model_list = [model["model_name"] for model in body["data"] if model["model_info"]["mode"] == "embedding"]


@app.cell
def _():
    app_form = mo.md(
    """
    # File Ingestion Pipeline

    ## Usage

    1. Select 1 or more file

    {file_upload}

    2. Select the embedding model

    {model_select}

    3. Select the chunking strategy

    {chunking_select}

    4. Name your collection

    {collection_name}

    5. Submit
    """
    ).batch(
        file_upload=mo.ui.file_browser(multiple=True, selection_mode='file', limit=100),
        model_select=mo.ui.dropdown(options=model_list, full_width=True, searchable=True, label='Embedding Model'),
        chunking_select=mo.ui.dropdown(options=['Hybrid', 'Hierarchical'], value='Hybrid', full_width=True, label='Chunking Strategy'),
        collection_name=mo.ui.text(value='my-collection', full_width=True, label='Collection Name')
    ).form(bordered=False)

    app_form
    return (app_form,)


@app.cell
def _(app_form):
    mo.stop(not app_form.value)

    documents = []
    for value in mo.status.progress_bar(app_form.value['file_upload']):
        file = value.path
        result = converter.convert(file)
        documents.append(result.document)
    return (documents,)


@app.cell
def _(app_form, documents):
    if app_form.value['chunking_select'] == 'Hybrid':
        chunker = HybridChunker()
    else:
        chunker = HierarchicalChunker()

    chunks = []

    for document in documents:
        for chunk in chunker.chunk(dl_doc=document):
            enriched_text = chunker.contextualize(chunk=chunk)
            chunks.append(enriched_text)
    return (chunks,)


@app.cell
def _(app_form):
    def dense_embed(chunk: str):
        response = openai.embeddings.create(input=chunk, model=app_form.value['model_select'])
        embedding = response.data[0].embedding
        return embedding
    return (dense_embed,)


@app.function
def sparse_embed(chunk: str):
    response = next(iter(bm25.query_embed(chunk)))
    embedding = {
        "indices": response.indices.astype(float).tolist(),
        "values": response.values.astype(float).tolist(),
    }
    return embedding


@app.cell
def _(app_form):
    _ = qdrant.recreate_collection(
        collection_name=app_form.value['collection_name'],
        vectors_config={"dense": models.VectorParams(size=1024, distance=models.Distance.COSINE)}, # You must change the size param to match the dimensions of your embedding model
        sparse_vectors_config={"sparse": models.SparseVectorParams()},
    )
    return


@app.cell
def _(chunks, dense_embed):
    points = [
        models.PointStruct(
            id=i,
            vector={
                "dense": dense_embed(chunk),
                "sparse": sparse_embed(chunk),
            },
            payload={
                "content": chunk,
            },
        )
        for i, chunk in enumerate(chunks, start=1)
    ]
    return (points,)


@app.cell
def _(app_form, points):
    for point in points:
        qdrant.upsert(app_form.value['collection_name'], [point], wait=True)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
