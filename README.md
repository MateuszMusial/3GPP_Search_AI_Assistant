# 3GPP Search Agent

This project is a Python-based application designed to perform Retrieval-Augmented Generation (RAG) on 3GPP technical specification documents. Currently, the application implements the **data ingestion and indexing pipeline**, utilizing Google's Gemini models or OpenAI models, and FAISS for vector storage.

## Features

-   **RAG Pipeline (Ingestion & Indexing):** Efficiently processes and indexes 3GPP documents.
-   **Multi-Model Support:** Seamlessly switch between Google Gemini and OpenAI models.
-   **Vector Search:** Uses FAISS for fast similarity search on embedded 3GPP documents.

## Project Structure

The core application code resides in the `src/search_agent/` directory, following a standard Python src-layout.

## Architecture Flow

The system's data flow for ingestion and indexing:
`PDF Documents` ---> `PyMuPDF (Document Loading)` ---> `RecursiveCharacterTextSplitter (Text Splitting)` ---> `Embedding Model (Embedding)` ---> `FAISS (Vector Indexing)`

For query answering (planned inference):
`User Query` ---> `LLM (Query Processing)` ---> `FAISS (Vector Search)` ---> `Retrieved Chunks` ---> `LLM (Answer Generation)` ---> `Answer`

## Prerequisites

- Python 3.13+
- `uv` package manager (recommended) or `pip`
- Google API Key (for Gemini models) or OpenAI API Key (for OpenAI models)

## Setup

1.  **Install dependencies and project in editable mode:**
    Using `uv`:
    ```bash
    uv sync
    ```
    This command will install all required dependencies and the `3gpp-search-agent` package itself in editable mode, making it importable.

2.  **Environment Configuration:**
    Create a `.env` file in the root directory and set your API keys:
    ```bash
    GOOGLE_API_KEY=your_google_api_key_here
    OPENAI_API_KEY=your_openai_api_key_here
    ```

3.  **Prepare Data:**
    Place your 3GPP PDF documents (e.g., `ts_124501v171600p.pdf`) in the `data/` directory.

## Usage

### Running Queries

To run queries against the indexed documents using the `--ie` (information element) and optionally `--model` arguments:

```bash
uv run python -m search_agent.main --ie "RLF timer"
```

Available models:
- Google Generative: `gemini-3-pro-preview` (default), `gemini-2.5-flash`
- OpenAI: `gpt-5-nano`, `gpt-4.0-turbo-preview`

### Running Tests

To execute the test suite:

```bash
uv run pytest
```

## Development

### Code Style

The project uses `ruff` for linting.

```bash
uv run ruff check .
```